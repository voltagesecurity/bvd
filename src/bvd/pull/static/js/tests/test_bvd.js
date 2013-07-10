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

/*
 * Test Constants
 */

var margin_size = 20;
var widget_size = 200;
var widget_size_multiple = 1;
var widget_data = {
	hostname: "localhost:8000",
	jobname: "italian", // (The Italian Job)
	displayname: "italian",
	status: "SUCCESS",
	id: 42,
	count: 1,
	readonly: false,
	background_img: "nope.jpg"
};

/*
 * Test Helpers
 */

var create_test_widget = function(readonly) {
	if(readonly == undefined) {
		readonly = widget_data['readonly'];
	}
	return new Widget(widget_data['hostname'], widget_data['displayname'], widget_data['jobname'],
		widget_data['status'], widget_data['id'], widget_data['count'], readonly, widget_data['background_img']);
}

/*
 * Test Widget
 */

test("widget has correct data and attributes when initialized", function() {
	var widget = create_test_widget();

	ok(widget, "Can create widget: " + widget);
	equal(widget.hostname, widget_data['hostname'], "widget sets hostname");
	equal(widget.displayname, widget_data['displayname'], "widget sets displayname");
	equal(widget.jobname, widget_data['jobname'], "widget sets jobname");
	equal(widget.status, widget_data['status'], "widget sets status");
	equal(widget.background_img, "url(/static/images/" + widget_data['background_img'] + ")",
		"widget sets background_img");
	equal(widget.id, "wdg" + widget_data['id'], "widget sets widget id");
	equal(widget.attr('id'), "wdg" + widget_data['id'], "widget sets id attribute");
	ok($.find(widget.attr('class'), "widget"), "widget sets class attribute");
});

test("widget has only displayname when readonly", function() {
	var widget = create_test_widget(true);

	equal($($(widget.toArray()[0]).children()).length, 1, "readonly widget has only displayname marquee")
	equal($($(widget.toArray()[0]).children()[0]).html(), widget_data['displayname'], "readonly marquee has correct displayname");
});

test("widget has div.icon subtree when not readonly", function() {
	var widget = create_test_widget(false);

	ok($(".widget div.icon"), "widget has div.icon");
	ok($(".widget div.icon ul"), "widget has div.icon ul");
	equal($(".widget div.icon ul li").length, 3, "widget icon has three list elements");
});

test("status set only to success when status is changed to success", function() {
	var widget = new Widget();
	widget.set_status('SUCCESS');

	ok(widget.hasClass('success') &&
		!widget.hasClass('error') &&
		!widget.hasClass('down') &&
		!widget.hasClass('unstable'),
		"Set status as 'success'");
});

test("status set only to error when status is changed to error", function() {
	var widget = new Widget();
	widget.set_status('FAILURE');

	ok(widget.hasClass('error') &&
		!widget.hasClass('success') &&
		!widget.hasClass('down') &&
		!widget.hasClass('unstable'),
		"Set status as 'error'");
});

test("status set only to down when status is changed to down", function() {
	var widget = new Widget();
	widget.set_status('DOWN');

	ok(widget.hasClass('down') &&
		!widget.hasClass('error') &&
		!widget.hasClass('success') &&
		!widget.hasClass('unstable'),
		"Set status as 'down'");
});

test("status set only to unstable when status is changed to unstable", function() {
	var widget = new Widget();
	widget.set_status('UNSTABLE');

	ok(widget.hasClass('unstable') &&
		!widget.hasClass('error') &&
		!widget.hasClass('down') &&
		!widget.hasClass('success'),
		"Set status as 'unstable'");
});

/*
 * Test BVD.data
 */

test("correct url returned when get_url is called", function() {
	for(var key in BVD.data.urls) {
		equal(BVD.data.get_url(key), BVD.data.urls[key], "get_url returns " + key);
	}
	equal(BVD.data.get_url('hostname',"?q=bananas"), BVD.data.urls['hostname'] + "?q=bananas",
		"get url returns correct querystring");
});

/*
 * Test BVD.utils
 */

test("all widgets removed when remove_old_widgets() is called", function() {
	for(var count = 0; count < 3; count++) {
		new Widget();
	}

	equal($(".widget").length, 3, "created three widgets");
	
	BVD.utils.remove_old_widgets();

	equal($(".widget").length, 0, "destroyed all widgets");
});

test("BVD.utils saves widget when created", function() {
	var jqueryajax = $.ajax;

	$.ajax = function(data) {
		equal(eval(data.data.widgets).length, $(BVD.widget_map).length, "$.ajax called with correct number of widgets");
	}
	BVD.utils.create_new_widget(widget_data);

	$.ajax = jqueryajax;
});

test("invalid when email address does not contain '@'", function() {
	var invalid_email_result = BVD.utils.validate_email("notanemailaddress.com");
	ok(!invalid_email_result, "email without '@' not validated");
});

test("invalid when email address does not contain '.'", function() {
	var invalid_email_result = BVD.utils.validate_email("notanemail@address");
	ok(!invalid_email_result, "email without '.' not validated");
});

test("valid when email address contains '@' and '.'", function() {
	var valid_email_result = BVD.utils.validate_email("validemail@gmail.com");
	ok(valid_email_result, "email with '@' and '.' validated");
});