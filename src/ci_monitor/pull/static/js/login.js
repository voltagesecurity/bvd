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
