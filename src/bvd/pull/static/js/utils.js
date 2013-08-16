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

BVD.utils.remove_old_widgets = function() {
	$.each($("#widgets").children(),function(){
    	$(this).remove();
    });
}

BVD.utils.create_new_widget = function(json) {
    var count = $(".widget").length;
    var $widget = new Widget(json.hostname, json.jobname, json.displayname, json.status, json.pk, count, false, json.icon, json.timeSinceLastSuccess);    
    BVD.utils.set_size_of_widgets(count);
}


BVD.utils.set_size_of_widgets = function(count) {
    /*
        This function sets the size of the widget based on the current number of
        widgets on the screen. It assumes that widgets will never be larger
        than 1000 pixels square or smaller than 100 pixels square, the latter
        of which is more than reasonable because past that size widgets are no
        longer very readable, especially for large displaynames.

        It does this by creating a dictionary of acceptable widget sizes based on
        the current window dimensions. This dictionary is generated on each resize
        because:
            A) widget resizes are often triggered by window resizes
            B) variable scope
            C) it doesn't appear to be a performance problem

        Essentially, the resulting dictionary is treated as a piecewise function
        where the key is the bottom of a range of widget quantities that fit
        in the window. The first for loop gerenates the dictionary by dividing
        the window width and height by a series of different possible widget sizes
        to determine what quantities of widgets need to be what size.

        The second for loop chooses a size from that dictionary by finding the largest
        value less than or equal to the number of widgets. As a final tweak to widget
        sizing it also subtracts a certain amount from the size of the widget based on
        a simple linear function of the number of widgets. This ensures that the large
        widgets fill as much of the screen as possible while the small widgets don't
        overflow past the screen and require scrolling.
    */

    var window_height = window.innerHeight;
    var window_width = window.innerWidth;

    var sizes = {};
    var n = 0;
    for(var s = 1000; s >= 100; s = s-10) {
        n = Math.floor(window_height/s) * Math.floor(window_width/s);
        sizes[n] = s;
    }

    var size = 200;
    for(n = count; n >= 0; n--) {
        if(sizes[n] != undefined) {
            size = sizes[n] - (-0.5*n + 50);
            break;
        }
    }

    $.each($('.widget'), function() {
        $(this).css('height',size+'px');
        $(this).css('width',size+'px');
    });
}


BVD.utils.draw_widgets = function(data) {
	$.each(data[0].jobs, function(product, jobs){
        if(product == 'no_product') {
            product = undefined;
        }
        $.each(jobs, function() {
    		var count = $(".widget").length;
    		$widget = new Widget(this.hostname,this.jobname,this.displayname,this.status,this.pk,count,this.readonly, this.icon, this.timeSinceLastSuccess, product);
    		Widget.render.draw($widget,this.width,this.height);
        });
	});
}


