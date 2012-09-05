function process_existing_widgets() {
    $widgets = widget_map[hostname];
    for (j = 0; j < $widgets.length; j++) {
        $widget = $widgets[j];
        for (x = 0; x < json_list.length; x++) {
            if ($widget.job_name == json_list[x].job_name) {
                $widget.set_status(json_list[x].status);
            }
        }
    }
}

function process_new_widgets($widgets, size) {
    for (j =0; j < json_list.length; j++) {
    	size++;
		var $widget = new Widget(json_list[j].job_name,json_list[j].status);
		$widgets.push($widget);
	}
	return size;
}

function set_size_of_widgets(size) {
    var $prev_widget = null;
    var counter = 0;
    var db_map = {};
    var db_list = [];
    for (hostname in widget_map) {
		$widgets = widget_map[hostname];
		for (i=0; i < $widgets.length; i++) {
		    var prev_left = ($prev_widget != null) ? parseInt($prev_widget.css('left').replace('px','')) : -1;
		    var prev_top = ($prev_widget != null) ? parseInt($prev_widget.css('top').replace('px','')) : -1;
			var $current_widget = $widgets[i];
			$current_widget.set_size(size,prev_left,prev_top,counter);
			db_map[$current_widget.attr('id')] = {'top' : parseInt($current_widget.css('top').replace('px','')), 'left' : parseInt($current_widget.css('top').replace('px',''))}
			db_list.push(db_map);
			$prev_widget = $current_widget;
		    counter++;
		}
	}
	
	return db_list;
}

/**
	Function to construct a map of widgets based on the result of polling
	all jenkins servers.
	
	This function looks for a set of existing widgets for each hostname, if not found
	it uses the create_widget function to construct them.
	
	@param json_results JSON
*/
function create_or_update_widgets(json_results) {
    hosts = [];
    var size = 1;
    for (i =0; i < json_results.length; i++) {
		var $widgets = [];
        var map = {};
        hostname = json_results[i]['hostname'];
        json_list = json_results[i]['json'];
        if (typeof(widget_map[hostname]) != 'undefined') {
            process_existing_widgets(); 
        }
        else{
			size = process_new_widgets($widgets, size);
    	}
    	map[hostname] = json_list;
    	hosts.push(map);
		widget_map[hostname] = $widgets;
    }
    
    db_list = set_size_of_widgets(size);
	
	widget_map['count'] = size;
	return hosts;
}
