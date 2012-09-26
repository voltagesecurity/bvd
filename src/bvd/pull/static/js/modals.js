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
    
    $("#login").button();
    $("#logout").button();
    
    $("#login").on("click",function(){
    	BVD.login.load_login_form();
    });
    
    $("#logout").on("click",function(){
    	BVD.login.do_logout();
    });

    $("#add_job").on("click",function () {
    	BVD.jobs.add_job(txtfield_map);
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
    
    BVD.jobs.hostname_autocomplete();
    
    
});
