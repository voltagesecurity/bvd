    var erd_display_line = function(pk, displayname, appletv_active, productname) {
        /*
            This function renders a job in the list of public display widgets in the Edit Public TV modal.

            1. Creates a div or list element for the job
            2. Adds the displayname to a span element
            3. Creates a button
            4. Assigns a callback to the button that changes the inactivity of the public display widget
            5. Adds the job to either the 'no_product' div or passes it to the product renderer.
        */
        if(productname == 'no_product') {
            productname = undefined;
        }
        if(productname != undefined) {
            var $erd_line = $("<li></li>");
        } else {
            var $erd_line = $("<div></div>");
        }
        $erd_line.addClass('erd_widget');
        
        var primary_btn_text = "";
        if(!appletv_active) {
            $erd_line.addClass('erd_fade');
            primary_btn_text = "Activate";
        } else {
            primary_btn_text = "Hide";
        }

        var label = $('<span id="' + pk + '_erdd_label">' + displayname + '</span>');
        $erd_line.append(label);
        
        var primary_btn = $('<div class="btn btn-primary erdd_primary_btn">' + primary_btn_text +
                            '<div style="display:none;">' + pk + '</div></div>');
        $erd_line.append(primary_btn);
        primary_btn.on("click", function() {
            if(primary_btn_text == "Hide") {
                primary_btn_text = "Activate";
                $erd_line.html($erd_line.html().replace("Hide", "Activate"));
                $erd_line.addClass('erd_fade');
                change_erdd_line_active(pk, false)
            } else {
                primary_btn_text = "Hide";
                $erd_line.html($erd_line.html().replace("Activate", "Hide"));
                $erd_line.removeClass('erd_fade');
                change_erdd_line_active(pk, true);
            }
        });

        if(productname != undefined) {
            erd_display_product(productname, $erd_line);    
        } else {
            if($("#erd_display_widgets .no_product").length == 0) {
                var widget_group = $("<div></div>");
                widget_group.attr('class','no_product');
                widget_group.addClass('erdd_widget_group');

                // To simplify logic for removing products, creates a hidden div so that the
                // product "garbage collector" just has to check if the product has <= 1 child
                widget_group.append($("<div style='display:none'></div>"));

                $("#erd_display_widgets").append(widget_group);
            }
            $("#erd_display_widgets .no_product").append($erd_line);
        }
    };

    var erd_display_product = function(productname, erd_line) {
        /*
            This function adds a job to a product in the Public Display widgets side of the Edit Public TV modal.

            1. Creates a unordered list element for the product if it does not exist.
            2. Adds the job to the prodcut.
        */
        if($("#erd_product_" + productname).length == 0) {
            var product = $("<ul></ul>");
            product.attr('id','erd_product_' + productname);
            product.attr('class','erdd_widget_group');

            var title = $("<li></li>");
            title.attr('class', 'erdd_productname');
            title.html(productname);

            product.append(title);

            $("#erd_display_widgets").append(product);
        }
        $("#erd_product_" + productname).append(erd_line);
    }

    var change_erdd_line_active = function(pk, appletv_active) {
        /*
            This is the callback assigned to the button created in erd_display_line.

            1. Posts data to the server to change the activity of the widget.
            2. Updates the screen behind the modal.
        */
        if(appletv_active == false) {
            BVD.utils.do_ajax('POST', '/pull/save_widget/',
                {
                    'widget_id': pk,
                    'entity_active': 'current',
                    'appletv': 'True'
                }, function() {
                    update_erdd();
                });
        } else {
            BVD.utils.do_ajax('post', '/pull/save_widget/',
                {
                    'widget_id': pk,
                    'entity_active': 'current',
                    'appletv': 'True',
                    'appletv_active': 'True'
                }, function() {
                    update_erdd();
                });
        }
        new Poll().ajax('/pull/pull_jobs/');
    };

    var update_erdd = function() {
        /*
            This function updates the list of public display widgets in the Edit Public Display modal.

            1. Pulls jobs from the display jobs view
            2. Passes each job to the erd_display_line function to be drawn on the page
            3. Checks all the product groupings to remove the ones that no longer have jobs ("garbage collector")
        */
        BVD.utils.do_ajax('get', '/pull/pull_all_display_jobs',{}, function(data) {
            data = eval(data);
            $("#erd_display_widgets .erd_widget").remove();
            $.each(data[0].jobs,function(productname, jobs) {
                $.each(jobs, function() {
                    erd_display_line(this.pk, this.displayname, this.appletv_active, productname);
                });
            });

            $.each($(".erdd_widget_group"), function() {
                if($(this).children().length <= 1) {
                    $(this).remove();
                }
            });
        });
    };