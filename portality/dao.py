import esprit
from portality.core import app

class LV_DAO(esprit.dao.DAO):
    def differential(self, existing, target):
        new = []
        removed = []
        unchanged = []
        
        for t in target:
            if t in existing:
                unchanged.append(t)
            else:
                new.append(t)
        
        for e in existing:
            if e not in target:
                removed.append(e)
        
        return new, removed, unchanged
    
    def prep_id(self, obj):
        id = None
        isnew = False
        
        # if there's no id, generate one
        if "id" not in obj:
            id = self.makeid()
            obj["id"] = id
            isnew = True
        else:
            id = obj["id"]
        
        return id, isnew

    def make_es_connection(self, host=None, port=None, index=None):
        host = app.config['ELASTIC_SEARCH_HOST'] if host is None else host
        index = app.config['ELASTIC_SEARCH_DB'] if index is None else index
        conn = esprit.raw.Connection(host, index, port)
        return conn
    
    def relationship_actions(self, conn, index, rel_query, target_field, new_values, ignore_id=None):
        """
        conn - ES connection object
        index - index in which to look for relationships
        rel_query - query which obtains the relevant relationships
        target_field - field in the relationship object which refers to the foreign object in the relationshio
        new_values - the values that we want to change the relationships to, used to compute the differential
        ignore_id - for relationships where there is one list field which holds the equivalence, 
                    this is the id to omit from the result set (i.e. the id of the object at the centre of 
                    the working context)
        """
        existing = []
        idmap = {}
        
        existing_resp = esprit.raw.search(conn, index, rel_query)
        objects = esprit.raw.unpack_result(existing_resp)
        for o in objects:
            target = None
            field = o.get(target_field)
            if isinstance(field, list):
                target = [f for f in field if f != ignore_id][0]
            else:
                target = field
            existing.append(target)
            idmap[target] = o.get("id")
            
        new, removed, unchanged = self.differential(existing, new_values)
        return new, removed, unchanged, idmap

class SongStoreDAO(LV_DAO):
    def save(self, host=None, port=None, index=None):
        # can we proceed with storage?
        song = self.data.get("song")
        if song is None:
            # song element must be present if only to access the id
            raise esprit.dao.StoreException("song element must be present")
        
        # sort out an id for the object to be stored
        id, isnew = self.prep_id(song)
        
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # extract the relational information we're interested in
        versions = self.data.get("versions")
        songs = self.data.get("songs")
        
        # we're going to compute all of the ES queries, and then execute them
        # together later
        action_queue = []
        
        # if there are version references, then if this is a new record compare and
        # get the differential on the existing record.  Then action any removals and
        # additions
        if versions is not None:
            idmap = {}
            new, removed = versions, []
            if not isnew:
                version_query = esprit.models.Query.term("song_id.exact", id)
                new, removed, unchanged, idmap = self.relationship_actions(conn, "song2version", version_query, "version_id", versions)
                
            for r in removed:
                action_queue.append({"remove" : {"index" : "song2version", "id" : idmap.get(r)}})
            for n in new:
                nid = self.makeid()
                ns = {"id" : nid, "song_id" : id, "version_id" : n, "created_date" : esprit.util.now()}
                action_queue.append({"store" : { "index" : "song2version", "record" : ns, "id" : nid }})
        
        # if there are song references, then if this is a new record compare and
        # get the differential on the existing record.  Then action any removals and
        # additions
        if songs is not None:
            idmap = {}
            new, removed = songs, []
            if not isnew:
                songs_query = esprit.models.Query.term("song_ids.exact", id)
                new, removed, unchanged, idmap = self.relationship_actions(conn, "song2song", songs_query, "song_ids", songs, ignore_id=id)
                
            for r in removed:
                action_queue.append({"remove" : {"index" : "song2song", "id" : idmap.get(r)}})
            for n in new:
                nid = self.makeid()
                ns = {"id" : nid, "song_ids" : [n, id], "created_date" : esprit.util.now()}
                action_queue.append({"store" : { "index" : "song2song", "record" : ns, "id" : nid }})
        
        if len(song.keys()) > 1:
            # we only store the song metadata if there is more than just the id element
            if "created_date" not in song:
                song["created_date"] = esprit.util.now()
            song["last_updated"] = esprit.util.now()
            action_queue.append({"store" : {"index" : "song_store", "record" : song, "id" : id}})
        
        # now kick off all of the actions
        self.actions(conn, action_queue)
        
class VersionStoreDAO(LV_DAO):
    def save(self, host=None, port=None, index=None):
        # can we proceed with storage?
        version = self.data.get("version")
        if version is None:
            # version element must be present if only to access the id
            raise esprit.dao.StoreException("version element must be present")
        
        # sort out an id for the object to be stored
        id, isnew = self.prep_id(version)
        
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # extract the relational information we're interested in
        song = self.data.get("song")
        singer = self.data.get("singer")
        
        # we're going to compute all of the ES queries, and then execute them
        # together later
        action_queue = []
        
        # if there is a song reference, then if this is a new record compare and
        # get the differential on the existing record.  Then action any removals and
        # additions
        if song is not None:
            idmap = {}
            new, removed = [song], []
            if not isnew:
                song_query = esprit.models.Query.term("version_id.exact", id)
                new, removed, unchanged, idmap = self.relationship_actions(conn, "song2version", song_query, "song_id", [song])
                
            for r in removed:
                action_queue.append({"remove" : {"index" : "song2version", "id" : idmap.get(r)}})
            for n in new:
                nid = self.makeid()
                ns = {"id" : nid, "song_id" : n, "version_id" : id, "created_date" : esprit.util.now()}
                action_queue.append({"store" : { "index" : "song2version", "record" : ns, "id" : nid }})
        
        # if there is a singer reference, then if this is a new record compare and
        # get the differential on the existing record.  Then action any removals and
        # additions
        if singer is not None:
            idmap = {}
            new, removed = [singer], []
            if not isnew:
                singer_query = esprit.models.Query.term("version_id.exact", id)
                new, removed, unchanged, idmap = self.relationship_actions(conn, "singer2version", singer_query, "singer_id", [singer])
                
            for r in removed:
                action_queue.append({"remove" : {"index" : "singer2version", "id" : idmap.get(r)}})
            for n in new:
                nid = self.makeid()
                ns = {"id" : nid, "singer_id" : n, "version_id" : id, "created_date" : esprit.util.now()}
                action_queue.append({"store" : { "index" : "singer2version", "record" : ns, "id" : nid }})
        
        # we only store the version metadata if there is more than just the id element
        if len(version.keys()) > 1:
            if "created_date" not in version:
                version["created_date"] = esprit.util.now()
            version["last_updated"] = esprit.util.now()
            action_queue.append({"store" : {"index" : "version_store", "record" : version, "id" : id}})
        
        # now kick off all of the actions
        self.actions(conn, action_queue)

class SingerStoreDAO(LV_DAO):
    def save(self, host=None, port=None, index=None):
        # can we proceed with storage?
        singer = self.data.get("singer")
        if singer is None:
            # version element must be present if only to access the id
            raise esprit.dao.StoreException("singer element must be present")
        
        # sort out an id for the object to be stored
        id, isnew = self.prep_id(singer)
        
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # extract the relational information we're interested in
        versions = self.data.get("versions")
        
        # we're going to compute all of the ES queries, and then execute them
        # together later
        action_queue = []
        
        # if there is a song reference, then if this is a new record compare and
        # get the differential on the existing record.  Then action any removals and
        # additions
        if versions is not None:
            idmap = {}
            new, removed = versions, []
            if not isnew:
                versions_query = esprit.models.Query.term("singer_id.exact", id)
                new, removed, unchanged, idmap = self.relationship_actions(conn, "singer2version", versions_query, "version_id", versions)
                
            for r in removed:
                action_queue.append({"remove" : {"index" : "singer2version", "id" : idmap.get(r)}})
            for n in new:
                nid = self.makeid()
                ns = {"id" : nid, "singer_id" : id, "version_id" : n, "created_date" : esprit.util.now()}
                action_queue.append({"store" : { "index" : "singer2version", "record" : ns, "id" : nid }})
        
        # we only store the singer metadata if there is more than just the id element
        if len(singer.keys()) > 1:
            if "created_date" not in singer:
                singer["created_date"] = esprit.util.now()
            singer["last_updated"] = esprit.util.now()
            action_queue.append({"store" : {"index" : "singer_store", "record" : singer, "id" : id}})
        
        # now kick off all of the actions
        self.actions(conn, action_queue)

