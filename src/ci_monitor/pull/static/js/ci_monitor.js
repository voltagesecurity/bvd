var Poll = function(url) {
	var self = this;
	self.created = {};
	
	this.draw_widgets = function(data) {
		self.created = create_or_update_widgets(eval(data));
	};
		
	var success = function(data) {
		self.draw_widgets(data);
	};
	
	var error = function(data) { 
		//catch-all 
		alert('Please check CI System URIs in settings.py');
	};
	
	this.ajax = function() {
		do_ajax('get',url,{}, function(data) {
    	    data = eval(data);
    	    remove_old_widgets();
    	    redraw_widgets(data);
    	});
	}
}

$(function(){

	var poll = new Poll('/pull/pull_jobs/');
   
    var jenkins = function() {
    	if ($("#add_job_modal").length == 0) {
        	poll.ajax();
        }
    }
	
	setInterval(jenkins,'60000');
	
	var resize = function(data) {
	    
	    var curr_width = $(this).width();
	    var curr_height = $(this).height();
	    var max_width = $("#widgets").children(0).css('width');
	    var max_height =  $("#widgets").children(0).css('height');
	    
	    var ratio = curr_height / curr_width;
	    
	    if ((curr_width/5) >= max_width && ratio <= 1) {
	        curr_width = max_width ;
	        curr_height = max_width * ratio;
        } else {
            curr_height = (curr_width/5) * ratio;
            curr_width = curr_height;
        }
	    
	    for (hostname in widget_map) {
    		$widgets = widget_map[hostname];
    		for (i=0; i < $widgets.length; i++) {
    			$widgets[i].resize(curr_width,curr_height);
    		}
    	}
	}
	
	$(window).resize(resize);
	
    
});
