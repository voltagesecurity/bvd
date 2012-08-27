
function createAsyncCounter(count) {
    count = count || 1; // count defaults to 1
    return function () { --count || start(); };
}

asyncTest("poll function errors because of 404", function() {
	var countDown = createAsyncCounter(1), // the number of async calls in this test

	expected = [{'status' : '404'}];
	
	var poll = new Poll('bad/url');
	
	poll.ajax().error(function(data) {
		ok(true,"Function has caused a 404");
	}).always(countDown);
	
});

asyncTest("function returns correct first result",2, function() {
	var countDown = createAsyncCounter(1), // the number of async calls in this test

	expected = {'job_name' : 'Job0', 'status' : 'success'};
	
	var poll = new Poll('/poll');
	
	poll.ajax().success(function(data) {
		ok(true,"Function has caused a 404");
		deepEqual(eval(data)[0],expected);
	}).always(countDown);
	
});

test("draw a single defaultl widget ",function() {
	var obj = $('<div></div>');
	obj.html('default');
	obj.attr('class','widget');	
	obj.job_name = 'default';
	
	var widget = create_widget('default');
	
	equal(widget.html(),obj.html());
	equal(widget.attr('class'),obj.attr('class'));
	equal(widget.length,obj.length);
	equal(widget.job_name,obj.job_name);

});

test("draw a success widget", function() {
	var obj = $('<div></div>');
	obj.html('green');
	obj.attr('class','widget success');
	obj.job_name = 'green';
	
	var widget = create_widget('green');
	widget.make_success();
	
	equal(widget.html(),obj.html());
	equal(widget.attr('class'),obj.attr('class'));
	equal(widget.length,obj.length);
	equal(widget.job_name,obj.job_name);
});


test("set size of widget  based on len of results", function() {
	count = 5;
	
	var exp1 = '180px';
	var exp2 = '200px';
	
	var widget = create_widget('green');
	widget.set_size(count);
	
	equal(widget.css('height'),exp1);
	equal(widget.css('line-height'),exp1);
	equal(widget.css('width'),exp2);
});

test("draw an error widget", function() {
	var obj = $('<div></div>');
	obj.html('red');
	obj.attr('class','widget error');
	obj.job_name = 'red';
	
	var widget = create_widget('red');
	widget.make_failure();
	
	equal(widget.html(),obj.html());
	equal(widget.attr('class'),obj.attr('class'));
	equal(widget.length,obj.length);
	equal(widget.job_name,obj.job_name);
});


test("create a set of widgets based on some json results", function(){
	json_results = [{'job_name' : 'job1', 'status' : 'success'}, {'job_name' : 'job2', 'status' : 'success'},{ 'job_name' : 'job3' , 'status' : 'failed'}]
	
	var obj = $('<div></div>');
	obj.html('job1');
	obj.attr('class','widget success');
	obj.job_name = 'job1';
	
	var obj1 = $('<div></div>');
	obj1.html('job3');
	obj1.attr('class','widget error');
	obj1.job_name = 'job3';
	
	create_or_update_widgets(json_results);
	
	equal(widget_map['job1'].html(),obj.html());
	equal(widget_map['job1'].attr('class'),obj.attr('class'));
	equal(widget_map['job1'].length,obj.length);
	equal(widget_map['job1'].job_name,obj.job_name);
	
	
	equal(widget_map['job3'].html(),obj1.html());
	equal(widget_map['job3'].attr('class'),obj1.attr('class'));
	equal(widget_map['job3'].length,obj1.length);
	equal(widget_map['job3'].job_name,obj1.job_name);
});
