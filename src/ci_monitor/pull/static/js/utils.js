var do_ajax = function (type, url, data, success, error) {
    return $.ajax({
            url: url,
	        type: type,
	        data: data,
	        headers: {
	               "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
	        },
	        success: success,
	        error: error
	    });
}

function validate_email(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
} 

function save_widgets() {
	var widgets = {};
	var list = [];
	for (hostname in widget_map) {
		$widgets = widget_map[hostname];
		for (i=0; i < $widgets.length; i++) {
			$widget = $widgets[i];
			data = $widget.getWidgetDimensions();
			data['hostname'] = hostname;
    		data['displayname'] = $widget.displayname;
    		data['jobname'] = $widget.jobname;
    		data['status'] = $widget.status;
    		list.push(data);
		}
	}
	widgets['widgets'] = JSON.stringify(list);
	do_ajax('post','/pull/save_jobs/',widgets);
}

function create_new_widget(json) {
    var count = $("#widgets").children().length + 3;
    var $widget = new Widget(json.jobname, json.displayname, json.status, count);
    
    if (typeof(widget_map[json.hostname]) != 'undefined') {
        widget_map[json.hostname].push($widget);
    } else {
        $widgets = [$widget];
        widget_map[json.hostname] = $widgets;
    }
    
    set_size_of_widgets(count);
    save_widgets();
   
}


function set_size_of_widgets(count) {
    
    var $prev_widget = $("<div></div>");
    var counter = 0;
    var db_map = {};
    var db_list = [];
    for (hostname in widget_map) {
		$widgets = widget_map[hostname];
		for (i=0; i < $widgets.length; i++) {
		    if (counter == 0) {dimensions = {left : '0px', top: '0px'}}
		    else {dimensions = $prev_widget.getWidgetDimensions();}
			var $current_widget = $widgets[i];
			
			$current_widget.set_size(count,
			                                parseInt(dimensions['left'].replace('px','')),
			                                parseInt(dimensions['top'].replace('px','')),
			                                counter
			                            );
			$prev_widget = $current_widget;
		    counter++;
		}
	}
	
	db_list.push(db_map);
	
	return db_list;
}

function update_widgets(json_results) {
    for (i =0; i < json_results.length; i++) {
        if (typeof(widget_map[json_results[i]['hostname']]) != 'undefined') {
            $widgets = widget_map[json_results[i]['hostname']];
            for (j = 0; j < $widgets.length; j++) {
                $widget = $widgets[j];
                if ($widget.jobname == json_results[i].jobname) {
                    $widget.set_status(json_results[i].status);
                }
            }
            widget_map[json_results[i]['hostname']] = $widgets;
        }
    }	
}


