function modal_factory (url, id, opts) {
    var $modal = $('<div id=\"'+id+'\"></div>').load(url).dialog(opts);
    return $modal;
}

var txt_map = {
    hostname    : {url : '/pull/validate_hostname/', value : 'PLEASE ENTER JENKINS HOSTNAME'},
    jobname     : {url : '/pull/validate_job/', value : 'PLEASE ENTER JOB NAME'},
    displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'},
    username    : {value: 'USERNAME'},
    email       : {value: 'Email'}
}

function validate_signup() {
	if ($("#password1").val() == '' || $("#password2").val() == '') {
		$("#signuperror").css('display','block');
		$("#signuperror").html('Empty password fields');
		return false;
	}
	if ($("#password1").val() != $("#password2").val()) {
		$("#signuperror").css('display','block');
		$("#signuperror").html('Passwords do not match');
		return false;
	} 
	
	if (!validate_email($("#email").val())) {
		$("#signuperror").css('display','block');
		$("#signuperror").html('Invalid email');
		return false;
	} 
	$("#signuperror").css('display','none');
	return true;
	
}

function load_signup_form() {
	id = 'signup_modal';
	var $modal;
	
	var buttons = [
		{
			text: 'Signup',
			click: function() {
				if (!validate_signup()) {return;}
				
			}
		},
		{
			text: "Cancel",
			click: function() {
				$modal.remove();
			}
		},
		{
			text: 'Login',
			click: function() {
				$modal.remove();
				load_login_form();
			}
		}
	]
	var opts =      {
        width : 600,
    	height : 400,
        autoOpen: true,
        title: 'Signup',
        resizable : false,
        modal : true,
        buttons: buttons
    }
    
    
    $modal = modal_factory('/pull/get_modal?template=signup',id, opts);
}

function load_login_form() {
	id = 'login_modal';
	var $modal;
    	
    var buttons = [
    	{
    		text: 'Login',
    		click: function() {
    			
    		}
    	},
    	{
    		text: "Signup",
    		click: function() {
    			$modal.remove();
    			load_signup_form();
    		}
    	},
    	{
    		text: "Cancel",
    		click: function() {
    			$modal.remove();
    		}
    	}
    ]
    	
    var opts =      {
        width : 600,
    	height : 300,
        autoOpen: true,
        title: 'Login',
        resizable : false,
        modal : true,
        buttons: buttons
    }
    
    
    $modal = modal_factory('/pull/get_modal?template=login',id, opts);
}

$(function(){


    $("#add_job").button();
    $("#login").button();
    
    $("#login").on("click",function(){
    	load_login_form();
    });

    $("#add_job").on("click",function () {
    
        id = 'add_job_modal';
        var $modal;
    
        var buttons = [
                        {
                            text: "Ok",
                            click: function() {
                                if ($("#displayname").val().toUpperCase() == txt_map['displayname']['value'].toUpperCase() || $("#displayname").val() == '') {
                                    $("#displayname").val($("#jobname").val());
                                }
                                var data = {};
                                for (id in txt_map) {data[id] = $("#" + id + "").val();}
                                
                                do_ajax('post', 
                                            '/pull/retrieve_job/', 
                                            data,
                                            function(data) {
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
                                            }, 
                                            function(data) {}
                                        );
                                
                            }
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

    
    });
    
    $(document).on('focus', 'input[type=text]', function () {
        $("#" + $(this).attr('id') + "_err").css('display','none');
        
        if ($(this).val().toUpperCase() == txt_map[$(this).attr('id')]['value'].toUpperCase()) {
            $(this).val('');
        }
    });
    
    $(document).on('blur', 'input[type=text]', function () {
        var self = $(this);
        if ($(this).val() == '') {
            $(this).val(txt_map[$(this).attr('id')]['value']);
        }
        
        var data = {};
        for (id in txt_map) {data[id] = $("#" + id + "").val();}
        
        var success = function(data) {
            data = eval(data);
            if (data[0].status == 200){
                $("#" + self.attr('id') + "_err").css('display','none');
            } else {
                $("#" + self.attr('id') + "_err").css('display','block');
            }
        }
        
        do_ajax('post', txt_map[self.attr('id')]['url'], data, success);
        
    });
    
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
    
    
});
