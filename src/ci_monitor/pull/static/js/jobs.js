var add_job_success = function(data) {
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

var add_job_ok_click = function() {
	if ($("#displayname").val().toUpperCase() == txt_map['displayname']['value'].toUpperCase() || $("#displayname").val() == '') {
			$("#displayname").val($("#jobname").val());
	}
	var data = {};
	for (id in txt_map) {data[id] = $("#" + id + "").val();}                            
    do_ajax('post', '/pull/retrieve_job/', data,add_job_success, function(data) {});
}

function add_job() {
	id = 'add_job_modal';
    var $modal;
    
    var buttons = [
    	{
        	text: "Ok",
            click: add_job_ok_click
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