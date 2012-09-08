var add_job_success = function(data,$modal) {
	data = eval(data);
	if (data[0].status != 100 && data[0].status != 500){
		$("#hostname_err").css('display','none');
			$("#hostname_err").html('Invalid URL');
			create_new_widget(data[0]);
			$modal.remove();
                                                    
	} else if (data[0].status == 100) {
		$("#hostname_err").css('display','block');
		$("#hostname_err").html('Job Already Exists!');
	} else {
		$("#hostname_err").css('display','block');
		$("#hostname_err").html('Server Error!');
	}
}

var add_job_ok_click = function($modal,txt_map) {
	if ($("#displayname").val().toUpperCase() == txt_map['displayname']['value'].toUpperCase() || $("#displayname").val() == '') {
			$("#displayname").val($("#jobname").val());
	}
	var data = {};
	for (id in txt_map) {data[id] = $("#" + id + "").val();}                            
    do_ajax('post', '/pull/retrieve_job/', data,function(data){add_job_success(data,$modal);});
}

function add_job(txt_map) {
	id = 'add_job_modal';
    var $modal;
    
    var buttons = [
    	{
        	text: "Ok",
            click: function(){add_job_ok_click($modal,txt_map);}
		},
		{
			text: "Cancel",
			click: function() { $modal.remove(); }
		}
	];
                    
	var opts =      {
		width : 600,
		height : 300,
		autoOpen: true,
		title: 'Adding a Jenkins Job',
		resizable : false,
		modal : true,
		buttons: buttons
	}
    
    
    $modal = modal_factory('/pull/get_modal?template=add_job',id, opts);
}

var hostname_autocomplete = function () {
	$(document).on('keyup','#hostname', function() {
        $(this).autocomplete({
            minLength : 2,
            source : function(request,response) {
                var data = {};
                data['txt'] = request.term;
                var result = do_ajax('post','/pull/autocomplete_hostname/',data,function(data) {response(eval(data))});
            }
        });
    });
}
