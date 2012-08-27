widget_map = {};

/**
	Function to create and return a widget object.  
	A widget object is an icon on the screen representing
	a Jenkins build, that has either a success or failed status
	
	The object returned can be later manipulated via helper methods
	to change state, set its position on the page, set its size, etc.
	
	@param job_name String 
*/
function create_widget(job_name) {

	var base = function() {
	 	
		$widget = $('<div></div>');
		$widget.html(job_name);
		$widget.attr('class','widget');
		
		
	}
	
	base();
	
	$widget.make_success = function() {
		this.addClass('success');
		this.removeClass('error');
	}
	
	$widget.make_failure = function() {
		this.addClass('error');
		this.removeClass('success');
	}
	
	$widget.set_size = function(count) {
		var size = String(0.5/Math.log(count));
		size = size.substring(2,5);
		
		this.css('height',size+'px');
		this.css('line-height',size+'px');
		this.css('width',size+'px');
	}
	
	$widget.append = function() {
		$('#widgets').append(this);
	}
	
	$widget.job_name = job_name;
	return $widget;
	
}

/**
	Function to construct a map of widgets based on the result of polling
	all jenkins servers.
	
	This function looks for an existing widget matching a job_name, if not found
	it uses the create_widget function to construct it.
	
	@param json_results JSON
*/
function create_or_update_widgets(json_results) {
	
	for (i =0; i < json_results.length; i++) {
		job_name = json_results[i].job_name;

		$widget = widget_map[job_name] || create_widget(job_name);
		
		switch (json_results[i].status) {
			case 'SUCCESS':
				$widget.make_success();
				break;
			case 'FAILURE':
				$widget.make_failure();
				break;
		}
		$widget.set_size(json_results.length);
		$widget.append();
		
		widget_map[job_name] = $widget;
	}
}


