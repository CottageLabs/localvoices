from portality.dao import SearchQuery, ListSingersQuery, Search
from portality.models import SingerIndex, SongIndex, VersionIndex, Singer, Song, Version

class SearchResult(object):
    def __init__(self, result_objects, from_number, page_size, total):
        self.result_objects = result_objects
        self.from_number = from_number
        self.page_size = page_size
        self.total = total
    
    def as_dict(self):
        return {
            "from" : int(self.from_number),
            "size" : int(self.page_size),
            "count" : len(self.result_objects),
            "total" : int(self.total),
            "results" : self.result_objects
        }

class NotFoundException(Exception):
    pass

class LocalVoicesAPI(object):
    
    @classmethod
    def search(cls, types, from_lat=None, to_lat=None, from_lon=None, to_lon=None, place=None, query_string=None, from_number=0, page_size=25):
        """
        types - one or more of "singer", "song", "version" in a list
        from_lat - upper-most latitude for search results
        to_lat - lower-most latitude for search results
        from_lon - left-most longitude for search results
        to_lon - right-most longitude for search results
        place - placename to search for
        query_string - free-text query string
        from_number - result number to start from
        page_size - number of results to return
        """
        
        # sanitise the types
        types = ["song", "singer", "version"] if types is None else types if isinstance(types, list) else [types]
        
        # build the query
        q = SearchQuery()
        if from_lat is not None and to_lat is not None and from_lon is not None and to_lon is not None:
            q.bounding_box(from_lat, to_lat, from_lon, to_lon)
        if place is not None:
            q.place_query(place)
        if query_string is not None:
            q.text_query(query_string)
        if from_number is not None:
            q.from_number(from_number)
        if page_size is not None:
            q.page_size(page_size)
        
        result_objects, total = Search().search(types, q.query())
        sr = SearchResult(result_objects, from_number, page_size, total)
        return sr
    
    @classmethod
    def get_singer(cls, singer_id):
        singer = SingerIndex.pull(singer_id)
        if singer is None:
            raise NotFoundException()
        return singer.raw
    
    @classmethod
    def get_song(cls, song_id):
        song = SongIndex.pull(song_id)
        if song is None:
            raise NotFoundException()
        return song.raw
    
    @classmethod
    def list_singers(cls, fr=0, size=-1, initial_letters=None, order="asc"):
        # construct the list query
        q = ListSingersQuery()
        q.set_from(fr)
        
        if size == -1:
            q.all_results()
        else:
            q.set_size(size)
        
        if initial_letters is not None:
            q.set_initial_letters(initial_letters)
        
        if order.lower() in ["asc", "desc"]:
            q.set_order(order.lower())
        else:
            q.set_order("asc")
        
        result_objects, total = Search().search("singer", q.query(), transpose_type=False)
        sr = SearchResult(result_objects, fr, size, total)
        return sr
    
    @classmethod
    def create_singer(cls, singer_json, versions):
        if singer_json is None:
            return None
        
        # create the singer object and save it to the store
        singer = Singer({"singer" : singer_json})
        if versions is not None:
            singer.versions = versions
        singer.save()
        
        # call the indexing process, and index this object and all
        # related ones
        SingerIndex.by_id(singer.id, cascade=True)
        
        return singer
        
    @classmethod
    def update_singer(cls, singer_id, singer_json=None, versions=None):
        # retrieve and update the singer object in the desired way
        singer = Singer().get(singer_id, links=True)
        
        if singer is None:
            raise NotFoundException()
        
        if singer_json is not None:
            singer.patch_singer(singer_json, replace_all=True, keep_id=True)
        if versions is not None:
            singer.versions = versions
        singer.save()
        
        # call the indexing process, and index this object and all related ones
        SingerIndex.by_id(singer.id, cascade=True)
    
    @classmethod
    def delete_singer(cls, singer_id):
        singer = Singer().get(singer_id, links=True)
        
        if singer is None:
            raise NotFoundException()
        
        # remove the singer from storage first
        singer.remove()
        
        # then remove the singer and re-index any related objects
        SingerIndex.delete_by_id(singer.id)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
