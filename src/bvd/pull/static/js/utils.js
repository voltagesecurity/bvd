/**

* BVD v1.0

* Copyright (c) 2012 Voltage Security
* All rights reserved.

* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions
* are met:
* 1. Redistributions of source code must retain the above copyright
*    notice, this list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright
*    notice, this list of conditions and the following disclaimer in the
*    documentation and/or other materials provided with the distribution.
* 3. The name of the author may not be used to endorse or promote products
*    derived from this software without specific prior written permission.
* 
* THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
* IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
* OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
* IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
* NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
* THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

**/

var BVD = BVD || {};
BVD.utils = {};

BVD.utils.do_ajax = function (type, url, data, success, error) {
	

    return $.ajax({
            url: url,
	        type: type,
	        data: data,
	        headers: {
	               "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
	        },
	        success: success,
	        error: error
	    });
}

BVD.utils.validate_email = function(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
} 

BVD.utils.save_widgets = function() {
	var widgets = {};
	var list = [];
	for (hostname in BVD.widget_map) {
		var $widgets = BVD.widget_map[hostname];
		for (i=0; i < $widgets.length; i++) {
			$widget = $widgets[i];
			data = Widget.render.getWidgetDimensions($widget);
			data['hostname'] = hostname;
    		data['displayname'] = $widget.displayname;
    		data['jobname'] = $widget.jobname;
    		data['status'] = $widget.status;
    		data['icon'] = $widget.icon;
    		list.push(data);
		}
	}
	widgets['widgets'] = JSON.stringify(list);
	BVD.utils.do_ajax('post','/pull/save_jobs/',widgets);
}

BVD.utils.remove_old_widgets = function() {
	$.each($("#widgets").children(),function(){
    	$(this).remove();
    });
}

BVD.utils.create_new_widget = function(json) {
    var count = $(".widget").length;
    var $widget = new Widget(json.hostname, json.jobname, json.displayname, json.status, json.pk, count, false, json.icon, json.timeSinceLastSuccess);
    
    if (typeof(BVD.widget_map[json.hostname]) != 'undefined') {
        BVD.widget_map[json.hostname].push($widget);
    } else {
        $widgets = [$widget];
        BVD.widget_map[json.hostname] = $widgets;
    }
    
    BVD.utils.set_size_of_widgets(count);
    BVD.utils.save_widgets();
   
}


BVD.utils.set_size_of_widgets = function(count) {
    
    var $prev_widget = $("<div></div>");
    var counter = 0;
    var db_map = {};
    var db_list = [];
    for (hostname in BVD.widget_map) {
		$widgets = BVD.widget_map[hostname];
		for (i=0; i < $widgets.length; i++) {
		    if (counter == 0) {dimensions = {left : '0px', top: '0px'}}
		    else {dimensions = Widget.render.getWidgetDimensions($prev_widget);}
			var $current_widget = $widgets[i];
			
			$current_widget.set_size(count);
			$prev_widget = $current_widget;
		    counter++;
		}
	}
	
	db_list.push(db_map);
	
	return db_list;
}


BVD.utils.redraw_widgets = function(data) {
	BVD.widget_map = {};
	$.each(data[0].jobs, function(){
        $.each(this, function() {
    		var count = $(".widget").length;
    		$widget = new Widget(this.hostname,this.jobname,this.displayname,this.status,this.pk,count,this.readonly, this.icon, this.timeSinceLastSuccess);
    		Widget.render.draw($widget,this.width,this.height);
    			
    		if (typeof(BVD.widget_map[this.hostname]) != 'undefined') {
    			BVD.widget_map[this.hostname].push($widget);
    		} else {
    			$widgets = [$widget];
    			BVD.widget_map[this.hostname] = $widgets; 
    		}
        });
	});
}


