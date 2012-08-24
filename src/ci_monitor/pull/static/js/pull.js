widget_map = {};

function create_widget(job_name) {

	var base = function() {
	 	$widget = $('<div></div>');
		$widget.text = job_name;
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
	
	$widget.job_name = job_name;
	return $widget;
	
}

function create_widgets(json_results) {
	widget_map = {};
	
	for (i =0; i < json_results.length; i ++) {
		$widget = create_widget(json_results[i].job_name);
		widget_map[$widget.job_name] = $widget;
		switch (json_results[i].status) {
			case 'success':
				$widget.make_success();
				break;
			case 'failed':
				$widget.make_failure();
				break;
		}
	}
	
	
}


