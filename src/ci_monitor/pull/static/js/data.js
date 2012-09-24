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

CIMonitor.data = {};

CIMonitor.data.urls = {
	hostname         : '/pull/validate_hostname/',
	jobname          : '/pull/validate_job/',
	retrieve_job     : '/pull/retrieve_job/',
	modal            : '/pull/get_modal',
	ac_hostname      : '/pull/autocomplete_hostname/',
	signup           : '/pull/signup/',
	username         : '/pull/validate_username/',
	login            : '/pull/login/',
	logout           : '/pull/logout/',
	remove           : '/pull/remove_job/'
}

CIMonitor.data.get_txtfield_map = function() {
	return {
    	hostname    : {value : 'PLEASE ENTER JENKINS HOSTNAME'},
    	jobname     : {value : 'PLEASE ENTER JOB NAME'},
    	displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'},
    	username    : {value: 'USERNAME'},
    	email       : {value: 'Email'}
	}
	
}

CIMonitor.data.get_url = function(key,querystring) {
	url = CIMonitor.data.urls[key];
	if (typeof(querystring) != 'undefined') {
		url = url + querystring;
	}
	return url;
}