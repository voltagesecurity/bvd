var urls = {
	hostname         : '/pull/validate_hostname/',
	jobname          : '/pull/validate_job/',
	retrieve_job     : '/pull/retrieve_job/',
	modal            : '/pull/get_modal',
	ac_hostname      : '/pull/autocomplete_hostname/',
	signup           : '/pull/signup/'
}

function get_txtfield_map() {
	return {
    	hostname    : {value : 'PLEASE ENTER JENKINS HOSTNAME'},
    	jobname     : {value : 'PLEASE ENTER JOB NAME'},
    	displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'},
    	username    : {value: 'USERNAME'},
    	email       : {value: 'Email'}
	}
	
}

function get_url(key,querystring) {
	url = urls[key];
	if (typeof(querystring) != 'undefined') {
		url = url + querystring;
	}
	return url;
}
 