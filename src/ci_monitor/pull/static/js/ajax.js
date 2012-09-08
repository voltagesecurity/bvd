var call_ajax = ['hostname','jobname'];

var blur_success = function(data) {
	data = eval(data);
	if (data[0].status == 200){
		$("#" + self.attr('id') + "_err").css('display','none');
	} else {
		$("#" + self.attr('id') + "_err").css('display','block');
	}
}

var txtfield_blur = function(txt_map, self) {
	if ($(this).val() == '') {
		$(this).val(txt_map[$(this).attr('id')]['value']);
	}
        
	var data = {};
	for (id in txt_map) {data[id] = $("#" + id + "").val();}   
	if (self.attr('id') in call_ajax) {do_ajax('post', txt_map[self.attr('id')]['url'], data, blur_success);}
}
