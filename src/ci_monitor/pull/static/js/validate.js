var password_txt = ['txt_password1','txt_password2'];
var call_ajax = ['hostname','jobname'];

var blur_success = function(data,$this) {
	data = eval(data);
	
	if (data[0].status == 200){
		$("#" + $this.attr('id') + "_err").css('display','none');
	} else {
		$("#" + $this.attr('id') + "_err").css('display','block');
	}
}

var txtfield_blur = function(txt_map, $this) {
	if ($this.val() == '') {
		$this.val(txt_map[$this.attr('id')]['value']);
		return;
	} 
        
	var data = {};
	for (id in txt_map) {data[id] = $("#" + id + "").val();}
	   
	if ($.inArray($this.attr('id'), call_ajax) > -1) {
		do_ajax('post', get_url($this.attr('id')), data, function(data){blur_success(data,$this)});
	}
}

var passfield_blur = function($this) {
	if ($this.val() == '') {
		id = 'txt_' + $this.attr('id');
		$this.css('display','none');
		$pass = $("#"+id+"");
		$pass.css('display','block');
	}
}

var replace_txt_with_password = function(id) {
	var id1 = id.replace('txt_','');
	$("#" + id1+ "").css('display','block');
	$("#" + id + "").css('display','none');
	$("#" + id1+ "").focus();		
}
var clear_fields = function (txt_map, $this) {
	if ($.inArray($this.attr('id'),password_txt) > -1) {
		replace_txt_with_password($this.attr('id'));
		return;
	}
	
	$("#" + $this.attr('id') + "_err").css('display','none');
	
	if ($this.val().toUpperCase() == txt_map[$this.attr('id')]['value'].toUpperCase()) {
		$this.val('');
	}
}