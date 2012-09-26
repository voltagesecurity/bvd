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

test("test validate email returns false", function(){
	actual = BVD.utils.validate_email('sam@me');
	equal(actual,false);
});


test("test validate email return true", function(){
	actual = BVD.utils.validate_email('sam@apple.me');
	equal(actual,true);
});

test("remove widgets", function(){
	var $widget = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 14, 0);
	var $widget2 = new Widget('http://www.google.com', 'test-job1', 'test1-job1', 'SUCCESS', 15, 0);

	BVD.utils.remove_old_widgets();
	equal($("#widgets").children().length,0);
});

//BVD.utils.create_new_widget

test("create new widget", function(){
	json = {
		hostname    : 'localhost:9080',
		jobname     : 'job1',
		displayname : 'job1',
		status      : 'SUCCESS',
		pk          : 16
	}

	BVD.utils.create_new_widget(json);

	var $widgets = BVD.widget_map['localhost:9080'];

	equal($widgets.length,1);

	var $widget = $widgets[0];
	equal($widget.pk,16);
	equal($widget.hostname, 'localhost:9080');
	equal($widget.jobname, 'job1');
	equal($widget.displayname,'job1');
	equal($widget.attr('class'),'widget success ui-draggable');


});

test("set size of widgets", function(){

	BVD.widget_map = {};

	json1 = {
		hostname    : 'localhost:8080',
		jobname     : 'job1',
		displayname : 'job1',
		status      : 'SUCCESS',
		pk          : 17
	}
	json2 = {
		hostname    : 'localhost:8080',
		jobname     : 'job2',
		displayname : 'job2',
		status      : 'FAILURE',
		pk          : 18
	}
	json3 = {
		hostname    : 'localhost:8080',
		jobname     : 'job3',
		displayname : 'job3',
		status      : 'DOWN',
		pk          : 19
	}

	BVD.utils.create_new_widget(json1);
	BVD.utils.create_new_widget(json2);
	BVD.utils.create_new_widget(json3);

	BVD.utils.set_size_of_widgets(3);

	var $widgets = BVD.widget_map['localhost:8080'];

	var $widget = $widgets[2];
	dimensions = $widget.getWidgetDimensions();
	equal(dimensions['width'],'455px');
	equal(dimensions['height'],'455px');
	equal(dimensions['top'],'0px');


});

