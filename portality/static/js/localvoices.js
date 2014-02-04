///////////////////////////////////////////////////////////
// pure client library for the LV API
///////////////////////////////////////////////////////////

// doSearch - perform a search on the LV database
//
// parameters:
//
//top_left_lat - upper-most latitude for search results
//bottom_right_lat - lower-most latitude for search results
//top_left_lon - left-most longitude for search results
//bottom_right_lon - right-most longitude for search results
//place - placename to search for
//q - free-text query string
//type - one or more of "singer", "song", "version" as a comma-delimitted list
//from - the result number to commence listing from. Defaults to 0, and is used for result set paging
//size - the size of the result set, and can be used to determine the "from" value for the next request when paging
//success - function to execute on returned data
//error - function to execute in the case of error
    
function doSearch(params) {
    // extract all the parameters
    var from_lat = params.top_left_lat
    var to_lat = params.bottom_right_lat
    var from_lon = params.top_left_lon
    var to_lon = params.bottom_right_lon
    var place = params.place
    var q = params.q
    var types = params.types
    var from = params.from
    var size = params.size
    var success_callback = params.success
    var error_callback = params.error
    
    // build the request object based on the parameters
    var obj = {}
    if (from_lat && to_lat && from_lon && to_lon) {
        obj["from_lat"] = from_lat
        obj["to_lat"] = to_lat
        obj["from_lon"] = from_lon
        obj["to_lon"] = to_lon
    }
    
    if (place) {obj["place"] = place}
    if (q) {obj["q"] = q}
    
    if (types) {
        // detect if this is a list, and join by "," if necessary
        if ($.isArray(types)) {
            types = types.join(",")
        }
        obj["type"] = types
    }
    
    if (from) {obj["from"] = from}
    if (size) {obj["size"] = size}
    
    if (!success_callback) {
        success_callback = function() {}
    }
    if (!error_callback) {
        error_callback = function() {}
    }
    
    // now make the ajax request
    $.ajax({
        type: "GET",
        url: "/search",
        dataType: "jsonp",
        data: obj,
        success: success_callback,
        error: error_callback
    })
}

// doRetrieve - retrieve singer or song objects from the LV database by id
//
// parameters:
//type - one of "singer" or "song"
//id - the identifier of the singer or song
//success - function to execute on returned data
//error - function to execute in the case of error

function doRetrieve(params) {
    // extract all the parameters
    var type = params.type
    var id = params.id
    var success_callback = params.success
    var error_callback = params.error
    
    if (!success_callback) {
        success_callback = function() {}
    }
    if (!error_callback) {
        error_callback = function() {}
    }
    
    if (!id) {
        error_callback()
        return
    }
    
    // build the url from the parameters
    var url = "/" + type + "/" + id
    
    // now make the ajax request
    $.ajax({
        type: "GET",
        url: url,
        dataType: "jsonp",
        success: success_callback,
        error: error_callback
    })
}

// listSingers - retrieve an alphabetically ordered list of singers
//
// parameters:
//letter - initial letter to list
//from - the result number to commence listing from. Defaults to 0, and is used for result set paging
//size - the size of the result set, and can be used to determine the "from" value for the next request when paging
//success - function to execute on returned data
//error - function to execute in the case of error

function listSingers(params) {
    // extract all the parameters
    var letter = params.letter
    var from = params.from
    var size = params.size
    var success_callback = params.success
    var error_callback = params.error
    
    if (!success_callback) {
        success_callback = function() {}
    }
    if (!error_callback) {
        error_callback = function() {}
    }
    
    // build the request object based on the parameters
    var obj = {}
    if (letter) { obj["letter"] = letter }
    if (from) {obj["from"] = from}
    if (size) {obj["size"] = size}
    
    // now make the ajax request
    $.ajax({
        type: "GET",
        url: "/singers",
        dataType: "jsonp",
        data: obj,
        success: success_callback,
        error: error_callback
    })
}

// doSave - save the LV object to the datastore
//
// parameters:
//type - the type of object to be saved
//data - the object itself to be saved
//success - function to execute on returned data
//error - function to execute in the case of error

function doSave(params) {
    var type = params.type
    var entity = params.entity
    var id = params.id
    var singer = params.singer_link
    var song = params.song_link
    var versions = params.version_links
    var songs = params.song_links
    var success_callback = params.success
    var error_callback = params.error
    
    // work out which method we're using
    var method = id ? "PUT" : "POST"
    
    // work out the url to send the request to
    var url = undefined
    if (type === "singer") {
        url = id ? "/singer/" + id : "/singers"
    } else if (type === "song") {
        url = id ? "/song/" + id : "/songs"
    } else if (type === "version") {
        url = id ? "/version/" + id : "/versions"
    }
    
    // build the object to be saved
    var obj = {}
    if (id) {obj["id"] = id}
    if (entity) {
        if (type === "singer") { obj["singer"] = entity }
        if (type === "song") { obj["song"] = entity }
        if (type === "version") { obj["version"] = entity }
    }
    if (singer) { obj["singer"] = singer }
    if (song) { obj["song"] = song }
    if (versions) { obj["versions"] = versions }
    if (songs) { obj["songs"] = songs }
    
    if (!success_callback) {
        success_callback = function() {}
    }
    if (!error_callback) {
        error_callback = function() {}
    }
    
    // make the ajax request and call the callbacks
    $.ajax({
        type: method,
        url: url,
        contentType: "application/json",
        dataType: "jsonp",
        data: JSON.stringify(obj),
        success : success_callback,
        error: error_callback
    })
}

// doDelete - delete an object from the LV database
//
// parameters:
//type - type of object to be deleted
//id - id of object to be deleted
//success - function to execute on returned data
//error - function to execute in the case of error
function doDelete(params) {
    var type = params.type
    var id = params.id
    var success_callback = params.success
    var error_callback = params.error
    
    // work out the url to send the request to
    var url = undefined
    if (type === "singer") {
        url = "/singer/" + id
    } else if (type === "song") {
        url = "/song/" + id
    } else if (type === "version") {
        url = "/version/" + id
    }
    
    if (!url || !id) {
        error_callback()
        return
    }
    
    // now make the ajax request
    $.ajax({
        type: "DELETE",
        url: url,
        dataType: "jsonp",
        success: success_callback,
        error: error_callback
    })
}
    
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// Render functions for the various LV objects
///////////////////////////////////////////////////////////

function renderSinger(singer_data) {
    // start a fluid row
    var frag = "<div class='row-fluid'><div class='span12'>"
    
    // get and normalise the fields we want to display
    var name = singer_data.canonical_name
    var gender = singer_data.gender === "m" ? "male" : singer_data.gender === "f" ? "female" : ""
    var lvid = singer_data.lv_id
    var born = singer_data.born ? singer_data.born : "unknown"
    var died = singer_data.died ? singer_data.died : "present/unknown"
    var bio = singer_data.biograpy
    var sid = singer_data.id
    
    // build the singer's entry
    frag += "<div class='row-fluid'><div class='span12'>"
    frag += "<strong>" + name + "</strong> (" + lvid + ") - " + sid + "<br>"
    frag += gender + "; " + born + " to " + died
    if (bio) {
        frag += "<p>" + bio + "</p>"
    }
    frag += "</div>"
    
    // list the versions associated with the singer
    if (singer_data.versions) {
        frag += "<div class='row-fluid'><div class='span12'>"
        frag += "<strong>versions of songs performed</strong><br>"
        for (var i = 0; i < singer_data.versions.length; i++) {
            var version = singer_data.versions[i]
            var vtitle = version.title
            var vlvid = version.lv_id
            var summary = version.summary
            var vid = version.id
            
            frag += "<div class='row-fluid'><div class='span12'>"
            frag += "<strong>" + vtitle + "</strong> (" + vlvid + ") - " + vid + "<br>"
            frag += "<p><em>" + summary + "</em></p>"
            frag += "</div></div>"
        }
        frag += "</div></div>"
    }
    
    // close off the initial divs
    frag += "</div></div>"
    return frag
}


function renderSong(song_data) {
    // start a fluid row
    var frag = "<div class='row-fluid'><div class='span12'>"
    
    // get and normalise the song fields we want to display
    var title = song_data.title
    var lvid = song_data.lv_id
    var sid = song_data.id
    var alts = song_data.alternative_title
    var summary = song_data.summary
    
    // build the song's entry
    frag += "<div class='row-fluid'><div class='span12'>"
    frag += "<strong>" + title + "</strong> (" + lvid + ") - " + sid + "<br>"
    if (alts) {
        frag += "aka " + alts.join(" | ")
    }
    if (summary) {
        frag += "<p>" + summary + "</p>"
    }
    frag += "</div>"
    
    // list the versions associated with the song
    if (song_data.versions) {
        frag += "<div class='row-fluid'><div class='span12'>"
        frag += "<strong>versions of this song</strong><br>"
        for (var i = 0; i < song_data.versions.length; i++) {
            var version = song_data.versions[i]
            var vtitle = version.title
            var vlvid = version.lv_id
            var summary = version.summary
            var vid = version.id
            
            var singer = "unknown"
            if (version.singer && version.singer.canonical_name) {
                singer = version.singer.canonical_name
            }
            
            frag += "<div class='row-fluid'><div class='span12'>"
            frag += "<strong>" + vtitle + "</strong> (" + vlvid + ") - " + vid + "<br>"
            frag += "by " + singer + "<br>"
            frag += "<p><em>" + summary + "</em></p>"
            frag += "</div></div>"
        }
        frag += "</div></div>"
    }
    
    // close off the initial divs
    frag += "</div></div>"
    return frag
}


///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// Edit forms for the various LV objects
///////////////////////////////////////////////////////////

function _formRow(params) {
    var label = params.label
    var name = params["name"]
    var type = params.type
    var placeholder = params.placeholder
    var value = params.value
    var options = params.options
    var field = params.field
    var clazz = params.clazz
    var selected = params.selected

    if (!label) { label = "&nbsp;" }
    if (!value) { value = "" }
    
    if (type === "hidden") {
        // special treatment for hidden fields
        var frag = "<input type='hidden' name='" + name + "' value='" + value + "'>"
        return frag
    }
    
    var frag = "<div class='row-fluid'><div class='span3'><strong>" + label + "</strong></div>"
    frag += "<div class='span9'>"
    
    if (field) {
        frag += field
    } else if (type === "text") {
        if (!placeholder) { placeholder = "" }
        if (!value) { value = "" }
        frag += "<input type='text' name='" + name + "' placeholder='" + placeholder + "' value='" + value + "' style='width: 100%'>"
    } else if (type === "radio") {
        var keys = Object.keys(options)
        for (var i = 0; i < keys.length; i++) {
            var val = keys[i]
            var disp = options[val]
            var check = ""
            if (val === selected) {
                check = "checked='checked'"
            }
            frag += "<input type='radio' name='" + name + "' value='" + val + "' " + check + ">" + disp + "&nbsp;&nbsp;"
        }
    } else if (type === "textarea") {
        frag += "<textarea name='" + name + "' placeholder='" + placeholder + "' style='width: 100%'>" + value + "</textarea>"
    } else if (type === "button") {
        if (!clazz) {clazz = ""}
        frag += "<button name='" + name + "' class='" + clazz + "'>" + value + "</button>"
    }
    
    frag += "</div></div>"
    return frag
}

function _locationEntry(params) {
    // extract the parameters
    params = params ? params : {}
    var locs = params.locations
    
    // FIXME: only displaying the first location
    var loc = {location: "", lat : "", lon: "", relation: ""}
    if (locs) {
        if (locs.length > 0) {
            loc = locs[0]
        }
    }
    
    var lat = loc.lat ? loc.lat : ""
    var lon = loc.lon ? loc.lon : ""
    var place = loc.place ? loc.place : ""
    
    var native_selected = loc.relation === "native_area" ? "selected='selected'" : ""
    var significant_selected = loc.relation === "significant" ? "selected='selected'" : ""
    var main_selected = loc.relation === "main" ? "selected='selected'" : ""
    
    var frag = "<select name='relation' style='width: 200px'>"
    frag += "<option value='native_area' " + native_selected + ">Native Area</option>"
    frag += "<option value='significant' " + significant_selected + ">Significant Location</option>"
    frag += "<option value='main' " + main_selected + ">Main Location in a Song</option></select>"
    
    frag += "&nbsp;&nbsp;Lat <input type='text' name='lat' placeholder='latitude' value='" + lat + "' style='width: 50px'>"
    frag += "&nbsp;&nbsp;Lon <input type='text' name='lon' placeholder='longitude' value='" + lon + "' style='width: 50px'><br>"
    frag += "Place Name <input type='text' name='place' placeholder='placename' value='" + place + "' style='width: 150px'>"
    return _formRow({label: "Location", field: frag})
}

function renderSingerForm(params) {
    // extract the parameters
    params = params ? params : {}
    var singer = params.singer
    
    // extract the form values from the singer object
    if (singer) {
        var sid = singer.id
        var lvid = singer.lv_id
        var first_name = singer["name"].first
        var middle_name = singer["name"].middle
        var last_name = singer["name"].last
        var aka = ""
        if (singer["name"].aka) {
            aka = singer["name"].aka.join(", ")
        }
        var groups = ""
        if (singer.groups) {
            groups = singer.groups.join(", ")
        }
        var gender = singer.gender
        var locs = singer.location // FIXME: there can be multiple locs, but we only support one in this version of the form
        var born = singer.born
        var died = singer.died
        var bio = singer.biography
        var photo_url = singer.photo_url
        var source = singer["source"]
    }

    // start a fluid row
    var frag = "<div class='row-fluid'><div class='span12'>"
    
    if (singer) {
        frag += "<p><strong>Edit an existing singer</strong></p>"
    } else {
        frag += "<p><strong>Create a new singer</strong></p>"
    }
    
    frag += "<form name='singer_form'>"
    if (sid) {
        frag += _formRow({name: "id", type: "hidden", value: sid})
    }
    frag += _formRow({label: "LV ID", name: "lvid", type: "text", placeholder: "Local Voices Identifier", value: lvid})
    frag += _formRow({label: "First Name", name: "first_name", type: "text", placeholder: "First Name", value: first_name})
    frag += _formRow({label: "Middle Name", name: "middle_name", type: "text", placeholder: "Middle Name", value: middle_name})
    frag += _formRow({label: "Last Name", name: "last_name", type: "text", placeholder: "Last Name", value: last_name})
    frag += _formRow({label: "Also Known As (comma separated)", name: "aka", type: "text", placeholder: "Also Known As (comma separated)", value: aka})
    frag += _formRow({label: "Groups (comma separated)", name: "groups", type: "text", placeholder: "Groups (comma separated)", value: groups})
    frag += _formRow({label: "Gender", name: "gender", type: "radio", options: {"m" : "male", "f" : "female"}, selected: gender})
    frag += _locationEntry({locations: locs})
    frag += _formRow({label: "Born", name: "born", type: "text", placeholder: "Date singer was born (e.g. 1978, 1980-01-01)", value: born})
    frag += _formRow({label: "Died", name: "died", type: "text", placeholder: "Date singer died (e.g. 1984, 1984-03-01)", value: died})
    frag += _formRow({label: "Biography", name: "bio", type: "textarea", placeholder: "Singer Biography...", value: bio})
    frag += _formRow({label: "Photo URL", name: "photo_url", type: "text", placeholder: "Photo URL", value: photo_url})
    frag += _formRow({label: "Source", name: "source", type: "textarea", placeholder: "Source of information", value: source})
    
    var btnval = singer ? "Update!" : "Create!"
    frag += _formRow({name: "submit_singer", type: "button", value: btnval, clazz: "btn btn-info"})
    frag += "</form>"
    
    // close off the initial divs
    frag += "</div></div>"
    return frag
}

function renderSongForm(params) {
    // extract the parameters
    params = params ? params : {}
    var song = params.song
    
    // extract the form values from the song object
    if (song) {
        var sid = song.id
        var lvid = song.lv_id
        var title = song.title
        var summary = song.summary
        var locs = song.location // FIXME: there can be multiple locs, but we only support one in this version of the form
        if (song.time_period) {
            var from = song.time_period.from
            var to = song.time_period.to
        }
        var composer = song.composer
    }

    // start a fluid row
    var frag = "<div class='row-fluid'><div class='span12'>"
    
    if (song) {
        frag += "<p><strong>Edit an existing song</strong></p>"
    } else {
        frag += "<p><strong>Create a new song</strong></p>"
    }
    
    frag += "<form name='song_form'>"
    if (sid) {
        frag += _formRow({name: "id", type: "hidden", value: sid})
    }
    frag += _formRow({label: "LV ID", name: "lvid", type: "text", placeholder: "Local Voices Identifier", value: lvid})
    frag += _formRow({label: "Title", name: "title", type: "text", placeholder: "Title", value: title})
    frag += _formRow({label: "Summary", name: "summary", type: "textarea", placeholder: "Summary", value: summary})
    frag += _locationEntry({locations: locs})
    frag += _formRow({label: "From date/period", name: "from", type: "text", placeholder: "From date/period", value: from})
    frag += _formRow({label: "To date/period", name: "to", type: "text", placeholder: "To date/period", value: to})
    frag += _formRow({label: "Composer", name: "composer", type: "text", placeholder: "Composer", value: composer})
    
    var btnval = song ? "Update!" : "Create!"
    frag += _formRow({name: "submit_song", type: "button", value: btnval, clazz: "btn btn-info"})
    frag += "</form>"
    
    // close off the initial divs
    frag += "</div></div>"
    return frag
}

function renderVersionForm(params) {
    // extract the parameters
    params = params ? params : {}
    var version = params.version
    
    // extract the form values from the version object
    if (version) {
        var sid = version.id
        var lvid = version.lv_id
        var title = version.title
        var alts = ""
        if (version.alternative_title) {
            alts = version.alternative_title.join(", ")
        }
        var summary = version.summary
        var langs = ""
        if (version.language) {
            langs = version.language.join(", ")
        }
        var media_url = ""
        if (version.media_url) {
            media_url = version.media_url.join(", ")
        }
        var lyrics = version.lyrics
        var photo_url = version.photo_url
        var collector = version.collector
        var source = version["source"]
        var collected_date = version.collected_date
        var locs = version.location // FIXME: there can be multiple locs, but we only support one in this version of the form
        var roud = undefined
        var greig_duncan = undefined
        var child = undefined
        var laws = undefined
        if (version.references) {
            for (var i = 0; i < version.references.length; i++) {
                var ref = version.references[i]
                if (ref.type === "roud") { roud = ref.number }
                if (ref.type === "greig-duncan") { greig_duncan = ref.number }
                if (ref.type === "child") { child = ref.number }
                if (ref.type === "laws") { laws = ref.number }
            }
        }
        var comments = version.comments
        var tags = ""
        if (version.tags) {
            tags = version.tags.join(", ")
        }
    }

    // start a fluid row
    var frag = "<div class='row-fluid'><div class='span12'>"
    
    if (version) {
        frag += "<p><strong>Edit an existing song version</strong></p>"
    } else {
        frag += "<p><strong>Create a new song version</strong></p>"
    }
    
    frag += "<form name='version_form'>"
    if (sid) {
        frag += _formRow({name: "id", type: "hidden", value: sid})
    }
    frag += _formRow({label: "LV ID", name: "lvid", type: "text", placeholder: "Local Voices Identifier", value: lvid})
    frag += _formRow({label: "Title", name: "title", type: "text", placeholder: "Title", value: title})
    frag += _formRow({label: "Alternative Titles (comma separated)", name: "alternative_title", type: "text", placeholder: "Alternative Titles (comma separated)", value: alts})
    frag += _formRow({label: "Summary", name: "summary", type: "textarea", placeholder: "Summary...", value: summary})
    frag += _formRow({label: "Languages (comma separated)", name: "language", type: "text", placeholder: "Languages (comma separated)", value: langs})
    frag += _formRow({label: "Media URL", name: "media_url", type: "text", placeholder: "Media URL", value: media_url})
    frag += _formRow({label: "Lyrics", name: "lyrics", type: "textarea", placeholder: "Lyrics...", value: lyrics})
    frag += _formRow({label: "Photo URL", name: "photo_url", type: "text", placeholder: "Photo URL", value: photo_url})
    frag += _formRow({label: "Collector", name: "collector", type: "text", placeholder: "Collector", value: collector})
    frag += _formRow({label: "Source", name: "source", type: "textarea", placeholder: "Source of information", value: source})
    frag += _formRow({label: "Collected Date", name: "collected_date", type: "text", placeholder: "Collected Date", value: collected_date})
    frag += _locationEntry({locations: locs})
    frag += _formRow({label: "Roud", name: "roud", type: "text", placeholder: "Roud Number", value: roud})
    frag += _formRow({label: "Greig-Duncan", name: "greig_duncan", type: "text", placeholder: "Greig-Duncan Number", value: greig_duncan})
    frag += _formRow({label: "Child", name: "child", type: "text", placeholder: "Child Number", value: child})
    frag += _formRow({label: "Laws", name: "laws", type: "text", placeholder: "Laws Number", value: laws})
    frag += _formRow({label: "Comments", name: "comments", type: "textarea", placeholder: "Comments ...", value: comments})
    frag += _formRow({label: "Tags (comma separated)", name: "tags", type: "text", placeholder: "Tags (comma separated)", value: tags})
    
    var btnval = version ? "Update!" : "Create!"
    frag += _formRow({name: "submit_version", type: "button", value: btnval, clazz: "btn btn-info"})
    frag += "</form>"
    
    // close off the initial divs
    frag += "</div></div>"
    return frag
}

///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// Save routines for the various LV objects
///////////////////////////////////////////////////////////

function parseSingerFromForm(params) {
    var form_selector = params.form_selector ? params.form_selector : "form[name=singer_form]"
    
    // lift all of the singer metadata out of the form
    var form = $(form_selector)
    var sid = form.find("input[name=id]").val()
    var lvid = form.find("input[name=lvid]").val()
    var first_name = form.find("input[name=first_name]").val()
    var middle_name = form.find("input[name=middle_name]").val()
    var last_name = form.find("input[name=last_name]").val()
    var aka = form.find("input[name=aka]").val()
    var groups = form.find("input[name=groups]").val()
    var gender = form.find("input[name=gender]:checked").val()
    var location_relation = form.find("select[name=relation]").val()
    var lat = form.find("input[name=lat]").val()
    var lon = form.find("input[name=lon]").val()
    var place = form.find("input[name=place]").val()
    var born = form.find("input[name=born]").val()
    var died = form.find("input[name=died]").val()
    var bio = form.find("textarea[name=bio]").val()
    var photo_url = form.find("input[name=photo_url]").val()
    var source = form.find("textarea[name=source]").val()
    
    // construct a singer object according to the storage specification
    var singer = {}
    if (sid) { singer["id"] = sid }
    if (lvid) { singer["lv_id"] = lvid }
    if (first_name || middle_name || last_name || aka) {
        var name = {}
        if (first_name) {name["first"] = first_name}
        if (middle_name) {name["middle"] = middle_name}
        if (last_name) {name["last"] = last_name}
        if (aka) {
            var alts = []
            var akas = aka.split(",")
            for (var i = 0; i < akas.length; i++) {
                alts.push(akas[i].trim())
            }
            name["aka"] = alts
        }
        singer["name"] = name
    }
    if (groups) {
        var gs = []
        var groupses = groups.split(",")
        for (var i = 0; i < groupses.length; i++) {
            gs.push(groupses[i].trim())
        }
        singer["groups"] = gs
    }
    if (gender) { singer["gender"] = gender }
    if (lat || lon || place) {
        var loc = {}
        if (location_relation) {loc["relation"] = location_relation}
        if (lat && lon) {
            loc["lat"] = lat
            loc["lon"] = lon
        }
        if (place) { loc["place"] = place }
        singer["location"] = [loc]  // FIXME: we currently only allow one location per singer via this form
    }
    if (born) { singer["born"] = born }
    if (died) { singer["died"] = died }
    if (bio) { singer["biography"] = bio }
    if (photo_url) { singer["photo_url"] = photo_url }
    if (source) { singer["source"] = source }
    
    return singer
}

function saveSingerFromForm(params) {
    var form_selector = params.form_selector ? params.form_selector : "form[name=singer_form]"
    var success_callback = params.success
    var error_callback = params.error
    
    var singer_obj = parseSingerFromForm({form_selector: form_selector})
    var sid = singer_obj.id
    
    doSave({
        type: "singer",
        entity: singer_obj,
        id: sid,
        success: success_callback,
        error: error_callback
    })
}



function parseSongFromForm(params) {
    var form_selector = params.form_selector ? params.form_selector : "form[name=song_form]"
    
    // lift all of the singer metadata out of the form
    var form = $(form_selector)
    var sid = form.find("input[name=id]").val()
    var lvid = form.find("input[name=lvid]").val()
    var title = form.find("input[name=title]").val()
    var summary = form.find("textarea[name=summary]").val()
    var location_relation = form.find("select[name=relation]").val()
    var lat = form.find("input[name=lat]").val()
    var lon = form.find("input[name=lon]").val()
    var place = form.find("input[name=place]").val()
    var from = form.find("input[name=from]").val()
    var to = form.find("input[name=to]").val()
    var composer = form.find("input[name=composer]").val()
    
    // construct a song object according to the storage specification
    var song = {}
    if (sid) { song["id"] = sid }
    if (lvid) { song["lv_id"] = lvid }
    if (title) { song["title"] = title }
    if (summary) { song["summary"] = summary }
    if (lat || lon || place) {
        var loc = {}
        if (location_relation) {loc["relation"] = location_relation}
        if (lat && lon) {
            loc["lat"] = lat
            loc["lon"] = lon
        }
        if (place) { loc["place"] = place }
        song["location"] = [loc]  // FIXME: we currently only allow one location per singer via this form
    }
    if (from || to) {
        song["time_period"] = {}
        if (from) { song.time_period["from"] = from }
        if (to) { song.time_period["to"] = to }
    }
    if (composer) { song["composer"] = composer }
    
    return song
}

function saveSongFromForm(params) {
    var form_selector = params.form_selector ? params.form_selector : "form[name=song_form]"
    var success_callback = params.success
    var error_callback = params.error
    
    var song_obj = parseSongFromForm({form_selector: form_selector})
    var sid = song_obj.id
    
    doSave({
        type: "song",
        entity: song_obj,
        id: sid,
        success: success_callback,
        error: error_callback
    })
}

function parseVersionFromForm(params) {
    var form_selector = params.form_selector ? params.form_selector : "form[name=version_form]"
    
    // lift all of the version metadata out of the form
    var form = $(form_selector)
    var sid = form.find("input[name=id]").val()
    var lvid = form.find("input[name=lvid]").val()
    var title = form.find("input[name=title]").val()
    var alts = form.find("input[name=alternative_title]").val()
    var summary = form.find("textarea[name=summary]").val()
    var langs = form.find("input[name=language]").val()
    var media_url = form.find("input[name=media_url]").val()
    var lyrics = form.find("textarea[name=lyrics]").val()
    var photo_url = form.find("input[name=photo_url]").val()
    var collector = form.find("input[name=collector]").val()
    var source = form.find("textarea[name=source]").val()
    var collected_date = form.find("input[name=collected_date]").val()
    var location_relation = form.find("select[name=relation]").val()
    var lat = form.find("input[name=lat]").val()
    var lon = form.find("input[name=lon]").val()
    var place = form.find("input[name=place]").val()
    var roud = form.find("input[name=roud]").val()
    var greig_duncan = form.find("input[name=greig_duncan]").val()
    var child = form.find("input[name=child]").val()
    var laws = form.find("input[name=laws]").val()
    var comments = form.find("textarea[name=comments]").val()
    var tags = form.find("input[name=tags]").val()
    
    // construct a version object according to the storage specification
    var version = {}
    if (sid) { version["id"] = sid }
    if (lvid) { version["lv_id"] = lvid }
    if (title) { version["title"] = title }
    if (alts) {
        var alternatives = []
        var altses = alts.split(",")
        for (var i = 0; i < altses.length; i++) {
            alternatives.push(altses[i].trim())
        }
        version["alternative_title"] = alternatives
    }
    if (summary) { version["summary"] = summary }
    if (langs) {
        var languages = []
        var langses = langs.split(",")
        for (var i = 0; i < langses.length; i++) {
            languages.push(langses[i].trim())
        }
        version["language"] = languages
    }
    if (media_url) {
        var urls = []
        var medias = media_url.split(",")
        for (var i = 0; i < medias.length; i++) {
            urls.push(medias[i].trim())
        }
        version["media_url"] = urls
    }
    if (lyrics) { version["lyrics"] = lyrics }
    if (photo_url) { version["photo_url"] = photo_url }
    if (collector) { version["collector"] = collector }
    if (source) { version["source"] = source }
    if (collected_date) { version["collected_date"] = collected_date }
    if (lat || lon || place) {
        var loc = {}
        if (location_relation) {loc["relation"] = location_relation}
        if (lat && lon) {
            loc["lat"] = lat
            loc["lon"] = lon
        }
        if (place) { loc["place"] = place }
        version["location"] = [loc]  // FIXME: we currently only allow one location per version via this form
    }
    
    var refs = []
    if (roud) { refs.push({"type" : "roud", "number" : roud}) }
    if (greig_duncan) { refs.push({"type" : "greig-duncan", "number" : greig_duncan}) }
    if (child) { refs.push({"type" : "child", "number" : child}) }
    if (laws) { refs.push({"type" : "laws", "number" : laws}) }
    if (refs.length > 0) {
        version["references"] = refs
    }
    if (comments) { version["comments"] = comments }
    if (tags) {
        var ts = []
        var tagses = tags.split(",")
        for (var i = 0; i < tagses.length; i++) {
            ts.push(tagses[i].trim())
        }
        version["tags"] = ts
    }
    
    return version
}

function saveVersionFromForm(params) {
    var form_selector = params.form_selector ? params.form_selector : "form[name=version_form]"
    var success_callback = params.success
    var error_callback = params.error
    
    var version_obj = parseVersionFromForm({form_selector: form_selector})
    var vid = version_obj.id
    
    doSave({
        type: "version",
        entity: version_obj,
        id: vid,
        success: success_callback,
        error: error_callback
    })
}

///////////////////////////////////////////////////////////
