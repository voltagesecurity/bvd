var Poll = function(url) {
	var self = this;
	self.host_names = [];
	
	this.draw_widgets = function(data) {
		self.host_names = create_or_update_widgets(eval(data));
	}
		
	var success = function(data) {
		self.draw_widgets(data);
	};
	
	var error = function(data) { 
		//catch-all 
		alert('Please check CI System URIs in settings.py');
	};
	
	this.ajax = function() {
	    if (self.host_names.length > 0) {
    	    self.post_data = {
    	        'hosts' : JSON.stringify(self.host_names)
    	    };
    	} else {
    	    self.post_data =  {
    	        
    	    };
    	}
    	
    	return $.ajax({
    	                       url: url,
    	                       type: 'post',
    	                       data: self.post_data,
    	                       headers: {
    	                           "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
    	                       },
    	                       success: success,
    	                       error: error
    	                       });
	}
}

$(function(){
    
	var poll = new Poll('/pull/get_jenkins_views/');
	poll.ajax();
	
	var jenkins = function() {
		poll.ajax();
	}
	
	setInterval(jenkins,'60000');
	
	var resize = function(data) {
	    
	    var curr_width = $(this).width();
	    var curr_height = $(this).height();
	    var max_width = 1250;
	    var max_height = 700;
	    
	    var ratio = curr_height / curr_width;
	    
	    if (curr_width >= max_width && ratio <= 1) {
	        curr_width = max_width;
	        curr_height = max_width * ratio;
        } else if(curr_height >= max_height) {
            curr_height = max_height;
            curr_width = curr_height / ratio;
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