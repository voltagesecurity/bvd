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

var Widget = Widget || {};
Widget.render = {};

Widget.render.add_widget = function(widget, product) {
    /*
        This function:
            - If the widget belongs to a product
                - Creates the product div if it doesn't exist
                - Adds the widget to the product
            - If the widget doesn't belong to a product
                - Adds the widget directly to div#widgets
    */
	if(product != undefined) {
        if($('#product_' + product).length == 0) {
            Widget.render.add_product(product);
            $('#product_' + product).eq(0).append(widget);
        } else {
            $('#product_' + product).eq(0).append(widget);
        }
    } else {
        widget.addClass('noproduct')
        $('#widgets').append(widget);
    }
}

Widget.render.add_product = function(product_name) {
    var product = $("<div></div>");
    product.attr('class', 'product');
    product.attr('id', 'product_' + product_name);

    var title = $('<p>' + product_name + '</p>');
    product.append(title);

    $("#widgets").append(product);
}

Widget.render.refresh_grid = function(animate) {
    BVD.utils.set_size_of_widgets($(".widget").length);
	if(animate) {
		$("#widgets").freetile({
			animate: true
		})
	} else {
		$("#widgets").freetile();
	}
    var size = $('.widget').eq(0).height();
    console.log(size);
    while(document.height > window.innerHeight) {
        console.log("make widgets smaller")
        size--;
        console.log(size);
        $.each($('.widget'), function() {
            Widget.render.resize($(this), size, size);
        });
    }
}

Widget.render.remove_widget = function(widget) {
	widget.remove();
}

Widget.render.resize = function(widget, width, height) {
    widget.css('height',height+'px');
    widget.css('width',width+'px');
}
	
Widget.render.draw = function (widget, width, height) {
    widget.css({ 'width' : width, 'height' : height });
}

Widget.render.refresh = function(widget) {
    var dimensions = this.getWidgetDimensions();
    widget.css(dimensions);
}

Widget.render.getWidgetDimensions = function(widget) {
	var ele = document.getElementById(widget.id);

    return { top: ele.style.top, left: ele.style.left, height: ele.style.height, width: ele.style.width };
}


