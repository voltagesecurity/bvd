var widget_map = {};

/**
	Class to create and return a widget object, inherited from JQuery's $("<div></div>").  
	
	A widget object is an icon on the screen representing
	a Jenkins build, that has either a success, failed, or down status
	
	The object returned can be later manipulated via helper methods
	to change state, set its position on the page, set its size, etc.
	
	@param job_name String 
*/
var Widget = function(job_name, status, counter){

	this.make_success = function() {
		this.addClass('success');
		this.removeClass('error');
		this.removeClass('down');
	}
	
	this.make_failure = function() {
		this.addClass('error');
		this.removeClass('success');
		this.removeClass('down');
	}
	
	this.make_down = function() {
	    this.addClass('down');
	    this.removeClass('success');
	    this.removeClass('error');
	}
	
	this.set_size = function(count, prev_left, prev_top, counter) {
		var size = String(0.5/Math.log(count));
		size = size.substring(2,5);
		size = (size.indexOf("0") == 0) ? size.substring(1,3) : size;	
		size = parseInt(size);
		
		var mod = 6;
		
		if (count <= 15) {mod = 5;}
		else if (count >= 50) {mod = 7;}
		
		var left = prev_left + size + 50;
		
		left = (counter % mod == 0 && left < 1400) ? 0 : left;
		
		var top = (counter % mod == 0 && left < 1400) ? (counter == 0) ? 0 : prev_top + size + 50  : prev_top
		
		this.css('height',size+'px');
		this.css('width',size+'px');
		this.css('left',left+'px');
		this.css('top',top+'px');
	}
	
	this.set_status = function(status) {
	    switch (status) {
    		case 'SUCCESS':
    			this.make_success();
    			break;
    		case 'FAILURE':
    			this.make_failure();
    			break;
    		case 'DOWN':
    		    this.make_down();
    		    break;
    		case '404':
    		    break;
    	}
	}
	
	this.resize = function(width,height) {
	    this.css('height',height+'px');
	    this.css('width',width+'px');
	}
	
	this.draw = function (width, height, left, top) {
	    this.css({'top' : top, 'width' : width, 'height' : height, 'left' : left});
	}
	
	this.refresh = function() {
	    var dimensions = this.getWidgetDimensions();
	    this.css(dimensions);
	}
	
	this.getWidgetDimensions = function() {
        var ele = document.getElementById(this.id);
        
        return { top: ele.style.top, left: ele.style.left, height: ele.style.height, width: ele.style.width };
    }
	
	this.init = function() {
	    
	    $.extend(this,$("<div></div>"));
	    
        this.job_name = job_name;
        this.status = status;
        
        this.attr('id','wdg'+counter);
        this.id = this.attr('id');
		$marquee = $('<div></div>');
		$marquee.html(this.job_name);
		this.attr('class','widget');
		this.css('position','absolute')
		this.append($marquee);
		this.set_status(this.status);
		$('#widgets').append(this);
		// $marquee.marquee();
		this.draggable({
		    stop : function(event,ui) {
		        alert($(this).css('left'));
		    }
		})
    }	
    
    this.init();
};
