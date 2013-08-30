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

BVD.modal_factory = function(url, id, opts) {
    var $modal = $('<div id=\"'+id+'\"></div>').load(url).dialog(opts);
    return $modal;
}


$(function(){

	var txtfield_map = BVD.data.get_txtfield_map();
	
    $("#add_job").button();
    $("#add_product").button();
    
    $("#login").button();
    $("#logout").button();
    $("#view_tv").button();
    $("#refresh").button();
    $("#view_inactive_widgets").button();
    $("#edit_readonly_display").button();
    
    $("#login").on("click",function(){
    	BVD.login.load_login_form();
    });
    
    $("#logout").on("click",function(){
    	BVD.login.do_logout();
    });

    $("#view_tv").on("click",function(){
        BVD.login.login_apple_tv(); 
    });

    $("#view_rally").button().click(function() {
        window.location.href = '/pull/rally';
    });

    $("#refresh").on('click',function(){
        poll = new Poll();
        if(apple_tv != true) {
            poll.ajax('/pull/pull_jobs/');
        } else {
            poll.ajax('/pull/pull_apple_tv_jobs/')
        }
    });

    $("#view_inactive_widgets").on("click", function() {
        var id = 'inactive_widgets';
        var $modal;
        var opts = {
            width: 400,
            height: 385,
            autoOpen: true,
            title: "Inactive Widgets",
            resizable: false,
            modal: true,
            beforeClose: function() {
                $("#inactive_widgets_dialog").remove();
            }
        }
        $modal = BVD.modal_factory(BVD.data.get_url('modal', '?template=inactive_widgets'), id, opts);
        return false;
    });

    $("#edit_readonly_display").on("click", function() {
        var id = 'readonly_display';
        var $modal;
        var opts = {
            width: 800,
            height: 500,
            autoOpen: true,
            title: "Edit Public TV",
            resizable: false,
            modal: true,
            beforeClose: function() {
                $("#edit_readonly_display_dialog").remove();
            }
        }
        $modal = BVD.modal_factory(BVD.data.get_url('modal', '?template=edit_readonly_display'), id, opts);
        return false;
    });

    $("#add_job").on("click",function () {
    	BVD.jobs.add_job(txtfield_map);
    });

    $("#add_product").on("click", function() {
        var id = 'new_product';
        var $modal;
        var opts = {
            width: 300,
            autoOpen: true,
            title: "Add Product",
            resizable: false,
            modal: true,
            beforeClose: function() {
                $("#new_product").remove();
            }
        }
        $modal = BVD.modal_factory(BVD.data.get_url('modal', '?template=new_product'), id, opts);
    });
    
    $(document).on('focus', 'input[type=text]', function(){
    	BVD.validate.clear_fields(txtfield_map,$(this))
    });
    
    $(document).on('blur', 'input[type=text]', function () {
        BVD.validate.txtfield_blur(txtfield_map,$(this));
    });
    
    $(document).on('blur', 'input[type=password]', function () {
        BVD.validate.passfield_blur($(this));
    });
    
    
});
