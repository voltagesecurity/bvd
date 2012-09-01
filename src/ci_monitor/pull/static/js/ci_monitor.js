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
	    var width = $(this).width();
	    var height = $(this).height();
	    var count = widget_map['count'];
	    
	    var widget_width = String((0.75 * Math.log(width)) / Math.log(count));
	    var widget_height = String((0.75 * Math.log(height)) / (0.75 * Math.log(count)));
	    
	    widget_width = widget_width.substring(0,4).replace('.','');
	    widget_height = widget_height.substring(0,4).replace('.','');
	    
	    for (hostname in widget_map) {
    		$widgets = widget_map[hostname];
    		for (i=0; i < $widgets.length; i++) {
    			$widgets[i].resize(widget_width,widget_height);
    		}
    	}
	}
	
	$(window).resize(resize);
	
});