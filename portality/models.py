from portality import dao
from copy import deepcopy
from datetime import datetime
import string

unicode_punctuation_map = dict((ord(char), None) for char in string.punctuation)

class ModelException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LV(object):
    def __init__(self, raw=None):
        self.data = raw if raw is not None else {}

class Song(LV, dao.SongStoreDAO):
    """
    {
        "song" : {
            "id" : "<opaque internal identifier>",
            "lv_id" : "<local voices identifier>",
            "title" : "<canonical song title>",
            "summary" : "<free text summary>",
            "location": [
                {
                    "relation" : "<nature of song's relationship to place>",
                    "lat" : "<latitude>",
                    "lon" : "<longitude>",
                    "name" : "<textual name of place>"
                }
            ],
            "time_period" : {
                "from" : "<partial date>",
                "to" : "<partial date>"
            },
            "composer" : "<free text name of composer>",
            "created_date" : "<created date>",
            "last_updated" : "<last updated date>",
        },
        "versions" : [<list of ids>],
        "songs" : [<list of ids>]
    }
    """
    
    def _set_song_property(self, prop, val):
        if "song" not in self.data:
            self.data["song"] = {}
        self.data["song"][prop] = val
    
    def _append_song_property(self, prop, val):
        if "song" not in self.data:
            self.data["song"] = {}
        if prop not in self.data["song"]:
            self.data["song"][prop] = []
        self.data["song"][prop].append(val)
    
    def patch_song(self, new_song, replace_all=True, keep_id=True):
        # normalise the incoming singer document
        if "song" in new_song:
            new_song = new_song.get("song")
        
        # remember the id
        oid = None
        if keep_id:
            oid = self.id
        
        if replace_all:
            self.data["song"] = new_song
        else:
            raise NotImplementedError()
        
        if keep_id:
            self.id = oid
    
    @property
    def id(self):
        return self.data.get("song", {}).get("id")
    
    @id.setter
    def id(self, value):
        self._set_song_property("id", value)
    
    @property
    def lv_id(self):
        return self.data.get("song", {}).get("lv_id")
    
    @lv_id.setter
    def lv_id(self, value):
        self._set_song_property("lv_id", value)
    
    @property
    def title(self):
        return self.data.get("song", {}).get("title")
    
    @title.setter
    def title(self, value):
        self._set_song_property("title", value)
    
    @property
    def summary(self):
        return self.data.get("song", {}).get("summary")
    
    @summary.setter
    def summary(self, value):
        self._set_song_property("summary", value)
    
    @property
    def location(self):
        return self.data.get("song", {}).get("location", [])
    
    @location.setter
    def location(self, locobj):
        if not isinstance(locobj, list):
            locobj = [locobj]
        self._set_song_property("location", locobj)
    
    def add_location(self, relation=None, lat=None, lon=None, name=None):
        locobj = {}
        if relation is not None:
            locobj["relation"] = relation
        if lat is not None:
            locobj["lat"] = float(lat)
        if lon is not None:
            locobj["lon"] = float(lon)
        if name is not None:
            locobj["name"] = name
        if len(locobj.keys()) > 0:
            self._append_song_property("location", locobj)
    
    @property
    def time_period(self):
        return self.data.get("song", {}).get("time_period")
    
    @time_period.setter
    def time_period(self, value):
        self._set_song_property("time_period", value)
    
    def set_time_period(self, from_date, to_date=None):
        tobj = {"from" : from_date}
        if to_date is not None:
            tobj["to"] = to_date
        self.time_period = tobj
    
    @property
    def composer(self):
        return self.data.get("song", {}).get("composer")
    
    @composer.setter
    def composer(self, value):
        self._set_song_property("composer", value)
    
    @property
    def created_date(self):
        return self.data.get("song", {}).get("created_date")
    
    @created_date.setter
    def created_date(self, value):
        self._set_song_property("created_date", value)
        
    @property
    def last_updated(self):
        return self.data.get("song", {}).get("last_updated")
    
    @last_updated.setter
    def last_updated(self, value):
        self._set_song_property("last_updated", value)
    
    @property
    def versions(self):
        return self.data.get("versions", [])
    
    @versions.setter
    def versions(self, value):
        if not isinstance(value, list):
            value = [value]
        self.data["versions"] = value
    
    def add_version(self, version_id):
        if "versions" not in self.data:
            self.data["versions"] = []
        self.data["versions"].append(version_id)
    
    @property
    def songs(self):
        return self.data.get("songs", [])
    
    @songs.setter
    def songs(self, value):
        if not isinstance(value, list):
            value = [value]
        self.data["songs"] = value
    
    def add_song(self, song_id):
        if "songs" not in self.data:
            self.data["songs"] = []
        self.data["songs"].append(song_id)
    
    def get_alternative_titles(self):
        return super(Song, self).get_alternative_titles(self.versions)
    
class Version(LV, dao.VersionStoreDAO):
    """
    {
        "version" : {
            "id" : "<opaque internal identifier>",
            "lv_id" : "<local voices identifier>",
            "title" : "<title of this version>",
            "alternative_title" : [<list of alternative titles>],
            "summary" : "<free text summary>",
            "language" : [<list of languages>],
            "media_url" : [<list of media links>],
            "lyrics" : "<the lyrics of the version>",
            "photo_url" : "<a photo representing the version>",
            "collector" : "<free text name of collector>",
            "source" : "<free text source of material>",
            "collected_date" : "<datestamp of collection>",
            "location" : [
                {
                    "relation" : "<nature of song's relationship to place>",
                    "lat" : "<latitude>",
                    "lon" : "<longitude>",
                    "name" : "<textual name of place>"
                }
            ],
            "references" : [
                {
                    "type" : "<reference type, e.g. ROUD>",
                    "number" : "<reference number>"
                }
            ],
            "comments" : "<free text comments>",
            "tags" : [<list of tags>],
            "created_date" : "<created date>",
            "last_updated" : "<last updated date>",
        },
        "song" : "<the song this is a version of>",
        "singer" : "<the singer who performed this version>"
    }
    """
    
    def _set_version_property(self, prop, val):
        if "version" not in self.data:
            self.data["version"] = {}
        self.data["version"][prop] = val
    
    def _append_version_property(self, prop, val):
        if "version" not in self.data:
            self.data["version"] = {}
        if prop not in self.data["version"]:
            self.data["version"][prop] = []
        self.data["version"][prop].append(val)
    
    def patch_version(self, new_version, replace_all=True, keep_id=True):
        # normalise the incoming version document
        if "version" in new_version:
            new_version = new_version.get("version")
        
        # remember the id
        oid = None
        if keep_id:
            oid = self.id
        
        if replace_all:
            self.data["version"] = new_version
        else:
            raise NotImplementedError()
        
        if keep_id:
            self.id = oid
    
    @property
    def id(self):
        return self.data.get("version", {}).get("id")
    
    @id.setter
    def id(self, value):
        self._set_version_property("id", value)
    
    @property
    def lv_id(self):
        return self.data.get("version", {}).get("lv_id")
    
    @lv_id.setter
    def lv_id(self, value):
        self._set_version_property("lv_id", value)
    
    @property
    def title(self):
        return self.data.get("version", {}).get("title")
    
    @title.setter
    def title(self, value):
        self._set_version_property("title", value)
    
    @property
    def alternative_title(self):
        return self.data.get("version", {}).get("alternative_title", [])
    
    @alternative_title.setter
    def alternative_title(self, value):
        if not isinstance(value, list):
            value = [value]
        self._set_version_property("alternative_title", value)
    
    def add_alternative_title(self, value):
        self._append_version_property("alternative_title", value)
    
    @property
    def summary(self):
        return self.data.get("version", {}).get("summary")
    
    @summary.setter
    def summary(self, value):
        self._set_version_property("summary", value)
    
    @property
    def language(self):
        return self.data.get("version", {}).get("language", [])
    
    @language.setter
    def language(self, language):
        if not isinstance(language, list):
            language = [language]
        self._set_version_property("language", language)
    
    def add_language(self, language):
        self._append_version_property("language", language)
    
    @property
    def media_url(self):
        return self.data.get("version", {}).get("media_url", [])
    
    @media_url.setter
    def media_url(self, value):
        if not isinstance(value, list):
            value = [value]
        self._set_version_property("media_url", value)
    
    def add_media_url(self, value):
        self._append_version_property("media_url", value)
    
    @property
    def lyrics(self):
        return self.data.get("version", {}).get("lyrics")
    
    @lyrics.setter
    def lyrics(self, value):
        self._set_version_property("lyrics", value)
    
    @property
    def photo_url(self):
        return self.data.get("version", {}).get("photo_url")
    
    @photo_url.setter
    def photo_url(self, value):
        self._set_version_property("photo_url", value)
    
    @property
    def collector(self):
        return self.data.get("version", {}).get("collector")
    
    @collector.setter
    def collector(self, value):
        self._set_version_property("collector", value)
    
    @property
    def source(self):
        return self.data.get("version", {}).get("source")
    
    @source.setter
    def source(self, value):
        self._set_version_property("source", value)
    
    @property
    def collected_date(self):
        return self.data.get("version", {}).get("collected_date")
    
    @collected_date.setter
    def collected_date(self, value):
        self._set_version_property("collected_date", value)
    
    @property
    def location(self):
        return self.data.get("version", {}).get("location", [])
    
    @location.setter
    def location(self, locobj):
        if not isinstance(locobj, list):
            locobj = [locobj]
        self._set_version_property("location", locobj)
    
    def add_location(self, relation=None, lat=None, lon=None, name=None):
        locobj = {}
        if relation is not None:
            locobj["relation"] = relation
        if lat is not None:
            locobj["lat"] = float(lat)
        if lon is not None:
            locobj["lon"] = float(lon)
        if name is not None:
            locobj["name"] = name
        if len(locobj.keys()) > 0:
            self._append_version_property("location", locobj)
    
    @property
    def references(self):
        return self.data.get("version", {}).get("references", [])
    
    @references.setter
    def references(self, references):
        if not isinstance(references, list):
            references = [references]
        self._set_version_property("references", references)
    
    def add_reference(self, type, number):
        refobj = {"type" : type, "number" : number}
        self._append_version_property("references", refobj)
    
    @property
    def comments(self):
        return self.data.get("version", {}).get("comments")
    
    @comments.setter
    def comments(self, value):
        self._set_version_property("comments", value)
        
    @property
    def tags(self):
        return self.data.get("version", {}).get("tags", [])
    
    @tags.setter
    def tags(self, value):
        if not isinstance(value, list):
            value = [value]
        self._set_version_property("tags", value)
    
    def add_tag(self, value):
        self._append_version_property("tags", value)
     
    @property
    def created_date(self):
        return self.data.get("version", {}).get("created_date")
    
    @created_date.setter
    def created_date(self, value):
        self._set_version_property("created_date", value)
        
    @property
    def last_updated(self):
        return self.data.get("version", {}).get("last_updated")
    
    @last_updated.setter
    def last_updated(self, value):
        self._set_version_property("last_updated", value)
    
    @property
    def song(self):
        return self.data.get("song")
    
    @song.setter
    def song(self, song_id):
        self.data["song"] = song_id
    
    @property
    def singer(self):
        return self.data.get("singer")
    
    @singer.setter
    def singer(self, singer_id):
        self.data["singer"] = singer_id
    
class Singer(LV, dao.SingerStoreDAO):
    """
    {
        "singer" : {
            "id" : "<opaque internal identifier>",
            "lv_id" : "<local voices identifier>",
            "name" : {
                "first" : "<first name>",
                "middle" : "<middle name or initial>",
                "last" : "<surname>",
                "aka" : [<nicknames and translations>]
            },
            "groups" : [<list of bands/choirs>],
            "gender" : "<male|female>",
            "location" : [
                {
                    "relation" : "<nature of singers relationship to place>",
                    "lat" : "<latitude>",
                    "lon" : "<longitude>",
                    "name" : "<textual name of place>"
                }
            ]
            "born" : "<(partial) datestamp>",
            "died" : "<(partial) datestamp>",
            "biography" : "<biographical summary>",
            "source" : "<source of information about this singer>",
            "photo_url" : "<url for singer's photo>",
            "created_date" : "<created date>",
            "last_updated" : "<last updated date>",
        },
        "versions" : [<list of version identifiers>]
    }
    """
    
    def _set_singer_property(self, prop, val):
        if "singer" not in self.data:
            self.data["singer"] = {}
        self.data["singer"][prop] = val
    
    def _append_singer_property(self, prop, val):
        if "singer" not in self.data:
            self.data["singer"] = {}
        if prop not in self.data["singer"]:
            self.data["singer"][prop] = []
        self.data["singer"][prop].append(val)
    
    @property
    def id(self):
        return self.data.get("singer", {}).get("id")
    
    @id.setter
    def id(self, value):
        self._set_singer_property("id", value)
    
    def patch_singer(self, new_singer, replace_all=True, keep_id=True):
        # normalise the incoming singer document
        if "singer" in new_singer:
            new_singer = new_singer.get("singer")
        
        # remember the id
        oid = None
        if keep_id:
            oid = self.id
        
        if replace_all:
            self.data["singer"] = new_singer
        else:
            raise NotImplementedError()
        
        if keep_id:
            self.id = oid
    
    @property
    def lv_id(self):
        return self.data.get("singer", {}).get("lv_id")
    
    @lv_id.setter
    def lv_id(self, value):
        self._set_singer_property("lv_id", value)
    
    @property
    def name(self):
        return self.data.get("singer", {}).get("name")
    
    @name.setter
    def name(self, nameobj):
        self._set_singer_property("name", nameobj)
    
    def set_name(self, first=None, middle=None, last=None, aka=None):
        nameobj = {}
        if first is not None:
            nameobj["first"] = first
        if middle is not None:
            nameobj["middle"] = middle
        if last is not None:
            nameobj["last"] = last
        if aka is not None:
            if not isinstance(aka, list):
                aka = [aka]
            nameobj["aka"] = aka
        if len(nameobj.keys()) > 0:
            self.name = nameobj
    
    def add_aka(self, aka):
        if "singer" not in self.data:
            self.data["singer"] = {}
        if "name" not in self.data["singer"]:
            self.data["singer"]["name"] = {}
        if "aka" not in self.data["singer"]["name"]:
            self.data["singer"]["name"]["aka"] = []
        self.data["singer"]["name"]["aka"].append(aka)
    
    @property
    def groups(self):
        return self.data.get("singer", {}).get("groups", [])
    
    @groups.setter
    def groups(self, value):
        if not isinstance(value, list):
            value = [value]
        self._set_singer_property("groups", value)
    
    def add_group(self, value):
        self._append_singer_property("groups", value)
    
    @property
    def gender(self):
        return self.data.get("singer", {}).get("gender")
    
    @gender.setter
    def gender(self, value):
        self._set_singer_property("gender", value)
    
    @property
    def location(self):
        return self.data.get("singer", {}).get("location", [])
    
    @location.setter
    def location(self, locobj):
        if not isinstance(locobj, list):
            locobj = [locobj]
        self._set_singer_property("location", locobj)
    
    def add_location(self, relation=None, lat=None, lon=None, name=None):
        locobj = {}
        if relation is not None:
            locobj["relation"] = relation
        if lat is not None:
            locobj["lat"] = float(lat)
        if lon is not None:
            locobj["lon"] = float(lon)
        if name is not None:
            locobj["name"] = name
        if len(locobj.keys()) > 0:
            self._append_singer_property("location", locobj)
    
    @property
    def born(self):
        return self.data.get("singer", {}).get("born")
    
    @born.setter
    def born(self, value):
        self._set_singer_property("born", value)
    
    @property
    def died(self):
        return self.data.get("singer", {}).get("died")
    
    @died.setter
    def died(self, value):
        self._set_singer_property("died", value)
    
    @property
    def biography(self):
        return self.data.get("singer", {}).get("biography")
    
    @biography.setter
    def biography(self, value):
        self._set_singer_property("biography", value)
    
    @property
    def photo_url(self):
        return self.data.get("singer", {}).get("photo_url")
    
    @photo_url.setter
    def photo_url(self, value):
        self._set_singer_property("photo_url", value)
    
    @property
    def source(self):
        return self.data.get("singer", {}).get("source")
    
    @source.setter
    def source(self, value):
        self._set_singer_property("source", value)
    
    @property
    def created_date(self):
        return self.data.get("singer", {}).get("created_date")
    
    @created_date.setter
    def created_date(self, value):
        self._set_singer_property("created_date", value)
        
    @property
    def last_updated(self):
        return self.data.get("singer", {}).get("last_updated")
    
    @last_updated.setter
    def last_updated(self, value):
        self._set_singer_property("last_updated", value)
    
    @property
    def versions(self):
        return self.data.get("versions", [])
    
    @versions.setter
    def versions(self, value):
        if not isinstance(value, list):
            value = [value]
        self.data["versions"] = value
    
    def add_version(self, version_id):
        if "versions" not in self.data:
            self.data["versions"] = []
        self.data["versions"].append(version_id)



class LV_Index(object):
    # relations, in order of preference of canonical
    # FIXME: we don't know what these relationships are yet
    location_relations = ["main", "native_area", "significant"]

    def canonicalise_location(self, locations):
        loc = self._select_location(locations)
        if loc is None: return None
        cl = {"lat" : float(loc.get("lat")), "lon" : float(loc.get("lon"))}
        return cl
    
    def _select_location(self, locations):
        # if no locations then no location to select
        if len(locations) == 0: return None
        
        # if exactly one location, if it meets the criteria, use it
        if len(locations) == 1:
            if self._validate_location(locations[0]):
                return locations[0]
            else:
                return None
        
        # we have multiple locations, so we need to choose between them
        # start by pulling out the relations
        reld = {}
        for loc in locations:
            rel = loc.get("relation")
            if rel is not None:
                reld[rel] = loc
        
        # go through the relations in preferred order, returning the first hit which meets the criteria
        for r in self.location_relations:
            if r in reld:
                if self._validate_location(reld[r]):
                    return reld[r]
        
        # if we get here, just return the first one with a relationship which meets the criteria
        for r, loc in reld.iteritems():
            if self._validate_location(loc):
                return loc
        
        # if we don't have any with relations which validate, go through all of them and return the first one which does
        for loc in locations:
            if self._validate_location(loc):
                return loc
        
        # we have failed :(
        return None
        
    def _validate_location(self, location):
        return "lat" in location and "lon" in location
    
    def canonicalise_name(self, name_object):
        first = name_object.get("first", "")
        middle = name_object.get("middle", "")
        last = name_object.get("last", "")
        if middle != "": first += " "
        if last != "": middle += " "
        name = first + middle + last
        if name != "":
            return name
        return None
    
    def order_by_name(self, name_object):
        first = name_object.get("first", "")
        middle = name_object.get("middle", "")
        last = name_object.get("last", "")
        name = " ".join([last, middle, first])
        name = self._normalise_name_string(name)
        if name != "":
            return name
        return None
    
    def _normalise_name_string(self, s):
        if type(s) == "str":
            s = s.translate(string.maketrans("",""), string.punctuation)
        elif type(s) == "unicode":
            s = s.translate(unicode_punctuation_map)
        s = s.lower().replace(" ", "_")
        return s
    
    def canonicalise_group(self, groups):
        # all we can really do is return the first group
        if len(groups) > 0:
            return groups[0]
        return None
    
    def expand_date_partial(self, partial):
        try:
            return datetime.strptime(partial, "%Y").isoformat().split("T")[0]
        except: pass
        
        try:
            return datetime.strptime(partial, "%Y-%m").isoformat().split("T")[0]
        except: pass
        
        try:
            return datetime.strptime(partial, "%Y-%m-%d").isoformat().split("T")[0]
        except: pass
        return None

class VersionIndex(LV_Index, dao.VersionIndexDAO):

    @classmethod
    def by_id(cls, version_id, cascade=True):
        # get the original version
        version = Version().get(version_id, links=True)
        if version is None:
            return
        
        # generate the version index
        vi = VersionIndex.from_version(version)
        vi.save()
        
        if not cascade:
            return
        
        if version.singer is not None:
            singer = Singer().get(version.singer, links=True)
            if singer is not None:
                si = SingerIndex.from_singer(singer)
                si.save()
        
        if version.song is not None:
            song = Song().get(version.song, links=True)
            if song is not None:
                si = SongIndex.from_song(song)
                si.save()
    
    @classmethod
    def delete_by_id(cls, version_id, cascade=True):
        vi = VersionIndex.pull(version_id)
        if vi is None:
            return
        
        if vi.data.get("singer") is not None:
            singer = Singer().get(vi.data.get("singer", {}).get("id"), links=True)
            if singer is not None:
                si = SingerIndex.from_singer(singer)
                si.save()
        
        if vi.data.get("song") is not None:
            song = Song().get(vi.data.get("song", {}).get("id"), links=True)
            if song is not None:
                si = SongIndex.from_song(song)
                si.save()
        
        vi.delete()

    @classmethod
    def from_version(cls, version):
        # make a copy of the core version object and wrap the versionindex around it
        v = version.data.get("version")
        if v is None:
            raise ModelException("for versionindex to be made from_version, version object must contain a version!")
        vi = cls(deepcopy(v))
        
        # if the version has a location, canonicalise it
        vloc = version.location
        if vloc is not None and len(vloc) > 0:
            vl = vi.canonicalise_location(vloc)
            if vl is not None:
                vi.data["canonical_location"] = vl
        
        # if the version has a singer, add their record
        if version.singer is not None:
            singer_object = Singer().get(version.singer)
            singer = singer_object.data.get("singer")
            
            # canonicalise the singer or group's name
            if singer_object.name is not None:
                # singer name takes priority over group name
                canonname = vi.canonicalise_name(singer_object.name)
                singer["canonical_name"] = canonname
            elif singer_object.groups is not None and len(singer_object.groups) > 0:
                # if there's no singer name, use the group name
                canonname = vi.canonicalise_group(singer_object.groups)
                singer["canonical_name"] = canonname
            
            # canonicalise the singer's location
            if singer_object.location is not None and len(singer_object.location) > 0:
                sloc = vi.canonicalise_location(singer_object.location)
                if sloc is not None:
                    singer["canonical_location"] = sloc
            
            # expand the born and died dates
            if singer_object.born is not None:
                expanded = vi.expand_date_partial(singer_object.born)
                singer["born_date"] = expanded
            if singer_object.died is not None:
                expanded = vi.expand_date_partial(singer_object.died)
                singer["died_date"] = expanded
            
            vi.data["singer"] = singer
        
        # if the version has a song, add its record
        if version.song is not None:
            song_object = Song().get(version.song, links=True)
            song = song_object.data.get("song")
            
            # canonicalise the song location
            loc = song_object.location
            if loc is not None and len(loc) > 0:
                cl = vi.canonicalise_location(loc)
                if cl is not None:
                    song["canonical_location"] = cl
            
            # finally get all the alternative titles of the song
            alts = song_object.get_alternative_titles()
            song["alternative_title"] = alts
            
            # add to the version
            vi.data["song"] = song
        
        return vi

class SingerIndex(LV_Index, dao.SingerIndexDAO):
    
    @classmethod
    def by_id(cls, singer_id, cascade=True):
        # get the original singer
        singer = Singer().get(singer_id, links=True)
        if singer is None:
            return
        
        # generate the singer index
        si = SingerIndex.from_singer(singer)
        si.save()
        
        if not cascade:
            return
        
        # for each version regenerate the version index
        for v in singer.versions:
            version = Version().get(v, links=True)
            if version is not None:
                vi = VersionIndex.from_version(version)
                vi.save()
            
            # regenerate the song index
            if version.song is not None:
                song = Song().get(version.song, links=True)
                if song is not None:
                    soi = SongIndex.from_song(song)
                    soi.save()
    
    @classmethod
    def delete_by_id(cls, singer_id, cascade=True):
        si = SingerIndex.pull(singer_id)
        if si is None:
            return
        
        for v in si.data.get("versions"):
            version = Version().get(v.get("id"), links=True)
            if version is not None:
                vi = VersionIndex.from_version(version)
                vi.save()
            
            if version.get("song") is not None:
                song = Song().get(version.get("song", {}).get("id"), links=True)
                if song is not None:
                    soi = SongIndex.from_song(song)
                    soi.save()
            
        si.delete()
        
    @classmethod
    def from_singer(cls, singer):
        # make a copy of the core singer object and wrap the singerindex around it
        s = singer.data.get("singer")
        if s is None:
            raise ModelException("for singerindex to be made from_singer, singer object must contain a singer!")
        si = cls(deepcopy(s))
        
        # canonicalise the singer or group's name
        if singer.name is not None:
            # singer name takes priority over group name
            canonname = si.canonicalise_name(singer.name)
            si.data["canonical_name"] = canonname
        elif singer.groups is not None and len(singer.groups) > 0:
            # if there's no singer name, use the group name
            canonname = si.canonicalise_group(singer.groups)
            si.data["canonical_name"] = canonname
        
        # sort out the order_by_name field for alphabetical sorting
        if singer.name is not None:
            order_by = si.order_by_name(singer.name)
            si.data["order_by_name"] = order_by
        
        # canonicalise the singer's location
        if singer.location is not None and len(singer.location) > 0:
            sloc = si.canonicalise_location(singer.location)
            if sloc is not None:
                si.data["canonical_location"] = sloc
        
        # expand the born and died dates
        if singer.born is not None:
            expanded = si.expand_date_partial(singer.born)
            si.data["born_date"] = expanded
        if singer.died is not None:
            expanded = si.expand_date_partial(singer.died)
            si.data["died_date"] = expanded
        
        # obtain all of the versions by this singer
        si.data["versions"] = []
        related_version_ids = singer.versions
        if related_version_ids is not None and len(related_version_ids) > 0:
            related_versions = Version().get_all(related_version_ids, links=True)
            for v in related_versions:
                version = v.data.get("version")
                
                # if the version has a location, canonicalise it
                vloc = v.location
                if vloc is not None and len(vloc) > 0:
                    vl = si.canonicalise_location(vloc)
                    if vl is not None:
                        version["canonical_location"] = vl
                
                # if the version has a song, add it to the record
                if v.song is not None:
                    song_object = Song().get(v.song, links=True)
                    song = song_object.data.get("song")
                    
                    # canonicalise the song location
                    loc = song_object.location
                    if loc is not None and len(loc) > 0:
                        cl = si.canonicalise_location(loc)
                        if cl is not None:
                            song["canonical_location"] = cl
                    
                    # finally get all the alternative titles of the song
                    alts = song_object.get_alternative_titles()
                    song["alternative_title"] = alts
                    
                    # add to the version
                    version["song"] = song
                
                # add to the singer
                si.data["versions"].append(version)
        
        return si
        
        
class SongIndex(LV_Index, dao.SongIndexDAO):
    
    @classmethod
    def by_id(cls, song_id, cascade=True):
        # get the original song
        song = Song().get(song_id, links=True)
        if song is None:
            return
        
        print song.data
        
        # generate the singer index
        si = SongIndex.from_song(song)
        print si.data
        si.save()
        
        if not cascade:
            return
        
        # for each version regenerate the version index
        for v in song.versions:
            version = Version().get(v, links=True)
            if version is not None:
                vi = VersionIndex.from_version(version)
                vi.save()
                
                # regenerate the singer index
                if version.singer is not None:
                    singer = Singer().get(version.singer, links=True)
                    if singer is not None:
                        soi = SingerIndex.from_singer(singer)
                        soi.save()
        
        # for each related song, regenerate its index
        for s in song.songs:
            relsong = Song().get(s, links=True)
            if relsong is not None:
                ri = SongIndex.from_song(relsong)
                ri.save()
    
    @classmethod
    def delete_by_id(cls, song_id, cascade=True):
        si = SongIndex.pull(song_id)
        if si is None:
            return
        
        # refresh the indexes of related songs
        for rel in si.data.get("relations", []):
            rs = Song().get(rel.get("id"))
            if rs is not None:
                ri = SongIndex.from_song(s)
                ri.save()
        
        # deleting a song deletes all the versions, so we need
        # to call delete by id on each version too
        for v in si.data.get("versions", []):
            VersionIndex.delete_by_id(v.get("id"))
        
        si.delete()
    
    @classmethod
    def from_song(cls, song):
        # make a copy of the core song object and wrap the songindex around it
        s = song.data.get("song")
        if s is None:
            raise ModelException("for songindex to be made from_song, song object must contain a song!")
        si = cls(deepcopy(s))
        
        # canonicalise the location
        loc = song.location
        if loc is not None and len(loc) > 0:
            cl = si.canonicalise_location(loc)
            if cl is not None:
                si.data["canonical_location"] = cl
        
        # attach basic metadata about all the related songs
        related_song_ids = song.data.get("songs")
        if related_song_ids is not None and len(related_song_ids) > 0:
            related_songs = song.get_all(related_song_ids)
            relations = [{"id" : s.id, "title": s.title} for s in related_songs]
            si.data["relations"] = relations
        
        # obtain all of the versions of this song
        related_version_ids = song.data.get("versions")
        if related_version_ids is not None and len(related_version_ids) > 0:
            related_versions = Version().get_all(related_version_ids, links=True)
            
            # obtain the aggregate list of alternative titles and references from the versions
            alt_titles = []
            refs = []
            ref_index = []
            for v in related_versions:
                # record the titles (we'll de-duplicate later)
                alt_titles.append(v.title)
                alt_titles += v.alternative_title
                
                # record all the unique references
                for ref in v.references:
                    canon = ref.get("type") + ":" + ref.get("number")
                    if canon not in ref_index:
                        ref_index.append(canon)
                        refs.append(ref)
            
            # deduplicate the titles
            alt_titles = list(set(alt_titles))
            
            # add the aggregate information
            si.data["alternative_title"] = alt_titles
            si.data["references"] = refs
            
            # now add each of the versions as a whole to the document, calculating their singer at the same time
            si.data["versions"] = []
            for v in related_versions:
                version = v.data.get("version")
                
                # if the version has a location, canonicalise it
                vloc = v.location
                if vloc is not None and len(vloc) > 0:
                    vl = si.canonicalise_location(vloc)
                    if vl is not None:
                        version["canonical_location"] = vl
                
                # if the version has a singer, enhance the record and then add it to the version
                if v.singer:
                    singer_object = Singer().get(v.singer)
                    singer = singer_object.data.get("singer")
                    
                    # canonicalise the singer or group's name
                    if singer_object.name is not None:
                        # singer name takes priority over group name
                        canonname = si.canonicalise_name(singer_object.name)
                        singer["canonical_name"] = canonname
                    elif singer_object.groups is not None and len(singer_object.groups) > 0:
                        # if there's no singer name, use the group name
                        canonname = si.canonicalise_group(singer_object.groups)
                        singer["canonical_name"] = canonname
                    
                    # canonicalise the singer's location
                    if singer_object.location is not None and len(singer_object.location) > 0:
                        sloc = si.canonicalise_location(singer_object.location)
                        if sloc is not None:
                            singer["canonical_location"] = sloc
                    
                    # expand the born and died dates
                    if singer_object.born is not None:
                        expanded = si.expand_date_partial(singer_object.born)
                        singer["born_date"] = expanded
                    if singer_object.died is not None:
                        expanded = si.expand_date_partial(singer_object.died)
                        singer["died_date"] = expanded
                    
                    version["singer"] = singer
                
                si.data["versions"].append(version)
        
        return si

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
