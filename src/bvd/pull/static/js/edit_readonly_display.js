    var erd_display_line = function(pk, displayname, appletv_active) {
        $erd_line = $("<div></div>");
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
                    '<div style="display:none;">' + pk + '</div>');
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

        $("#erd_display_widgets").append($erd_line);
    };

    var change_erdd_line_active = function(pk, appletv_active) {
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
        BVD.utils.do_ajax('get', '/pull/pull_all_display_jobs',{}, function(data) {
            data = eval(data);
            $("#erd_display_widgets .erd_widget").remove();
            $.each(data[0].jobs,function() {
                $.each(this, function() {
                    erd_display_line(this.pk, this.displayname, this.appletv_active);
                });
            });
        });
    };