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

/**

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

*/