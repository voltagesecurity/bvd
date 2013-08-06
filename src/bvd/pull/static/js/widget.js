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
BVD.widget_map = {};

/**
	Class to create and return a widget object, inherited from JQuery's $("<div></div>").  
	
	A widget object is an icon on the screen representing
	a Jenkins build, that has either a success, failed, or down status
	
	The object returned can be later manipulated via helper methods
	to change state, set its position on the page, set its size, etc.
	
	@param job_name String 
*/
var Widget = function(hostname, jobname, displayname, status, id, counter, readonly, background_img){

	this.make_success = function() {
		this.addClass('success');
		this.removeClass('error');
		this.removeClass('down');
		this.removeClass('unstable');
	}
	
	this.make_failure = function() {
		this.addClass('error');
		this.removeClass('success');
		this.removeClass('down');
		this.removeClass('unstable');
	}
	
	this.make_down = function() {
	    this.addClass('down');
	    this.removeClass('success');
	    this.removeClass('error');
	    this.removeClass('unstable');
	    
	}
	
	this.make_unstable = function () {
	    this.addClass('unstable');
	    this.removeClass('success');
	    this.removeClass('error');
	    this.removeClass('down');
	}
	
	this.set_size = function(count) {
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
		
		this.css('height',size+'px');
		this.css('width',size+'px');
	}
	
	this.set_status = function(status) {
	    this.status = status;
	    switch (status) {
    		case 'SUCCESS':
    			this.make_success();
    			this.css('background-image', this.background_img);
    			break;
    		case 'FAILURE':
    			this.make_failure();
    			break;
    		case 'DOWN':
    		    this.make_down();
    		    break;
    		case 'UNSTABLE':
        	    this.make_unstable();
        	    break;
    		default:
    			this.make_success();
    	}
	}

    this.make_icon = function (self) {
    	$icon = $('<div>&nbsp;</div>');
		$icon.attr('class','icon');
		this.append($icon);
		
		$menu = $('<div></div>');
		$ul = $('<ul></ul>');
		
		$li = $('<li></li>');
		$li.html('Remove Job');
		$li.attr('class','menu-item');
		
		$li.hover(function(){
			$(this).addClass('menu-on');
		},function(){
			$(this).removeClass('menu-on');
		});
		
		$li1 = $('<li></li>');
		$li1.html('View Job');
		$li1.attr('class','menu-item');
		
		$li.click(function(){
			self.off('click');
			data = {};
			data['pk'] = self.pk;
			BVD.utils.do_ajax('post',BVD.data.get_url('remove'),data,function(data){
				//remove the element from the widget map
				var $widgets = BVD.widget_map[self.hostname];
				var index = 0;
				var $widget;
				for (i =0; i < $widgets.length; i++) {
					if ($widgets[i].pk == self.pk) {
						index = i;
						$widget = $widgets[i];
						break;
					}
				}
				$widgets.splice(index,1);
				$widget.remove();
				Widget.render.refresh_grid();
				BVD.widget_map[self.hostname] = $widgets;
				BVD.utils.set_size_of_widgets($(".widget").length);
				BVD.utils.save_widgets();
				setTimeout(500,function(){
					var poll = new Poll('/pull/pull_jobs/');
					poll.ajax();
				});
			});
		});
		
		$li1.hover(function(){
			$(this).addClass('menu-on');
		},function(){
			$(this).removeClass('menu-on');
		});
		
		$li1.click(function(){
			window.location.href = self.hostname + '/job/' + self.jobname;
		});

        $li2 = $('<li></li>');
        $li2.html('Edit Widget');
        $li2.attr('class', 'menu-item');

        $li2.hover(function() {
            $(this).addClass('menu-on');
        }, function() {
            $(this).removeClass('menu-on');
        });

        $li2.click(function() {
            var id = 'edit_widget';
            var $modal;
            var opts = {
                width: 400,
                height: 410,
                autoOpen: true,
                title: "Edit Widget: '" + self.displayname + "'",
                resizable: false,
                modal: true,
                beforeClose: function() {
                    $("#edit_widget_dialog").remove();
                },
            }
            $modal = BVD.modal_factory(BVD.data.get_url('modal', '?template=edit_widget&widget_id='+self.pk), id, opts);
            return false;
        });

		$li3 = $('<li></li>');
		$li3.html('Edit Image');


		$li3.hover(function(){
			$(this).addClass('menu-on');
		},function(){
			$(this).removeClass('menu-on');
		});

		$li3.click(function(){
			id = 'edit_image';
			var $modal;
	
			var opts =      {
        		width : 400,
    			height : 225,
        		autoOpen: true,
        		title: 'Edit Image',
        		resizable : false,
        		modal : true
    		}
    
    		$modal = BVD.modal_factory(BVD.data.get_url('modal','?template=edit_image&widget_id='+self.pk), id, opts);
    		return false;
		});
		
		$ul.append($li);
		$ul.append($li1);
        $ul.append($li2);
		$ul.append($li3);
		
		$menu.append($ul);
		
		$icon.append($menu);
		
		$icon.hover(function(){
			$(this).children(0).toggle();
			self.on('click',function(){
				return;
			});
		},function(){
			$(this).children(0).toggle();
			self.on('click',function(){

        		window.location.href = self.hostname + '/job/' + self.jobname;
        	});
		});
		
		$marquee = $('<div></div>');
		$marquee.html(this.displayname);
    }
	
	this.init = function() {
	    
	    $.extend(this,$("<div></div>"));
	    
	    var self = this;
	    
	    this.pk = id;
	    this.hostname = hostname;
        this.jobname = jobname;
        this.status = status;
        this.displayname = displayname;
        this.icon = background_img;
        this.background_img = 'url(/static/images/'+background_img+')';
        
        this.attr('id','wdg'+id);
        this.id = this.attr('id');

        if (!eval(readonly)) {
        	this.make_icon(self);
        } else {
        	$marquee = $('<div></div>');
			$marquee.html(this.displayname);	
        }
        
		this.attr('class','widget');

        $marquee.attr('class','marquee');
        $marquee.on('click', function() {
            window.location.href = self.hostname + '/job/' + self.jobname;     
        });
		this.append($marquee);
		this.set_status(this.status);
		
		Widget.render.add_widget(this);

    }	
    
    this.init();
};
