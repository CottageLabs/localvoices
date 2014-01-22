import esprit
from portality.core import app
from copy import deepcopy

class LV_DAO(esprit.dao.DAO):

    @classmethod
    def initialise_index(cls, host=None, port=None, index=None, mappings=None):
        # get the connection and the mapping based on the context
        conn = LV_DAO().make_es_connection(host, port, index)
        mappings = app.config["MAPPINGS"] if mappings is None else mappings
        
        if not esprit.raw.index_exists(conn):
            print "Creating Index; host:" + str(conn.host) + " port:" + str(conn.port) + " db:" + str(conn.index)
            esprit.raw.create_index(conn)
        for key, mapping in mappings.iteritems():
            if not esprit.raw.has_mapping(conn, key):
                r = esprit.raw.put_mapping(conn, key, mapping)
                print key, r.status_code

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

    def get(self, id, links=False, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # execute a multi get against the index
        resp = esprit.raw.get(conn, "song_store", id)
        obj = esprit.raw.unpack_get(resp)
        if obj is None:
            return None
        obj = self.__class__({"song" : obj})
        
        if links:
            song_query = esprit.models.Query.term_filter("song_ids.exact", id)
            version_query = esprit.models.Query.term_filter("song_id.exact", id)
            
            song_resp = esprit.raw.search(conn, "song2song", song_query)
            song_links = esprit.raw.unpack_result(song_resp)
            
            version_resp = esprit.raw.search(conn, "song2version", version_query)
            version_links = esprit.raw.unpack_result(version_resp)
            
            for l in song_links:
                other = [x for x in l.get("song_ids") if x != id][0]
                obj.add_song(other)
            
            for l in version_links:
                obj.add_version(l.get("version_id"))
        
        return obj

    def get_all(self, ids, links=False, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # execute a multi get against the index
        resp = esprit.raw.mget(conn, "song_store", ids)
        objects = esprit.raw.unpack_mget(resp)
        objects = [self.__class__({"song" : o}) for o in objects]
        
        if links:
            # TODO: query the index for all relations which match the
            # various song ids, and then reconstruct the objects in memory
            pass
        
        return objects

    def save(self, host=None, port=None, index=None, refresh=False):
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
        
        # call a refresh if needed
        if refresh:
            esprit.raw.refresh(conn)
    
    def remove(self, host=None, port=None, index=None):
        # can we delete?
        song = self.data.get("song")
        if song is None:
            # song element must be present if only to access the id
            raise esprit.dao.StoreException("song element must be present")
        if "id" not in song:
            # id element must be present in order to do delete
            raise esprit.dao.StoreException("song element must have id in order to be deleted")
        
        id = song.get("id")
        
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # we're going to compute all of the ES queries, and then execute them
        # together later
        action_queue = []
        
        # issue delete-by-query on the join tables
        version_query = esprit.models.Query.term("song_id.exact", id)
        action_queue.append({"remove" : {"index" : "song2version", "query" : version_query}})
        
        songs_query = esprit.models.Query.term("song_ids.exact", id)
        action_queue.append({"remove" : {"index" : "song2song", "query" : songs_query}})
        
        # issue delete on the song id
        action_queue.append({"remove" : {"index" : "song_store", "id" : id}})
        
        # now kick off all of the actions
        self.actions(conn, action_queue)
    
    def get_alternative_titles(self, version_ids, host=None, port=None, index=None):
        title_docs = VersionStoreDAO().get_fields_for_all(version_ids, fields=["alternative_title.exact", "title.exact"])
        alts = [t.get("alternative_title.exact") for t in title_docs if t is not None and t.get("alternative_title.exact") is not None]
        titles = [t.get("title.exact") for t in title_docs if t is not None and t.get("title.exact") is not None]
        return list(set(alts + titles))
    
class VersionStoreDAO(LV_DAO):

    def get_fields_for_all(self, ids, fields, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        result = esprit.raw.mget(conn, "version_store", ids, fields)
        docs = esprit.raw.unpack_mget(result)
        return docs
    
    def get(self, id, links=False, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # execute a multi get against the index
        resp = esprit.raw.get(conn, "version_store", id)
        obj = esprit.raw.unpack_get(resp)
        if obj is None:
            return None
        obj = self.__class__({"version" : obj})
        
        if links:
            singer_query = esprit.models.Query.term_filter("version_id.exact", id)
            singer_resp = esprit.raw.search(conn, "singer2version", singer_query)
            singer_links = esprit.raw.unpack_result(singer_resp)
            if len(singer_links) > 0:
                obj.singer = singer_links[0].get("singer_id")
            
            song_query = esprit.models.Query.term_filter("version_id.exact", id)
            song_resp = esprit.raw.search(conn, "song2version", song_query)
            song_links = esprit.raw.unpack_result(song_resp)
            if len(song_links) > 0:
                obj.song = song_links[0].get("song_id")
        
        return obj
    
    def get_all(self, ids, links=False, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # execute a multi get against the index
        resp = esprit.raw.mget(conn, "version_store", ids)
        objects = esprit.raw.unpack_mget(resp)
        objects = [self.__class__({"version" : o}) for o in objects]
        
        if links:
            song_query = esprit.models.Query.terms_filter("version_id.exact", ids)
            singer_query = esprit.models.Query.terms_filter("version_id.exact", ids)
            
            song_resp = esprit.raw.search(conn, "song2version", song_query)
            song_links = esprit.raw.unpack_result(song_resp)
            
            singer_resp = esprit.raw.search(conn, "singer2version", singer_query)
            singer_links = esprit.raw.unpack_result(singer_resp)
            
            # for each object, find its links and attach them
            for o in objects:
                for l in song_links:
                    if l.get("version_id") == o.id:
                        o.song = l.get("song_id")
                for l in singer_links:
                    if l.get("version_id") == o.id:
                        o.singer = l.get("singer_id")
        
        return objects

    def save(self, host=None, port=None, index=None, refresh=False):
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
        
        # call a refresh if needed
        if refresh:
            esprit.raw.refresh(conn)

    def remove(self, host=None, port=None, index=None):
        # can we delete?
        version = self.data.get("version")
        if version is None:
            # version element must be present if only to access the id
            raise esprit.dao.StoreException("version element must be present")
        if "id" not in version:
            # id element must be present in order to do delete
            raise esprit.dao.StoreException("version element must have id in order to be deleted")
        
        id = version.get("id")
        
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # we're going to compute all of the ES queries, and then execute them
        # together later
        action_queue = []
        
        # issue delete-by-query on the join tables
        song_query = esprit.models.Query.term("version_id.exact", id)
        action_queue.append({"remove" : {"index" : "song2version", "query" : song_query}})
        
        singer_query = esprit.models.Query.term("version_id.exact", id)
        action_queue.append({"remove" : {"index" : "singer2version", "query" : singer_query}})
        
        # issue delete on the song id
        action_queue.append({"remove" : {"index" : "version_store", "id" : id}})
        
        # now kick off all of the actions
        self.actions(conn, action_queue)

class SingerStoreDAO(LV_DAO):

    def get(self, id, links=False, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # execute a multi get against the index
        resp = esprit.raw.get(conn, "singer_store", id)
        obj = esprit.raw.unpack_get(resp)
        if obj is None:
            return None
        obj = self.__class__({"singer" : obj})
        
        if links:
            version_query = esprit.models.Query.term_filter("singer_id.exact", id)
            version_resp = esprit.raw.search(conn, "singer2version", version_query)
            version_links = esprit.raw.unpack_result(version_resp)
            
            for l in version_links:
                obj.add_version(l.get("version_id"))
        
        return obj

    def save(self, host=None, port=None, index=None, refresh=False):
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
        
        # call a refresh if needed
        if refresh:
            esprit.raw.refresh(conn)

    def remove(self, host=None, port=None, index=None):
        # can we delete?
        singer = self.data.get("singer")
        if singer is None:
            # singer element must be present if only to access the id
            raise esprit.dao.StoreException("singer element must be present")
        if "id" not in singer:
            # id element must be present in order to do delete
            raise esprit.dao.StoreException("singer element must have id in order to be deleted")
        
        id = singer.get("id")
        
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # we're going to compute all of the ES queries, and then execute them
        # together later
        action_queue = []
        
        # issue delete-by-query on the join tables
        versions_query = esprit.models.Query.term("singer_id.exact", id)
        action_queue.append({"remove" : {"index" : "singer2version", "query" : versions_query}})
        
        # issue delete on the song id
        action_queue.append({"remove" : {"index" : "singer_store", "id" : id}})
        
        # now kick off all of the actions
        self.actions(conn, action_queue)

class SongIndexDAO(esprit.dao.DomainObject):
    __type__ = "song"
    __conn__ = esprit.raw.Connection(app.config['ELASTIC_SEARCH_HOST'], app.config['ELASTIC_SEARCH_DB'])
    
    def save(self, conn=None):
        super(SongIndexDAO, self).save(conn=conn, updated=False, created=False)

class SingerIndexDAO(esprit.dao.DomainObject):
    __type__ = "singer"
    __conn__ = esprit.raw.Connection(app.config['ELASTIC_SEARCH_HOST'], app.config['ELASTIC_SEARCH_DB'])
    
    def save(self, conn=None):
        super(SingerIndexDAO, self).save(conn=conn, updated=False, created=False)

class VersionIndexDAO(esprit.dao.DomainObject):
    __type__ = "version"
    __conn__ = esprit.raw.Connection(app.config['ELASTIC_SEARCH_HOST'], app.config['ELASTIC_SEARCH_DB'])
    
    def save(self, conn=None):
        super(VersionIndexDAO, self).save(conn=conn, updated=False, created=False)

class Search(LV_DAO):
    def search(self, types, query, transpose_type=True, host=None, port=None, index=None):
        # create a connection to the ES server
        conn = self.make_es_connection(host, port, index)
        
        # do the query on the selected types
        resp = esprit.raw.search(conn, types, query)
        
        records = []
        if transpose_type:
            # we want to unpack and also transpose the _type into the object for the caller to distinguish between
            # the different kinds of objects
            j = resp.json()
            for i in j.get('hits', {}).get('hits', []):
                record = i.get("_source", {})
                t = i.get("_type")
                record["_type"] = t
                records.append(record)
                
        else:
            # otherwise, let esprit deal with it
            records = esprit.raw.unpack_result(resp)
        
        return records

class SearchQuery(object):
    _filtered_query = {
        "query" : {
            "filtered" : {
                "query" : {"match_all" : {}}
            }
        }
    }
    
    _bool_filter = { 
        "filter" : {
            "bool" : {}
        }
    }
    
    _geo_bounding_box_container = {"geo_bounding_box" : { "canonical_location" : {} }} # "canonical_location" : _geo_bounding_box
    _geo_bounding_box = {"top_left" : {"lat" : 0, "lon": 0}, "bottom_right" : {"lat" : 0, "lon" : 0}}
    _query_string = {"query_string" : { "query" : "<query string>", "default_operator" : "OR"}}
    
    _locations = [
        "location.name",
        "versions.location.name",
        "versions.singer.location.name",
        "versions.song.location.name",
        "singer.location.name",
        "song.location.name"
    ]
    
    def __init__(self):
        self.box = None
        self.place = None
        self.place_analysed = None
        self.text = None
        self.text_analysed = None

    def bounding_box(self, from_lat, to_lat, from_lon, to_lon):
        if self.box is None:
            self.box = {}
        self.box["from_lat"] = from_lat
        self.box["to_lat"] = to_lat
        self.box["from_lon"] = from_lon
        self.box["to_lon"] = to_lon
        
    def place_query(self, place):
        self.place = place
        self.place_analysed = esprit.models.Query.tokenise(place)
    
    def text_query(self, text_query):
        self.text = text_query
        self.text_analysed = esprit.models.Query.tokenise(text_query)
    
    def query(self):
        q = deepcopy(self._filtered_query)
        
        if self.box is not None or self.place is not None:
            if "filter" not in q["query"]["filtered"]:
                q["query"]["filtered"].update(deepcopy(self._bool_filter))
        
        if self.box is not None:
            b = deepcopy(self._geo_bounding_box)
            b["top_left"]["lat"] = self.box['from_lat']
            b["top_left"]["lon"] = self.box['from_lon']
            b["bottom_right"]["lat"] = self.box['to_lat']
            b["bottom_right"]["lon"] = self.box['to_lon']
            gbb = deepcopy(self._geo_bounding_box_container)
            gbb["geo_bounding_box"]["canonical_location"] = b
            
            q["query"]["filtered"]["filter"]["bool"]["must"] = []
            q["query"]["filtered"]["filter"]["bool"]["must"].append(gbb)
        
        if self.text is not None:
            qa = deepcopy(self._query_string)
            qa["query_string"]["query"] = " ".join(self.text_analysed)
            q["query"]["filtered"]["query"] = qa
        
        if self.place is not None:
            shoulds = []
            for p in self.place_analysed:
                for l in self._locations:
                    shoulds.append({"term" : {l : p}})
            q["query"]["filtered"]["filter"]["bool"]["should"] = shoulds
        
        return q
    
class ListSingersQuery(object):
    _base_query = {
        "fields" : ["id", "canonical_name"],
        "script_fields" : { "version_count" : {"script" : "doc['versions.id'].values.length"} },
        "query" : {
            "match_all" : {}
        },
        "size" : 50,
        "sort" : [{"order_by_name.exact" : {"order" : "asc"}}]
    }
    
    _from = {"from" : 0}
    _query_string = {"query_string" : { "query" : "<query string>"}}
    
    _all_results = 10000
    
    def __init__(self):
        self.from_number = None
        self.size = 50
        self.initial_letters = None
        self.order = "asc"
    
    def set_from(self, fr):
        self.from_number = fr
    
    def set_size(self, size):
        self.size = size
    
    def all_results(self):
        self.size = self._all_results
    
    def set_initial_letters(self, letters):
        self.initial_letters = letters
    
    def set_order(self, order):
        self.order = order
    
    def query(self):
        q = deepcopy(self._base_query)
        
        if self.from_number is not None:
            f = deepcopy(self._from)
            f["from"] = self.from_number
            q.update(f)
        
        if self.size is not None:
            q["size"] = self.size
        
        if self.order.lower() in ["asc", "desc"]:
            q["sort"][0]["order_by_name.exact"]["order"] = self.order.lower()
        
        if self.initial_letters is not None:
            qs = deepcopy(self._query_string)
            qs["query_string"]["query"] = "order_by_name:" + self.initial_letters.lower() + "*"
            q["query"] = qs
        
        return q
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
