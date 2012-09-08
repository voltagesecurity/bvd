function modal_factory (url, id, opts) {
    var $modal = $('<div id=\"'+id+'\"></div>').load(url).dialog(opts);
    return $modal;
}


$(function(){

	var txtfield_map = get_txtfield_map();
	
    $("#add_job").button();
    
    $("#login").button();
    $("#logout").button();
    
    $("#login").on("click",function(){
    	load_login_form();
    });

    $("#add_job").on("click",function () {
    	add_job(txtfield_map);
    });
    
    $(document).on('focus', 'input[type=text]', function(){
    	clear_fields(txtfield_map,$(this))
    });
    
    $(document).on('blur', 'input[type=text]', function () {
        txtfield_blur(txtfield_map,$(this));
    });
    
    $(document).on('blur', 'input[type=password]', function () {
        passfield_blur($(this));
    });
    
    hostname_autocomplete();
    
    
});
