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
		
	    //$.ajax(url,JSON.stringify({'hosts' : self.host_names})).success(success);
	}
	
	
	
}

$(function(){
	var poll = new Poll('/pull/get_jenkins_views/');
	poll.ajax();
	
	var jenkins = function() {
		poll.ajax();
	}
	
	setInterval(jenkins,'60000');
	
	$.resize(data,function(){
	    alert('test');
	});
	
});