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

Widget.render.add_widget = function(widget, product, readonly) {
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
            Widget.render.add_product(product, readonly);
            $('#product_' + product).eq(0).append(widget);
        } else {
            $('#product_' + product).eq(0).append(widget);
        }
    } else {
        widget.addClass('noproduct')
        $('#widgets').append(widget);
    }
}

Widget.render.add_product = function(product_name, readonly) {
    var product = $("<div></div>");
    product.attr('class', 'product');
    product.attr('id', 'product_' + product_name);

    var label = $('<div></div>');
    label.addClass('product-label');

    if(!eval(readonly)) {
        var icon = $('<div></div>');
        icon.addClass('product-icon');

        var menu = $('<div></div>');
        menu.addClass('product-menu');
        icon.hover(function() {
            $(this).children(0).toggle();
        },
        function(){
            $(this).children(0).toggle();
        });

        var list = $('<ul></ul>');

        var edit_product = $('<li></li>');
        edit_product.addClass('menu-item');
        edit_product.hover(function() {
            edit_product.addClass('menu-on');
        },
        function() {
            edit_product.removeClass('menu-on');
        });
        edit_product.html("Edit Product");
        edit_product.click(function() {
            var id = 'edit_product';
            var $modal;
            var opts = {
                width: 300,
                autoOpen: true,
                title: "Edit Product",
                resizable: false,
                modal: true,
                beforeClose: function() {
                    $("#edit_product").remove();
                }
            }
            $modal = BVD.modal_factory(BVD.data.get_url('modal', "?template=edit_product&productname="+product_name), id, opts);
        });

        var remove_product = $('<li></li>');
        remove_product.hover(function() {
            remove_product.addClass('menu-on');
        },
        function() {
            remove_product.removeClass('menu-on');
        });
        remove_product.html("Remove Product");
        remove_product.click(function() {
            BVD.utils.do_ajax('POST', '/pull/remove_product/', {
                productname: product_name
            },function() {
                new Poll().ajax('/pull/pull_jobs/');
            });
        });

        list.append(edit_product);
        list.append(remove_product);

        menu.append(list);
        icon.append(menu);
        label.append(icon);
    }

    var title = $('<a>' + product_name + '</a>');
    title.attr('href','/pull/product/'+product_name+'/');
    label.append(title);

    if(readonly) {
        title.addClass('readonly');
    }

    product.append(label);

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
    while(document.height > window.innerHeight) {
        size--;
        $.each($('.widget'), function() {
            Widget.render.resize($(this), size, size);
        });
        if(size <= 0) {
            break;
        }
    }
}

Widget.render.remove_widget = function(widget) {
	widget.remove();
}

Widget.render.resize = function(widget, width, height) {
    widget.css('height',height+'px');
    widget.css('width',width+'px');
}


