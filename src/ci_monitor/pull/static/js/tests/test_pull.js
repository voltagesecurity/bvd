test("draw a single defaultl widget ",function() {
	var obj = $('<div></div>');
	obj.text = 'default';
	obj.attr('class','widget');	
	obj.job_name = 'default';
	
	var widget = create_widget('default');
	
	equal(widget.text,obj.text);
	equal(widget.attr('class'),obj.attr('class'));
	equal(widget.length,obj.length);
	equal(widget.job_name,obj.job_name);

});

test("draw a success widget", function() {
	var obj = $('<div></div>');
	obj.text = 'green';
	obj.attr('class','widget success');
	obj.job_name = 'green';
	
	var widget = create_widget('green');
	widget.make_success();
	
	equal(widget.text,obj.text);
	equal(widget.attr('class'),obj.attr('class'));
	equal(widget.length,obj.length);
	equal(widget.job_name,obj.job_name);
});

test("draw an error widget", function() {
	var obj = $('<div></div>');
	obj.text = 'red';
	obj.attr('class','widget error');
	obj.job_name = 'red';
	
	var widget = create_widget('red');
	widget.make_failure();
	
	equal(widget.text,obj.text);
	equal(widget.attr('class'),obj.attr('class'));
	equal(widget.length,obj.length);
	equal(widget.job_name,obj.job_name);
});


test("create a set of widgets based on some json results", function(){
	json_results = [{'job_name' : 'job1', 'status' : 'success'}, {'job_name' : 'job2', 'status' : 'success'},{ 'job_name' : 'job3' , 'status' : 'failed'}]
	
	var obj = $('<div></div>');
	obj.text = 'job1';
	obj.attr('class','widget success');
	obj.job_name = 'job1';
	
	var obj1 = $('<div></div>');
	obj1.text = 'job3';
	obj1.attr('class','widget error');
	obj1.job_name = 'job3';
	
	create_widgets(json_results);
	
	equal(widget_map['job1'].text,obj.text);
	equal(widget_map['job1'].attr('class'),obj.attr('class'));
	equal(widget_map['job1'].length,obj.length);
	equal(widget_map['job1'].job_name,obj.job_name);
	
	
	equal(widget_map['job3'].text,obj1.text);
	equal(widget_map['job3'].attr('class'),obj1.attr('class'));
	equal(widget_map['job3'].length,obj1.length);
	equal(widget_map['job3'].job_name,obj1.job_name);
	
	
	
});