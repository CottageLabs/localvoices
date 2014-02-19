jQuery(document).ready(function($) {

    //////////////////////////////////////////////////////////
    // EXAMPLE SEARCH
    //////////////////////////////////////////////////////////
    
    $("#do_search_example").click(function(event) {
        event.preventDefault();
        var form = $("form[name=search_example]")
        
        // extract the search parameters from the form
        var top_left_lat = form.find("input[name=top_left_lat]").val()
        var top_left_lon = form.find("input[name=top_left_lon]").val()
        var bottom_right_lat = form.find("input[name=bottom_right_lat]").val()
        var bottom_right_lon = form.find("input[name=bottom_right_lon]").val()
        var place = form.find("input[name=place]").val()
        var q = form.find("input[name=q]").val()
        var types = form.find("input[name=types]").val()
        var from = form.find("input[name=from]").val()
        var size = form.find("input[name=size]").val()
        var all_info = form.find("input[name=all_info]").is(":checked")
        
        // build the parameters for the search API call
        var params = {}
        if (top_left_lat) { params["top_left_lat"] = top_left_lat }
        if (top_left_lon) { params["top_left_lon"] = top_left_lon }
        if (bottom_right_lat) { params["bottom_right_lat"] = bottom_right_lat }
        if (bottom_right_lon) { params["bottom_right_lon"] = bottom_right_lon }
        if (place) { params["place"] = place }
        if (q) { params["q"] = q }
        if (types) { params["types"] = types }
        if (from) { params["from"] = from }
        if (size) { params["size"] = size }
        params["max"] = all_info // will be set and will be true or false
        
        // add our callback functions
        params["success"] = function(data) {
            var frag = "<ul>"
            if (data.results) {
                for (var i = 0; i < data.results.length; i++) {
                    var res = data.results[i]
                    var type = res._type
                    var title = res.title
                    var id = res.id
                    var canonical_name = res.canonical_name
                    
                    var min_max = "minimal record"
                    if (res.lv_id) {
                        min_max = "full record"
                    }
                    
                    frag += "<li>"
                    if (title) {
                        frag += title
                    } else if (canonical_name) {
                        frag += canonical_name
                    }
                    frag += " (" + type + ") - " + id + " [" + min_max + "]</li>"
                }
            }
            frag += "</ul>"
            
            $("#search_example_results").html(frag)
        }
        
        params["error"] = function() {
            alert("error calling search API")
        }
        
        // do the search (which will in turn call the callback functions)
        doSearch(params)
    })
    
    
    
    //////////////////////////////////////////////////////////
    // EXAMPLE RETRIEVE
    //////////////////////////////////////////////////////////
    
    $("#do_retrieve_example").click(function(event) {
        event.preventDefault();
        var form = $("form[name=retrieve_example]")
        
        // extract the parameters from the form
        var type = form.find("select[name=retrieve_type]").val()
        var id = form.find("input[name=id]").val()
        
        // build the parameters for the retrieve call
        var params = {"type" : type}
        if (!id) {
            alert("you must enter an id")
            return
        } else {
            params["id"] = id
        }
        
        params["success"] = function(data) {
            // call the standard LV render function on the object
            var frag = undefined
            if (type === "singer") {
                var frag = renderSinger(data)
            } else if (type === "song") {
                var frag = renderSong(data)
            }
            if (frag) {
                $("#retrieve_example_result").html(frag)
            }
        }
        
        params["error"] = function() {
            alert("error calling retrieve API")
        }
        
        // do the retrieve (which will in turn call the callback functions)
        doRetrieve(params)
    });
    
    
    
    //////////////////////////////////////////////////////////
    // EXAMPLE LIST
    //////////////////////////////////////////////////////////
    
    $("#do_list_example").click(function(event) {
        event.preventDefault()
        var form = $("form[name=list_example]")
        
        // extract the list parameters from the form
        var letter = form.find("select[name=letter]").val()
        var from = form.find("input[name=from]").val()
        var size = form.find("input[name=size]").val()
        var type = form.find("select[name=list_type]").val()
        
        // build the parameters for the list call
        var params = {}
        if (letter) { 
            if (letter !== "0") {
                params["letter"] = letter 
            }
        }
        if (from) {params["from"] = from}
        if (size) {params["size"] = size}
        
        var count_of = "songs"
        if (type === "song") {
            count_of = "versions"
        }
        
        params["success"] = function(data) {
            var frag = "<ul>"
            if (data.results) {
                for (var i = 0; i < data.results.length; i++) {
                    var res = data.results[i]
                    var name = res.canonical_name ? res.canonical_name : res.title
                    var count = res.version_count
                    var id = res.id
                    frag += "<li><strong>" + name + "</strong> (" + count + " " + count_of + ") - " + id + "</li>"
                }
            }
            frag += "</ul>"
            $("#list_example_results").html(frag)
        }
        
        params["error"] = function() {
            alert("error calling retrieve API")
        }
        
        // do the list (which will in turn call the callback functions)
        if (type === "singer") {
            listSingers(params)
        } else if (type === "song") {
            listSongs(params)
        }
    });
    
    //////////////////////////////////////////////////////////
    // EXAMPLE CREATE
    //////////////////////////////////////////////////////////
    
    $("#do_create_example").click(function(event) {
        event.preventDefault();
        var form = $("form[name=create_example]")
        var type = form.find("select[name=create_type]").val()
        
        function error() { alert("error saving") }
        function success(data) { alert("saved with id " + data.id) }
        
        if (type === "singer") {
            var create_form = renderSingerForm()
            $("#create_example_form").html(create_form)
            
            $("button[name=submit_singer]").click(function(event) {
                event.preventDefault()
                saveSingerFromForm({
                    form_selector: "form[name=singer_form]",
                    error: error,
                    success: success
                })
            });
            
        } else if (type === "song") {
            var create_form = renderSongForm()
            $("#create_example_form").html(create_form)
            
            $("button[name=submit_song]").click(function(event) {
                event.preventDefault()
                saveSongFromForm({
                    form_selector: "form[name=song_form]",
                    error: error,
                    success: success
                })
            });
        } else if (type === "version") {
            var create_form = renderVersionForm()
            $("#create_example_form").html(create_form)
            
            $("button[name=submit_version]").click(function(event) {
                event.preventDefault()
                saveVersionFromForm({
                    form_selector: "form[name=version_form]",
                    error: error,
                    success: success
                })
            });
        }
    })
    
    //////////////////////////////////////////////////////////
    // EXAMPLE UPDATE
    //////////////////////////////////////////////////////////
    
    $("#do_update_example").click(function(event) {
        event.preventDefault();
        var form = $("form[name=update_example]")
        var type = form.find("select[name=update_type]").val()
        var id = form.find("input[name=id]").val()
        
        if (type === "singer") {
            function retrieve_singer_error() { alert("error retrieving") }
            function retrieve_singer_success(data) {
                var update_form = renderSingerForm({singer: data})
                $("#update_example_form").html(update_form)
                
                function save_singer_error() { alert("error saving") }
                function save_singer_success(data) { alert("saved id " + id) }
                
                $("button[name=submit_singer]").click(function(event) {
                    event.preventDefault()
                    saveSingerFromForm({
                        form_selector: "form[name=singer_form]",
                        error: save_singer_error,
                        success: save_singer_success
                    })
                });
            }
            
            doRetrieve({
                type: "singer",
                id: id,
                error: retrieve_singer_error,
                success: retrieve_singer_success
            })
            
        } else if (type === "song") {
            function retrieve_song_error() { alert("error retrieving") }
            function retrieve_song_success(data) {
                var update_form = renderSongForm({song: data})
                $("#update_example_form").html(update_form)
                
                function save_song_error() { alert("error saving") }
                function save_song_success(data) { alert("saved id " + id) }
                
                $("button[name=submit_song]").click(function(event) {
                    event.preventDefault()
                    saveSongFromForm({
                        form_selector: "form[name=song_form]",
                        error: save_song_error,
                        success: save_song_success
                    })
                });
            }
            
            doRetrieve({
                type: "song",
                id: id,
                error: retrieve_song_error,
                success: retrieve_song_success
            })
            
        } else if (type === "version") {
            function retrieve_version_error() { alert("error retrieving") }
            function retrieve_version_success(data) {
                var update_form = renderVersionForm({version: data})
                $("#update_example_form").html(update_form)
                
                function save_version_error() { alert("error saving") }
                function save_version_success(data) { alert("saved id " + id) }
                
                $("button[name=submit_version]").click(function(event) {
                    event.preventDefault()
                    saveVersionFromForm({
                        form_selector: "form[name=version_form]",
                        error: save_version_error,
                        success: save_version_success
                    })
                });
            }
            
            doRetrieve({
                type: "version",
                id: id,
                error: retrieve_version_error,
                success: retrieve_version_success
            })
        }
    })
    
    //////////////////////////////////////////////////////////
    // EXAMPLE DELETE
    //////////////////////////////////////////////////////////
    
    $("#do_delete_example").click(function(event) {
        event.preventDefault();
        var form = $("form[name=delete_example]")
        var type = form.find("select[name=delete_type]").val()
        var id = form.find("input[name=id]").val()
        
        function error() { alert("error deleting") }
        function success(data) { alert("deleted id " + id) }
        
        doDelete({
            type: type,
            id: id,
            error: error,
            success: success
        })
    });
    
    //////////////////////////////////////////////////////////
    // EXAMPLE LINK
    //////////////////////////////////////////////////////////
    
    function versionLinksForm(params) {
        var id = params.id
        var song_id = params.song_id
        var singer_id = params.singer_id
        
        var frag = "<div class='row-fluid'><div class='span12'>"
        frag += "<form name='version_links_form'>"
        frag += _formRow({name: "id", type: "hidden", value: id})
        frag += _formRow({label: "Song of which this is a version", name: "song_id", type: "text", placeholder: "Song of which this is a version", value: song_id})
        frag += _formRow({label: "Singer of this song version", name: "singer_id", type: "text", placeholder: "Singer of this song version", value: singer_id})
        frag += _formRow({name: "submit_version_links", type: "button", value: "Link!", clazz: "btn btn-info"})
        frag += "</form>"
    
        // close off the initial divs
        frag += "</div></div>"
        return frag
    }
    
    function saveLinksFromVersionForm(params) {
        var form_selector = params.form_selector ? params.form_selector : "form[name=version_links_form]"
        var success_callback = params.success
        var error_callback = params.error
        
        var form = $(form_selector)
        var vid = form.find("input[name=id]").val()
        var song_id = form.find("input[name=song_id]").val()
        var singer_id = form.find("input[name=singer_id]").val()
        
        doSave({
            type: "version",
            id: vid,
            singer_link: singer_id,
            song_link: song_id,
            success: success_callback,
            error: error_callback
        })
    }
    
    function singerLinksForm(params) {
        var id = params.id
        var version_ids = params.version_ids
        
        var version_ids_value = version_ids.join(", ")
        
        var frag = "<div class='row-fluid'><div class='span12'>"
        frag += "<form name='singer_links_form'>"
        frag += _formRow({name: "id", type: "hidden", value: id})
        frag += _formRow({label: "Song versions by this singer", name: "version_ids", type: "textarea", placeholder: "Song versions by this singer", value: version_ids_value})
        frag += _formRow({name: "submit_singer_links", type: "button", value: "Link!", clazz: "btn btn-info"})
        frag += "</form>"
    
        // close off the initial divs
        frag += "</div></div>"
        return frag
    }
    
    function saveLinksFromSingerForm(params) {
        var form_selector = params.form_selector ? params.form_selector : "form[name=singer_links_form]"
        var success_callback = params.success
        var error_callback = params.error
        
        var form = $(form_selector)
        var sid = form.find("input[name=id]").val()
        var version_ids = form.find("textarea[name=version_ids]").val()
        
        var versions = []
        var versionses = version_ids.split(",")
        for (var i = 0; i < versionses.length; i++) {
            versions.push(versionses[i].trim())
        }
                
        doSave({
            type: "singer",
            id: sid,
            version_links: versions,
            success: success_callback,
            error: error_callback
        })
    }
    
    function songLinksForm(params) {
        var id = params.id
        var version_ids = params.version_ids
        var song_ids = params.song_ids
        
        var version_ids_value = version_ids.join(", ")
        var song_ids_value = song_ids.join(", ")
        
        var frag = "<div class='row-fluid'><div class='span12'>"
        frag += "<form name='song_links_form'>"
        frag += _formRow({name: "id", type: "hidden", value: id})
        frag += _formRow({label: "Versions of this song", name: "version_ids", type: "textarea", placeholder: "Versions of this song", value: version_ids_value})
        frag += _formRow({label: "Related songs", name: "song_ids", type: "textarea", placeholder: "Related songs", value: song_ids_value})
        frag += _formRow({name: "submit_song_links", type: "button", value: "Link!", clazz: "btn btn-info"})
        frag += "</form>"
    
        // close off the initial divs
        frag += "</div></div>"
        return frag
    }
    
    function saveLinksFromSongForm(params) {
        var form_selector = params.form_selector ? params.form_selector : "form[name=song_links_form]"
        var success_callback = params.success
        var error_callback = params.error
        
        var form = $(form_selector)
        var sid = form.find("input[name=id]").val()
        var version_ids = form.find("textarea[name=version_ids]").val()
        var song_ids = form.find("textarea[name=song_ids]").val()
        
        var versions = []
        var versionses = version_ids.split(",")
        for (var i = 0; i < versionses.length; i++) {
            versions.push(versionses[i].trim())
        }
        
        var songs = []
        var songses = song_ids.split(",")
        for (var i = 0; i < songses.length; i++) {
            songs.push(songses[i].trim())
        }
                
        doSave({
            type: "song",
            id: sid,
            version_links: versions,
            song_links: songs,
            success: success_callback,
            error: error_callback
        })
    }
    
    $("#do_link_example").click(function(event) {
        event.preventDefault();
        var form = $("form[name=link_example]")
        var type = form.find("select[name=link_type]").val()
        var id = form.find("input[name=id]").val()
        
        function retrieve_error() { alert("error retrieving") }
        function retrieve_success(data) { 
            function link_error() { alert("error linking") }
            function link_success(data) { alert("saved links for id " + id) }
        
            // we have just retrieved the object, so now render the form for it
            if (type === "version") {
                var song_id = data.song.id
                var singer_id = data.singer.id
                var link_form = versionLinksForm({id : id, song_id: song_id, singer_id: singer_id});
                $("#link_example_form").html(link_form)
                
                $("button[name=submit_version_links]").click(function(event) {
                    event.preventDefault()
                    saveLinksFromVersionForm({
                        form_selector: "form[name=version_links_form]",
                        error: link_error,
                        success: link_success
                    })
                });
                
            } else if (type === "singer") {
                var version_ids = []
                if (data.versions) {
                    for (var i = 0; i < data.versions.length; i++) {
                        var v = data.versions[i]
                        version_ids.push(v.id)
                    }
                }
                var link_form = singerLinksForm({id : id, version_ids: version_ids});
                $("#link_example_form").html(link_form)
                
                $("button[name=submit_singer_links]").click(function(event) {
                    event.preventDefault()
                    saveLinksFromSingerForm({
                        form_selector: "form[name=singer_links_form]",
                        error: link_error,
                        success: link_success
                    })
                });
                
            } else if (type === "song") {
                var version_ids = []
                if (data.versions) {
                    for (var i = 0; i < data.versions.length; i++) {
                        var v = data.versions[i]
                        version_ids.push(v.id)
                    }
                }
                var song_ids = []
                if (data.relations) {
                    for (var i = 0; i < data.relations.length; i++) {
                        var s = data.relations[i]
                        song_ids.push(s.id)
                    }
                }
                var link_form = songLinksForm({id : id, version_ids: version_ids, song_ids: song_ids});
                $("#link_example_form").html(link_form)
                
                $("button[name=submit_song_links]").click(function(event) {
                    event.preventDefault()
                    saveLinksFromSongForm({
                        form_selector: "form[name=song_links_form]",
                        error: link_error,
                        success: link_success
                    })
                });
            }
        }
        
        // we need to retrieve the current links, so retrieve the object
        doRetrieve({
            type: type,
            id: id,
            error: retrieve_error,
            success: retrieve_success
        })
    });
    
    
    
    
    
    
    
    
    
    
});
