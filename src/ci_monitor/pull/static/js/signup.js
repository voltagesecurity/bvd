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
