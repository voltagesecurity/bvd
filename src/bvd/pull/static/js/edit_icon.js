$(function () {
    
    $("#fileupload").fileupload({
        
        url: '/pull/edit_widget/',
        submit: function(e, data) {
        	$("#div_msg").css('display', 'block');
        	$("#file_name").html(data.files[0].name);
        	$(this).fileupload('send', data);
        	return false;
        },
        done : function(e, data) {
        	BVD.utils.remove_old_widgets();
    	    BVD.utils.redraw_widgets(eval(data.result));
    	    $("#edit_image").remove();
        },
        progressall: function (e, data) {
        	var progress = parseInt(data.loaded / data.total * 100, 10);
        	
        	$('#progressbar').css(
            	'width',
            	progress + '%'
        	);
    	}

    });

});
