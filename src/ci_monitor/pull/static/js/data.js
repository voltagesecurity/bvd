function get_txtfield_map() {
	return {
    	hostname    : {url : '/pull/validate_hostname/', value : 'PLEASE ENTER JENKINS HOSTNAME'},
    	jobname     : {url : '/pull/validate_job/', value : 'PLEASE ENTER JOB NAME'},
    	displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'},
    	username    : {value: 'USERNAME'},
    	email       : {value: 'Email'}
	}
	
}