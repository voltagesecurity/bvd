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

	var base = function(counter) {
	 	
		$widget = $('<div></div>');
		$widget.attr('id','wdg'+counter);
		$marquee = $('<div></div>');
		$marquee.html(job_name);
		$widget.attr('class','widget');
		$widget.append($marquee);
		$('#widgets').append($widget);
//		$marquee.marquee();
		$widget.draggable({
		    stop : function(event,ui) {
		        alert($(this).css('left'));
		    }
		})
	}
	
	base();
	
	$widget.make_success = function() {
		this.addClass('success');
		this.removeClass('error');
		this.removeClass('down');
	}
	
	$widget.make_failure = function() {
		this.addClass('error');
		this.removeClass('success');
		this.removeClass('down');
	}
	
	$widget.make_down = function() {
	    this.addClass('down');
	    this.removeClass('success');
	    this.removeClass('error');
	}
	
	$widget.set_size = function(count,prev_left,prev_top,counter) {
		var size = String(0.5/Math.log(count));
		size = size.substring(2,5);
		size = (size.indexOf("0") == 0) ? size.substring(1,3) : size;	
		size = parseInt(size);
		
		var mod = 6;
		
		if ((count - 1) <= 10) {mod = 5;}
		else if ((count - 1) >= 50) {mod = 7;}
		
		var left = (prev_left != -1) ? prev_left + size + 50 : 0;
		
		left = (counter % mod == 0 && left < 1400) ? 0 : left;
		
		var top = (counter % mod == 0 && left < 1400) ? (counter == 0) ? 0 : prev_top + size + 50  : prev_top;
		
		
		this.css('height',size+'px');
		this.css('width',size+'px');
		this.css('left',left+'px');
		this.css('top',top+'px');
	}
	
	$widget.set_status = function(status) {
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
	
	$widget.resize = function(width,height) {
	    this.css('height',height+'px');
	    this.css('width',width+'px');
	}
	
	$widget.job_name = job_name;
	return $widget;
	
}