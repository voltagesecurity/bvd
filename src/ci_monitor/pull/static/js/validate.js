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

var CIMonitor = CIMonitor || {};
CIMonitor.validate = {};

var password_txt = ['txt_password1','txt_password2'];
var call_ajax = ['hostname','jobname','username'];

CIMonitor.validate.blur_success = function(data,$this) {
	data = eval(data);
	
	if (data[0].status == 200){
		$("#" + $this.attr('id') + "_err").css('display','none');
	} else {
		$("#" + $this.attr('id') + "_err").css('display','block');
	}
}

CIMonitor.validate.txtfield_blur = function(txt_map, $this) {
	if ($this.val() == '') {
		$this.val(txt_map[$this.attr('id')]['value']);
		return;
	} 
        
	var data = {};
	for (id in txt_map) {data[id] = $("#" + id + "").val();}
	   
	if ($.inArray($this.attr('id'), call_ajax) > -1) {
		CIMonitor.utils.do_ajax('post', CIMonitor.data.get_url($this.attr('id')), data, function(data){CIMonitor.validate.blur_success(data,$this)});
	}
}

CIMonitor.validate.passfield_blur = function($this) {
	if ($this.val() == '') {
		id = 'txt_' + $this.attr('id');
		$this.css('display','none');
		$pass = $("#"+id+"");
		$pass.css('display','block');
	}
}

CIMonitor.validate.replace_txt_with_password = function(id) {
	var id1 = id.replace('txt_','');
	$("#" + id1+ "").css('display','block');
	$("#" + id + "").css('display','none');
	$("#" + id1+ "").focus();		
}

CIMonitor.validate.clear_fields = function (txt_map, $this) {
	if ($.inArray($this.attr('id'),password_txt) > -1) {
		CIMonitor.validate.replace_txt_with_password($this.attr('id'));
		return;
	}
	
	$("#" + $this.attr('id') + "_err").css('display','none');
	
	if ($this.val().toUpperCase() == txt_map[$this.attr('id')]['value'].toUpperCase()) {
		$this.val('');
	}
}