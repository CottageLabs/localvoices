class LV(object):
    def __init__(self, raw=None):
        self.data = raw if raw is not None else {}

class Song(LV):
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
            locobj["lat"] = lat
        if lon is not None:
            locobj["lon"] = lon
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
    
class Version(LV):
    """
    {
        "version" : {
            "id" : "<opaque internal identifier>",
            "lv_id" : "<local voices identifier>",
            "title" : "<title of this version>",
            "alternative_title" : [<list of alternative titles>],
            "summary" : "<free text summary>",
            "language" : [<list of languages>],
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
            locobj["lat"] = lat
        if lon is not None:
            locobj["lon"] = lon
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
        self._append_version_property("reference", refobj)
    
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
    
class Singer(LV):
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
            "biography" : "<biographical summary>"
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
            locobj["lat"] = lat
        if lon is not None:
            locobj["lon"] = lon
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
