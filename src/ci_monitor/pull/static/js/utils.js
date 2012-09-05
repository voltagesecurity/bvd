function process_existing_widgets() {
    // $widgets = widget_map[hostname];
    //     for (j = 0; j < $widgets.length; j++) {
    //         $widget = $widgets[j];
    //         for (x = 0; x < json_list.length; x++) {
    //             if ($widget.job_name == json_list[x].job_name) {
    //                 $widget.set_status(json_list[x].status);
    //             }
    //         }
    //     }
}

function create_new_widgets($widgets, json_list, count) {
    for (j =0; j < json_list.length; j++) {
		var $widget = new Widget(json_list[j].job_name, json_list[j].status, count);
		$widgets.push($widget);
    	count++;
	}
	return count;
}

function set_size_of_widgets(count) {
    var $prev_widget = $("<div></div>");
    $prev_widget.css({'left' : -1, 'top' : -1});
    var counter = 0;
    var db_map = {};
    var db_list = [];
    for (hostname in widget_map) {
		$widgets = widget_map[hostname];
		for (i=0; i < $widgets.length; i++) {
			var $current_widget = $widgets[i];
			$current_widget.set_size(count,
			                                parseInt($prev_widget.css('left').replace('px','')),
			                                parseInt($prev_widget.css('top').replace('px','')),
			                                counter
			                            );
			db_map[$current_widget.attr('id')] = {'top' : parseInt($current_widget.css('top').replace('px','')), 'left' : parseInt($current_widget.css('top').replace('px',''))}
			
			$prev_widget = $current_widget;
		    counter++;
		}
	}
	
	db_list.push(db_map);
	
	return db_list;
}

/**
	Function to construct a map of widgets based on the result of polling
	all jenkins servers.
	
	This function looks for a set of existing widgets for each hostname, if not found
	it uses the create_new_widgets function to construct them.
	
	@param json_results JSON
*/
function create_or_update_widgets(json_results) {
    var created = {}
    var hosts = [];
    var count = 0;
    for (i =0; i < json_results.length; i++) {
		var $widgets = [];
        var map = {};
        if (typeof(widget_map[json_results[i]['hostname']]) != 'undefined') {
            process_existing_widgets(); 
        }
        else{
			count = create_new_widgets($widgets, json_results[i]['json'], count);
    	}
    	map[json_results[i]['hostname']] = json_results[i]['json'];
    	hosts.push(map);
		widget_map[json_results[i]['hostname']] = $widgets;
    }
    
    var db_list = set_size_of_widgets(count);
    
    created['hosts'] = hosts;
    created['db_list'] = db_list;

	return created;
}
