/**

* CI-Monitor v1.0 A Continous Integration Monitoring Tool

* Copyright (c) 2012 Voltage Security
* All rights reserved.

* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions
* are met:
* 1. Redistributions of source code must retain the above copyright
*    notice, this list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright
*    notice, this list of conditions and the following disclaimer in the
*    documentation and/or other materials provided with the distribution.
* 3. The name of the author may not be used to endorse or promote products
*    derived from this software without specific prior written permission.
* 
* THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
* IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
* OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
* IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
* NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
* THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

**/
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
		$("#login_modal").remove();
		$("#login").css('display','none');
		$("#logout").css('display','block');
		redraw_widgets(data);
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
	
	var opts =      {
        width : 300,
    	height : 300,
        autoOpen: true,
        title: 'Login',
        resizable : false,
        modal : true
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
	
	remove_old_widgets();
	
	$modal = modal_factory(get_url('modal','?template=logout_success'),id, opts);	
}

var do_logout = function() {
	do_ajax('post', get_url('logout'), {},function(data){logout_success();});	
}