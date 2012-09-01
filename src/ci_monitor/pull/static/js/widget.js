var widget_map = {};

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
		$('#widgets').append($widget);
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
	
	$widget.make_down = function() {
	    this.addClass('down');
	    this.removeClass('success');
	    this.removeClass('error');
	}
	
	$widget.set_size = function(count) {
		var size = String(0.5/Math.log(count));
		size = size.substring(2,5);
		
		this.css('height',size+'px');
		//this.css('line-height',size+'px');
		this.css('width',size+'px');
	}
	
	$widget.job_name = job_name;
	return $widget;
	
}


function check_widget_status($widget, status) {
    switch (json_list[j].status) {
		case 'SUCCESS':
			$widget.make_success();
			break;
		case 'FAILURE':
			$widget.make_failure();
			break;
		case 'DOWN':
		    $widget.make_down();
		    break;
		case '404':
		    break;
	}
}

/**
	Function to construct a map of widgets based on the result of polling
	all jenkins servers.
	
	This function looks for an existing widget matching a job_name, if not found
	it uses the create_widget function to construct it.
	
	@param json_results JSON
*/
function create_or_update_widgets(json_results) {
    hosts = [];
    var size = 1;
    for (i =0; i < json_results.length; i++) {
        var map = {};
        hostname = json_results[i]['hostname'];
        json_list = json_results[i]['json'];
        if (!typeof(widget_map[hostname]) == 'undefined') {
            $widgets = widget_map[hostname];
            for (j = 0; j < $widgets.length; j++) {
                $widget = $widgets[j];
                for (x = 0; x < json_list.length; x++) {
                    if ($widget.job_name == json_list[x].job_name) {
                        check_widget_status($widget,json_list[x].status);
                    }
                }
            }
        }
        for (j =0; j < json_list.length; j++) {
            size++;
    		job_name = json_list[j].job_name;
    		$widget = widget_map[job_name] || create_widget(job_name);
			check_widget_status($widget,json_list[j].status);
    		$widget.set_size(size);   		
    	}
    	map[hostname] = json_list;
    	hosts.push(map);
    }
	return hosts;
}