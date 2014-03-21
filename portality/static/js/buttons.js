jQuery(document).ready(function($) {

//close pop overs
    
    $(".close").click(function(event) {
    
    	$( this ).parent().removeClass( "view" );

	});
	
    //show singers div
    $("#singers-a-z").click(function(event) {
    
    	$( ".popovers" ).removeClass( "view" );
    
    	$("#pop-over-singers").addClass( "view" );

	});
	
	   //show singers div
    $("#songs-a-z").click(function(event) {
    
    	$( ".popovers" ).removeClass( "view" );
    
    	$("#pop-over-songs").addClass( "view" );

	});
	
	$("#advanced_search").click(function(event) {
    	$( ".popovers" ).removeClass( "view" );

    	$("#form_advanced_search").addClass( "view" );

	});

$("#do_search_advanced").click(function(event) {
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
                    
                    frag += "<li class='" + type + "' id='" + id + "' >"
                    if (title) {
                        frag += title
                    } else if (canonical_name) {
                        frag += canonical_name
                    }
                    frag += " (" + type + ")</li>"
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
        
	$(document).on('click', '.singer', function(event) { showSinger(event) });
	$(document).on('click', '.song', function(event) { showSong(event) });
	$(document).on('click', '.version', function(event) {
		showVersion(event)
	});

    })


});