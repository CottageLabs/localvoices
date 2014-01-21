from portality.dao import SearchQuery, Search

class LocalVoicesAPI(object):
    
    @classmethod
    def search(cls, types, from_lat=None, to_lat=None, from_lon=None, to_lon=None, place=None, query_string=None):
        """
        types - one or more of "singer", "song", "version" in a list
        from_lat - upper-most latitude for search results
        to_lat - lower-most latitude for search results
        from_lon - left-most longitude for search results
        to_lon - right-most longitude for search results
        place - placename to search for
        query_string - free-text query string
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
        
        result_objects = Search().search(types, q.query())
        
        return result_objects
