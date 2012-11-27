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
BVD.jobs = {};


BVD.jobs.add_job_success = function(data,$modal) {
	data = eval(data);
	if (data[0].status != 100 && data[0].status != 500 && data[0].status != 401){
		$("#hostname_err").css('display','none');
			$("#hostname_err").html('Invalid URL');
			BVD.utils.create_new_widget(data[0]);
			$modal.remove();
                                                    
	} else if (data[0].status == 100) {
		$("#hostname_err").css('display','block');
		$("#hostname_err").html('Job Already Exists!');
	} else if (data[0].status == 401) {
		$("#hostname_err").css('display','block');
		$("#hostname_err").html('Please login first!');
	} else {
		$("#hostname_err").css('display','block');
		$("#hostname_err").html('Server Error!');
	}
}

BVD.jobs.add_job_ok_click = function($modal,txt_map) {
	if ($("#displayname").val().toUpperCase() == txt_map['displayname']['value'].toUpperCase() || $("#displayname").val() == '') {
			$("#displayname").val($("#jobname").val());
	}
	var data = {};
	for (id in txt_map) {data[id] = $("#" + id + "").val();}
    BVD.utils.do_ajax('post', BVD.data.get_url('retrieve_job'), data,function(data){BVD.jobs.add_job_success(data,$modal);});
}

BVD.jobs.add_job = function(txt_map) {
	id = 'add_job_modal';
    var $modal;
    
    var buttons = [
    	{
        	text: "Ok",
            click: function(){BVD.jobs.add_job_ok_click($modal,txt_map);}
		},
		{
			text: "Cancel",
			click: function() { $modal.remove(); }
		}
	];
                    
	var opts =      {
		width : 600,
		height : 350,
		autoOpen: true,
		title: 'Adding a Jenkins Job',
		resizable : false,
		modal : true,
		buttons: buttons
	}
    
    
    $modal = BVD.modal_factory(BVD.data.get_url('modal','?template=add_job'),id, opts);
}

BVD.jobs.hostname_autocomplete = function () {
	$(document).on('keyup','#hostname', function() {
        $(this).autocomplete({
            minLength : 2,
            source : function(request,response) {
                var data = {};
                data['txt'] = request.term;
                var result = BVD.utils.do_ajax('post',BVD.data.get_url('ac_hostname'),data,function(data) {response(eval(data))});
            }
        });
    });
}
