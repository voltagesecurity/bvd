var login_ok_button = function () {
	
}

var load_login_form = function() {
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
    
    
    $modal = modal_factory(get_url('modal','?template=login'),id, opts);
}
