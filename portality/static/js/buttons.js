jQuery(document).ready(function($) {

//close pop overs
    
    $(".close").click(function(event) {
    
    	$( this ).parent().removeClass( "view" );
    

	});
	
	
	//advance search close
	
	$(".advancedclose").click(function(event) {
    
    	$( this ).parent().removeClass( "view" );
    	
    	     var frag = ""
            
            $("#search_example_results").html(frag)
            
            $("input[name=top_left_lat]").val('60') 
            $("input[name=top_left_lon]").val('-5') 
            $("input[name=bottom_right_lat]").val('50') 
            $("input[name=bottom_right_lon]").val('0') 
            
            $("input[name=place]").val("")             
            $("input[name=q]").val("")             
            $("input[name=types]").val("song,singer,version") 
            $("input[name=size]").val('10') 
            
    	

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



});