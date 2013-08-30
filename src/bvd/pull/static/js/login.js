/**

* BVD v1.0

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

var BVD = BVD || {};
BVD.login = {};

apple_tv = false;

BVD.login.login_apple_tv = function() {
	data = {};
	data['view_tv'] = 1
	apple_tv = true;
	BVD.utils.do_ajax('post', BVD.data.get_url('login'), data, function(data){BVD.login.login_success(data);});
}

BVD.login.validate_login_form = function() {
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

BVD.login.login_success = function(data,$modal) {
	data = eval(data);
	if (data[0].status != 200) {
		$("#loginerror").css('display','block');
		$("#loginerror").html('Invalid login!');
	} else {
		if (typeof($modal) != 'undefined') {$modal.remove();}
		$("#login_modal").remove();
		$("#login").css('display','none');
		$("#logout").css('display','inline');
		$("#view_tv").css('display','none');
		$("#refresh").css('display','inline');

		if (data[0].readonly) {
			$("#add_job").css('display','none');
			$("#add_product").css('display', 'none');
		} else {
			$("#add_job").css('display','inline');
			$("#add_product").css('display', 'inline')
		}
		poll = new Poll();
		if(apple_tv != true) {
			poll.ajax('/pull/pull_jobs/');
		} else {
			poll.ajax('/pull/pull_apple_tv_jobs/')
		}
	}
}

BVD.login.login_ok_button = function ($modal) {
	if (!BVD.login.validate_login_form()) {return;}
	
	var txtfields = ['username', 'password1'];
	var data = {};
	$.each(txtfields,function(index,id){
		data[id] = $("#"+id+"").val();
	});
	BVD.utils.do_ajax('post', BVD.data.get_url('login'), data,function(data){BVD.login.login_success(data,$modal);});
}

BVD.login.load_login_form = function() {
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
    
    $modal = BVD.modal_factory(BVD.data.get_url('modal','?template=login'),id, opts);
	
	
}

BVD.login.logout_success = function() {
	
	$("#logout").css('display','none');
	$("#login").css('display','inline');
	$("#view_tv").css('display','inline');
	$("#refresh").css('display','none');
	
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
	
	BVD.utils.remove_old_widgets();

	$("#charts").remove();
	
	$modal = BVD.modal_factory(BVD.data.get_url('modal','?template=logout_success'),id, opts);
}

BVD.login.do_logout = function() {
	apple_tv = false;
	BVD.utils.do_ajax('post', BVD.data.get_url('logout'), {},function(data){BVD.login.logout_success();});	
}