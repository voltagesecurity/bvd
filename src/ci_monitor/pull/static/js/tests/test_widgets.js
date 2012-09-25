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

test("make a widget constructor",function() {
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 1, 0);

	equal($widget.pk,1);
	equal($widget.hostname, 'http://www.google.com');
	equal($widget.jobname, 'test-job1');
	equal($widget.displayname,'test1-job1');
	equal($widget.attr('class'),'widget success ui-draggable');
	equal($widget.children().length,2);
	equal($widget.children(0).children(0).children().length,1);

});

test("wat a widget failure", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 2, 0);
	$widget.make_failure();
	equal($widget.attr('class'),'widget ui-draggable error');

});

test("wat a widget down", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 3, 0);
	$widget.make_down();
	equal($widget.attr('class'),'widget ui-draggable down');

});

test("wat a widget unstable", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 4, 0);
	$widget.make_unstable();
	equal($widget.attr('class'),'widget ui-draggable unstable');

});


test("wat a widget success", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 5, 0);
	$widget.make_success();
	equal($widget.attr('class'),'widget success ui-draggable');

});

test("set size of first widget", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 6, 0);
	$widget.set_size(1,0,0,1);

	equal($widget.css('top'),'0px');

});

test("set size of 15th widget", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 7, 0);
	$widget.set_size(15,50,50,16);	

	equal($widget.css('top'),'50px');
});

test("set size of 50th widget", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 8, 0);
	$widget.set_size(50,50,50,51);	

	equal($widget.css('top'),'50px');
});

test("set widget success status", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 9, 0);
	$widget.set_status('SUCCESS');

	equal($widget.attr('class'),'widget success ui-draggable');
	equal($widget.status,'SUCCESS');
});


test("set widget failure status", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 10, 0);
	$widget.set_status('FAILURE');

	equal($widget.attr('class'),'widget ui-draggable error');
	equal($widget.status,'FAILURE');
});


test("set widget down status", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 11, 0);
	$widget.set_status('DOWN');

	equal($widget.attr('class'),'widget ui-draggable down');
	equal($widget.status,'DOWN');
});

test("draw widget", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 12, 0);
	$widget.draw(100,100,0,0);

	equal($widget.css('width'),'100px');
	equal($widget.css('height'),'100px');
	equal($widget.css('top'),'0px');
});

test("get widget dimensions", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 13, 0);
	$widget.draw(100,100,0,0);

	dimensions = $widget.getWidgetDimensions();

	equal(dimensions['width'],'100px');
	equal(dimensions['height'],'100px');
	equal(dimensions['top'],'0px');
});