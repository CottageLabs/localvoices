from flask import Flask, request, abort, render_template, make_response
from flask.views import View
# from flask.ext.login import login_user, current_user
import json

import portality.models as models
from portality.core import app#, login_manager
from portality.api import LocalVoicesAPI, NotFoundException

# in case we need any login stuff later, these are useful ...
'''
@login_manager.user_loader
def load_account_for_login_manager(userid):
    out = models.Account.pull(userid)
    return out

@app.context_processor
def set_current_context():
    """ Set some template context globals. """
    return dict(current_user=current_user, app=app)
'''

'''
@app.before_request
def standard_authentication():
    """Check remote_user on a per-request basis."""
    remote_user = request.headers.get('REMOTE_USER', '')
    if remote_user:
        user = models.Account.pull(remote_user)
        if user:
            login_user(user, remember=False)
    # add a check for provision of api key
    elif 'api_key' in request.values:
        res = models.Account.query(q='api_key:"' + request.values['api_key'] + '"')['hits']['hits']
        if len(res) == 1:
            user = models.Account.pull(res[0]['_source']['id'])
            if user:
                login_user(user, remember=False)
'''

#######################################################################
# API endpoints for Local Voices
#######################################################################

@app.route("/")
def root():
    return make_response("Local Voices API")

@app.route("/search")
def search():
    """
    from_lat - upper-most latitude for search results
    to_lat - lower-most latitude for search results
    from_lon - left-most longitude for search results
    to_lon - right-most longitude for search results
    place - placename to search for
    q - free-text query string
    type - one or more of "singer", "song", "version" as a comma-delimitted list
    from - result number to start from
    size - page size to return
    """
    # extract the parameters from the query string
    from_lat = request.values.get("from_lat")
    to_lat = request.values.get("to_lat")
    from_lon = request.values.get("from_lon")
    to_lon = request.values.get("to_lon")
    place = request.values.get("place")
    q= request.values.get("q")
    type = request.values.get("type")
    fr = request.values.get("from", 0)
    size = request.values.get("size", 25)
    
    # break down the comma-delimited string of query types
    types = [t.strip() for t in type.split(",")] if type is not None else None
    
    # ask the API to calculate the answer
    result = LocalVoicesAPI.search(from_lat=from_lat, to_lat=to_lat, from_lon=from_lon, 
                                    to_lon=to_lon, place=place, query_string=q, types=types,
                                    from_number=fr, page_size=size)
    
    # return a json response
    resp = make_response(json.dumps(result.as_dict()))
    resp.mimetype = "application/json"
    return resp
    
@app.route("/singers", methods=["GET", "POST"])
def singers():
    if request.method == "GET":
        from_param = request.values.get("from", 0)
        size = request.values.get("size", 50)
        letter = request.values.get("letter")
        
        result = LocalVoicesAPI.list_singers(fr=from_param, size=size, initial_letters=letter, order="asc")
        
        # return a json response
        resp = make_response(json.dumps(result.as_dict()))
        resp.mimetype = "application/json"
        return resp
    
    elif request.method == "POST":
        try:
            req = json.loads(request.data) # for some reason request.get_json doesn't work
        except:
            abort(400)
        
        newid = None
        if "id" in req:
            # this is an update to an existing object
            try:
                LocalVoicesAPI.update_singer(req.get("id"), singer_json=req.get("singer"), versions=req.get("versions"))
                newid = req.get("id")
            except NotFoundException:
                abort(400) # bad request, not 404, as the url itself is fine
        else:
            # we are creating a new singer
            if req.get("singer") is not None:
                new_singer = LocalVoicesAPI.create_singer(req.get("singer"), req.get("versions"))
                newid = new_singer.id
            else:
                abort(400)
        
        resp = make_response(json.dumps({"id" : newid}))
        resp.mimetype = "application/json"
        return resp
        

@app.route("/singer/<singer_id>", methods=["GET", "PUT", "DELETE"])
def singer(singer_id):
    if request.method == "GET":
        try:
            s = LocalVoicesAPI.get_singer(singer_id)
            resp = make_response(json.dumps(s))
            resp.mimetype = "application/json"
            return resp
        except NotFoundException:
            abort(404)
    
    elif request.method == "PUT":
        try:
            req = json.loads(request.data) # for some reason request.get_json doesn't work
        except:
            abort(400)
        
        try:
            LocalVoicesAPI.update_singer(singer_id, singer_json=req.get("singer"), versions=req.get("versions"))
            return "", 204
        except NotFoundException:
            abort(404)
    
    elif request.method == "DELETE":
        try:
            LocalVoicesAPI.delete_singer(singer_id)
            return "", 204
        except NotFoundException:
            abort(404)
        
@app.route("/songs", methods=["POST"])
def songs():
    pass

@app.route("/song/<song_id>", methods=["GET", "PUT", "DELETE"])
def song(song_id):
    if request.method == "GET":
        try:
            s = LocalVoicesAPI.get_song(song_id)
            resp = make_response(json.dumps(s))
            resp.mimetype = "application/json"
            return resp
        except NotFoundException:
            abort(404)

@app.route("/versions", methods=["POST"])
def versions():
    pass
    
@app.route("/version/<version_id>", methods=["PUT", "DELETE"])
def version(version_id):
    pass

#######################################################################

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'])

