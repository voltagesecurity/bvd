var validate_login_form = function() {
	if ($("#username").val().toUpperCase() == 'username'.toUpperCase()) {
		$("#loginerror").css('display','block');
		$("#loginerror").html('Invalid username');
		return false;
	}
	if ($("#username").val() == '' || $("#password1").val() == '') {
		$("#loginerror").css('display','block');
		$("#loginerror").html('Please fill in form');
		return false;
	}
	
	$("#loginerror").css('display','none');
	return true;
}

var login_success = function(data,$modal) {
	data = eval(data);
	if (data[0].status != 200) {
		$("#loginerror").css('display','block');
		$("#loginerror").html('Invalid login!');
	} else {
		$modal.remove();
		$("#login").css('display','none');
		$("#logout").css('display','block');
	}
}

var login_ok_button = function ($modal) {
	if (!validate_login_form()) {return;}
	
	var txtfields = ['username', 'password1'];
	var data = {};
	$.each(txtfields,function(index,id){
		data[id] = $("#"+id+"").val();
	});
	do_ajax('post', get_url('login'), data,function(data){login_success(data,$modal);});
}

var load_login_form = function() {
	id = 'login_modal';
	var $modal;
    	
    var buttons = [
    	{
    		text: 'Login',
    		click: function() {
    			login_ok_button($modal);
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
    
    
    $modal = modal_factory(get_url('modal','?template=login'),id, opts);
}

var logout_success = function() {
	
	$("#logout").css('display','none');
	$("#login").css('display','block');
	
	id = 'logout_modal';
	
	var $modal;
	
	var buttons = [
    	{
			text: "OK",
			click: function() { $modal.remove(); }
		}
		
	];
                    
	var opts =      {
		width : 600,
		height : 400,
		autoOpen: true,
		title: 'Logout complete!',
		resizable : false,
		modal : true,
		buttons: buttons
	}
	
	$modal = modal_factory(get_url('modal','?template=logout_success'),id, opts);	
}

var do_logout = function() {
	do_ajax('post', get_url('logout'), {},function(data){logout_success();});	
}