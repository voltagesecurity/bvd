var validate_signup = function() {
	if (!validate_email($("#email").val())) {
		$("#signuperror").css('display','block');
		$("#signuperror").html('Invalid email');
		return false;
	} 
	
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
	
	if ($("#username").val().toUpperCase() == 'username'.toUpperCase()) {
		$("#signuperror").css('display','block');
		$("#signuperror").html('Invalid username');
		return;
	}
	
	
	$("#signuperror").css('display','none');
	return true;
	
}

var signup_success = function (data, $modal) {
	data = eval(data);
	if (data[0].status != 200) {
		$("#signuperror").css('display','block');
		$("#signuperror").html('Server Error');
	} else {
		$modal.remove();
		$("#login").css('display','none');
		$("#logout").css('display','block');
	}
}

var do_signup = function($modal) {
	var txtfields = ['username', 'email', 'password1', 'password2'];
	var data = {};
	$.each(txtfields,function(index,id){
		data[id] = $("#"+id+"").val();
	});
	do_ajax('post', get_url('signup'), data,function(data){signup_success(data,$modal);});
}

var load_signup_form = function() {
	id = 'signup_modal';
	var $modal;
	
	var buttons = [
		{
			text: 'Signup',
			click: function() {
				if (!validate_signup()) {return;}
				do_signup($modal);
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
    
    
    $modal = modal_factory(get_url('modal','?template=signup'),id, opts);
}
