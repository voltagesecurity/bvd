var clear_fields = function (txt_map, txtfield) {
	$("#" + txtfield.attr('id') + "_err").css('display','none');
	if (txtfield.val().toUpperCase() == txt_map[txtfield.attr('id')]['value'].toUpperCase()) {
		txtfield.val('');
	}
}