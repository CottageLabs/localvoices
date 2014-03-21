jQuery(document).ready(function($) {
	//Google Map -------------------------------------------------------------//

	function initialize() {
		var markers = [];
		var map = new google.maps.Map(document.getElementById('map-canvas'), {
			mapTypeId: google.maps.MapTypeId.ROADMAP
		});
		var defaultBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(59.2995517, -9.6240234), new google.maps.LatLng(55.6031782, -0.0878906));
		map.fitBounds(defaultBounds);
		// Create the search box and link it to the UI element.
		var input = /** @type {HTMLInputElement} */
		(
		document.getElementById('pac-input'));
		map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
		var searchBox = new google.maps.places.SearchBox( /** @type {HTMLInputElement} */ (input));
		
				//move checkbox html items onto map
		var checkbox_singer = (
		document.getElementById('singer-pins-check-container'));
		map.controls[google.maps.ControlPosition.TOP_LEFT].push(checkbox_singer);
		var checkbox_song = (
		document.getElementById('song-pins-check-container'));
		map.controls[google.maps.ControlPosition.TOP_LEFT].push(checkbox_song);
		
		
		// [START region_getplaces]
		// Listen for the event fired when the user selects an item from the
		// pick list. Retrieve the matching places for that item.
		google.maps.event.addListener(searchBox, 'places_changed', function() {
			var places = searchBox.getPlaces();
			for (var i = 0, marker; marker = markers[i]; i++) {
				marker.setMap(null);
			}
			// For each place, get the icon, place name, and location.
			markers = [];
			var bounds = new google.maps.LatLngBounds();
			for (var i = 0, place; place = places[i]; i++) {
				var image = {
					url: place.icon,
					size: new google.maps.Size(71, 71),
					origin: new google.maps.Point(0, 0),
					anchor: new google.maps.Point(17, 34),
					scaledSize: new google.maps.Size(20, 20)
				};
				// Create a marker for each place.
				var marker = new google.maps.Marker({
					map: map,
					icon: image,
					title: place.name,
					position: place.geometry.location
				});
				markers.push(marker);
				bounds.extend(place.geometry.location);
				map.setZoom(11);
			}
			map.fitBounds(bounds);

		});
		// [END region_getplaces]
		// Bias the SearchBox results towards places that are within the bounds of the
		// current map's viewport.
		google.maps.event.addListener(map, 'bounds_changed', function() {
			var bounds = map.getBounds();
			searchBox.setBounds(bounds);
		});
		// create marker and info window function		

		function createMarker(content, lat, lng, iconFile) {
			var contentString = content;
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(lat, lng),
				map: map,
			});
			google.maps.event.addListener(marker, 'click', function() {
				infowindow.setContent(contentString);
				infowindow.open(map, marker);
				var position = marker.getPosition();
				//Add click event to singers names to open info window
				$(document).on('click', '.mapsinger', function(event) { map.setCenter(position); map.setZoom(10); 						showSinger(event) });
			});
			
			marker.setIcon(iconFile)
		} // end create marker function
		//Load singer markers ---------------------------------------------------------
		//While loop for data  
		var infowindow = new google.maps.InfoWindow();
		var lat = 55.953252
		var lng = -3.188267
		var iconFile = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
		var contentString = 'not set';
		//Call function to get singer data
		var params = {}
		params["types"] = 'singer'
		params["max"] = false // will be set and will be true or false
		// Sucessful search - display results
		params["success"] = function(data) {
			//if data available			
			if (data.results) {
				//set singer icon type
				iconFile = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
				//loop through results and create map points.
				for (var i = 0; i < data.results.length; i++) {
					// get singer object data
					var res = data.results[i]
					var type = res._type
					var id = res.id
					var lat = res.canonical_location["lat"]
					var lng = res.canonical_location["lon"]
					var canonical_name = res.canonical_name
					//create pop up string
					contentString = '<div id="InfoWindowContent">' + '<div id="siteNotice">' + '</div>' + '<p class="mapsinger" id="' + id + '">' + canonical_name + '</p> </div>';
					//create marker
					createMarker(contentString, lat, lng, iconFile);
				}
			}
		}
		params["error"] = function() {
			alert("error calling search API")
		}
		// do the search (which will in turn call the callback functions)
		doSearch(params)

	}
	//load map	
	google.maps.event.addDomListener(window, 'load', initialize);


	// end google maps code ---------------------------------------------------------------*/
	//Singer A-Z ---------------------------------------------------------------*/
	$("#letter").change(function(event) {
		event.preventDefault()
		var form = $("form[name=list_singers]")
		// extract the list parameters from the form
		var letter = form.find("select[name=letter]").val()
		var from = form.find("input[name=from]").val()
		var size = form.find("input[name=size]").val()
		// build the parameters for the list call
		var params = {}
		if (letter) {
			if (letter !== "0") {
				params["letter"] = letter
			}
		}
		// add back in to use pagination 
		//  if (from) {params["from"] = from}
		//  if (size) {params["size"] = size}
		params["success"] = function(data) {
			var frag = "<ul>"
			if (data.results) {
				for (var i = 0; i < data.results.length; i++) {
					var res = data.results[i]
					var name = res.canonical_name
					var count = res.version_count
					var id = res.id
					frag += "<li id='" + id + "' class='singer_link' > " + name + " (" + count + " songs) </li>"
				}
			}
			frag += "</ul>"
			$("#list_singer_results").html(frag)
		}
		params["error"] = function() {
			alert("error calling retrieve API")
		}
		// do the list (which will in turn call the callback functions)
		listSingers(params)
	});
	
	//show singer
	$("#list_singer_results").on("click", "li", function(event) { showSinger(event) });	
	
	// Songs A-Z ---------------------------------------------------------------
	//
	$("#letter_songs").change(function(event) {
		event.preventDefault()
		var form = $("form[name=list_songs]")
		// extract the list parameters from the form
		var letter = form.find("select[name=letter_songs]").val()
		
		// build the parameters for the list call
		var params = {}
		if (letter) {
			if (letter !== "0") {
				params["letter"] = letter
			}
		}
			params["success"] = function(data) {
			var frag = "<ul>"
			if (data.results) {
				for (var i = 0; i < data.results.length; i++) {
					var res = data.results[i]
					var name = res.canonical_name ? res.canonical_name : res.title
					var count = res.version_count
					var id = res.id
					frag += "<li id='" + id + "' class='singer_link' > " + name + " (" + count + " versions) </li>"
				}
			}
			frag += "</ul>"
			$("#list_songs_results").html(frag)
		}
		params["error"] = function() {
			alert("error calling retrieve API")
		}
		// do the list (which will in turn call the callback functions)
		listSongs(params)
	});
	$("#list_songs_results").on("click", "li", function(event) {showSong(event); });
	
	// Nav bar  search --------------------------------------------------- *
	//
	$("#do_search").click(function(event) {
	
	
		event.preventDefault();
		var form = $("form[name=search_example]")
		// extract the search parameters from the form
		var q = form.find("input[name=q]").val()
		var all_info = form.find("input[name=all_info]").is(":checked")
		// build the parameters for the search API call
		var params = {}
		if (q) {
			params["q"] = q
		}
		params["types"] = 'singer,song'
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
					frag += "<li class='" + type +"' id='"+ id + "'>"
					if (title) {
						frag += title
					} else if (canonical_name) {
						frag += canonical_name
					}
					frag += " (" + type + ")</li>"
				}
			}
			frag += "</ul>"
			$("#search_results").html(frag)
			
			
		}
		params["error"] = function() {
			alert("error calling search API")
		}
		// do the search (which will in turn call the callback functions)
		doSearch(params)
		$("#pop-over-search").addClass("view")
	})
	
	$(document).on('click', '.singer', function(event) { showSinger(event) });
	$(document).on('click', '.song', function(event) { showSong(event) });
	$(document).on('click', '.version', function(event) {
		showVersion(event)
	});
	

}); //end on page load

//------------------------------------------------------------------------------

	//function to show singer pop over
	
	function showSinger(event) {
			
			var singerID = event.target.id;
			var params = {}
			params["type"] = 'singer'
			params["id"] = singerID
			params["error"] = function() {
				alert("error calling retrieve API - BEE FAIL")
			}
			params["success"] = function(data) {
				// call the standard LV render function on the object
				var frag = undefined
				var frag = renderSingerMod(data)
				if (frag) {
					$("#singer-profile").html(frag)
				}
				$("#pop-over-singer").addClass("view")
				
			}
			
			doRetrieve(params)
		}
	// function to show song pop over 
	
	function showSong(event) {
		var songID = event.target.id;
		var params = {}
		params["type"] = 'song'
		params["id"] = songID
		params["error"] = function() {}
		params["success"] = function(data) {
			// call the standard LV render function on the object
			var frag = undefined
			var frag = renderSongMod(data)
			if (frag) {
				$("#song-detail").html(frag)
			}
			$("#pop-over-song-detail").addClass("view")
		}
		doRetrieve(params)
	}
	
	// function to show secondary song pop over 
	
	function showSubSong(event) {
		var songID = event.target.id;
		var params = {}
		params["type"] = 'song'
		params["id"] = songID
		params["error"] = function() {}
		params["success"] = function(data) {
			// call the standard LV render function on the object
			var frag = undefined
			var frag = renderSongMod(data)
			if (frag) {
				$("#song-detail-2").html(frag)
			}
			else { frag = "API ERROR - BEE FAIL"}
			
			$("#sub-pop-over-song-detail").addClass("view")
			
		}
		doRetrieve(params)
	}

function showVersion(event) {
	var versionID = event.target.id;
	var params = {}
	params["type"] = 'version'
	params["id"] = versionID
	params["error"] = function() {}
	params["success"] = function(data) {
		// call the standard LV render function on the object
		var frag = undefined
		var frag = renderVersion(data)
		if (frag) {
			$("#song-detail").html(frag)
		}
		$("#pop-over-song-detail").addClass("view")
	}
	doRetrieve(params)
}

//Modified reder functions - singer
function renderSingerMod(singer_data) {
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
    frag += "<h2>" + name + "</h2>"
    frag += "<strong>LV Singer ID: </strong>" + lvid + "<br>"
    frag += "<strong>Gender: </strong>" + gender + "<br>"
    frag +=  "<strong>Birth, death dates: </strong>" + born + " - " + died
   // if (bio) {
        frag += "<h3>Biography</h3><p>" + bio + "</p>"
   // }
    frag += "</div>"
    
    // list the versions associated with the singer
    if (singer_data.versions) {
        frag += "<div class='row-fluid'><div class='span12'>"
        frag += "<h3> Songs performed by "+ name + "</h3><br> <ul>"
        
        for (var i = 0; i < singer_data.versions.length; i++) {
            var version = singer_data.versions[i]
            var vtitle = version.title
            var vlvid = version.lv_id
            var summary = version.summary
            var vid = version.id
            
            frag += "<li id='" + vid + "' class='version'>"
            frag +=  vtitle + " (" + vlvid + ")"
            frag += "</li>"
        }
        frag += "</ul></div></div>"
    }
    
    // close off the initial divs
    frag += "</div></div>"
    return frag
}

function renderSongMod(song_data) {
    // start a fluid row
    var frag = "<div class='row-fluid'><div class='span12'>"
    
    // get and normalise the song fields we want to display
    var title = song_data.title
    var lvid = song_data.lv_id
    var sid = song_data.id
    var alts = song_data.alternative_title
    var summary = song_data.summary
    var composer = song_data.composer
    if (song_data.time_period) {
    	var time_period_from = song_data.time_period["from"]
        var time_period_to = song_data.time_period["to"]
    }
    var created = song_data.created_date
    var updated = song_data.last_updated
    
    // build the song's entry
    frag += "<div class='row-fluid'><div class='span12'>"
    frag += "<h2>" + title + "</h2>"
    frag += "<strong>LV Version ID: </strong>" + lvid + "<br>"

    if (alts) {
        frag += "<strong> Alternative title(s): </strong> " + alts.join(" | ") + "<br>"
    }
    if (summary) {
        frag += "<strong> Summary: </strong><p>" + summary + "</p>"
    }
    
    if (time_period_from) {
    	frag += "<strong>Time Period: </strong> From" + time_period_from + " to " + time_period_to + "<br>"
    }
    
    if (!composer) { composer="unknown"}
    
    frag += "<strong>Composer: </strong> " + composer + "<br>"
    
    frag += "</div>"
    
    // list the versions associated with the song
    if (song_data.versions) {
        frag += "<div class='row-fluid'><div class='span12'>"
        frag += "<h3>Versions</h3>"
        frag += "<ul>"
        for (var i = 0; i < song_data.versions.length; i++) {
            var version = song_data.versions[i]
            var vtitle = version.title
            var vlvid = version.lv_id
            var vid = version.id

            
            var singer = "unknown"
            if (version.singer && version.singer.canonical_name) {
                singer = version.singer.canonical_name
            }
            
            frag += "<li class='version' id='" + vid + "'>"
            frag += "(" + vlvid + ") <strong>" + vtitle + "</strong> by " + singer
            frag += "</li>"
        }
        frag += "</ul></div></div>"
    }
    
    // list the versions associated with the song
    if (song_data.relations) {
    	frag += "<div class='row-fluid'><div class='span12'>"
    	frag += "<h3>Related Songs</h3> " 
    	frag += "<ul>"
    	for (var i = 0; i < song_data.relations.length; i++) {
    		var relation = song_data.relations[i]
    		var rtitle = relation.title
            var rid = relation.id
			
			frag += "<li class='relation' id='" + rid + "'>"
            frag += " " + rtitle + " "
            frag += "</li>"
    	}
    	frag += "</ul></div></div>"
    	
    	$(document).on('click', '.relation', function(event) { showSubSong(event) });
    }

    // close off the initial divs   
    frag += "<p>Created on: " + created + " Last Updated: " + updated + "</p>"
    frag += "</div></div>"
    return frag
}

function renderVersion(song_data) {
	// start a fluid row
	var frag = "<div class='row-fluid'><div class='span12'>"
	// get and normalise the song fields we want to display
	var title = song_data.title
	var parentTitle = song_data.song['title']
	var parentID = song_data.song['id']
	var lvid = song_data.lv_id
	var sid = song_data.id
	var alts = song_data.alternative_title
	var summary = song_data.summary
	var language = song_data.language
	var lyrics = song_data.lyrics
	var composer = song_data.composer
	var collector = song_data.collector
	var source = song_data.source
	var collected_date = song_data.collected_date
	if (song_data.time_period) {
		var time_period_from = song_data.time_period["from"]
		var time_period_to = song_data.time_period["to"]
	}
	var created = song_data.created_date
	var updated = song_data.last_updated
	// build the song's entry
	frag += "<div class='row-fluid'><div class='span12'>"
	frag += "<h2>" + title + "</h2>"
	frag += "<strong>LV Version ID: </strong>" + lvid + "<br>"
		frag += "<strong>Version Title: </strong>" + parentTitle + "<br>"
	if (alts) {
		frag += "<strong> Alternative title(s): </strong> " + alts.join(" | ") + "<br>"
	}
	if (summary) {
		frag += "<strong>Version Summary: </strong><p>" + summary + "</p>"
	}
	if (time_period_from) {
		frag += "<strong>Time Period: </strong> From" + time_period_from + " to " + time_period_to + "<br>"
	}
	if (!composer) {
		composer = "unknown"
	}
	frag += "<strong>Composer: </strong> " + composer + "<br>"
	frag += "<strong>Language: </strong> " + language + "<br>"
	frag += "<strong>Collector: </strong> " + collector + "<br>"
	frag += "<strong>Source: </strong> " + source + "<br>"
	frag += "<strong>Collected Date: </strong> " + collected_date + "<br>"
	if (!lyrics) {
		lyrics = "unavailable"
	}
	frag += "<strong>Lyrics: </strong> " + lyrics + "<br>"
	frag += "</div>"
	// list the versions associated with the song
	if (song_data.versions) {
		frag += "<div class='row-fluid'><div class='span12'>"
		frag += "<h3>Versions</h3>"
		frag += "<ul>"
		for (var i = 0; i < song_data.versions.length; i++) {
			var version = song_data.versions[i]
			var vtitle = version.title
			var vlvid = version.lv_id
			var vid = version.id
			var singer = "unknown"
			if (version.singer && version.singer.canonical_name) {
				singer = version.singer.canonical_name
			}
			frag += "<li class='version' id='" + vid + "'>"
			frag += "(" + vlvid + ") " + vtitle + "by " + singer
			frag += "</li>"
		}
		frag += "</ul></div></div>"
	}
	// list the versions associated with the song
	if (song_data.relations) {
		frag += "<div class='row-fluid'><div class='span12'>"
		frag += "<h3>Related Songs</h3> "
		frag += "<ul>"
		for (var i = 0; i < song_data.relations.length; i++) {
			var relation = song_data.relations[i]
			var rtitle = relation.title
			var rid = relation.id
			frag += "<li class='relation' id='" + rid + "'>"
			frag += " " + rtitle + " "
			frag += "</li>"
		}
		frag += "</ul></div></div>"
		$(document).on('click', '.relation', function(event) {
			showSubSong(event)
		});
	}
	// close off the initial divs   
	frag += "<p>Created on: " + created + " Last Updated: " + updated + "</p>"
	frag += "</div></div>"
	return frag
}

