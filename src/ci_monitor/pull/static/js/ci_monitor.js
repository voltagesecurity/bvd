var Poll = function(url) {
	var self = this;
	this.draw_widgets = function(data) {
		create_or_update_widgets(eval(data));
	}
		
	var success = function(data) {
		self.draw_widgets(data);
	};
	
	var error = function(data) { 
		//catch-all 
		alert('Please check CI System URIs in settings.py');
	};
	
	this.ajax = function() {
		return $.get(url)
		.success(success)
		.error(error)
		.complete(function(data) {});
	}
	
	
	
}

$(function(){
	var poll = new Poll('/pull/get_jenkins_views/');
	poll.ajax();
	
});