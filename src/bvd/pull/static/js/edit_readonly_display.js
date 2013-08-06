    var erd_display_line = function(pk, displayname, appletv_active) {
        var self = this;
        $.extend(this, $("<div></div>"));
        this.addClass('erd_widget');
        var primary_btn_text = "";
        if(!appletv_active) {
            this.addClass('erd_fade');
            primary_btn_text = "Activate";
        } else {
            primary_btn_text = "Hide";
        }

        var label = $('<span id="' + pk + '_erdd_label">' + displayname + '</span>');
        this.append(label);
        
        var primary_btn = $('<div class="btn btn-primary erdd_primary_btn">' + primary_btn_text +
                    '<div style="display:none;">' + pk + '</div>');
        this.append(primary_btn);
        primary_btn.on("click", function() {
            if(primary_btn_text == "Hide") {
                primary_btn_text = "Activate";
                $(this).html($(this).html().replace("Hide", "Activate"));
                $(this).parent().addClass('erd_fade');
                change_erdd_line_active(pk, false)
            } else {
                primary_btn_text = "Hide";
                $(this).html($(this).html().replace("Activate", "Hide"));
                $(this).parent().removeClass('erd_fade');
                change_erdd_line_active(pk, true);
            }
        });

        $("#erd_display_widgets").append(this);
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
                erd_display_line(this.pk, this.displayname, this.appletv_active);
            });
        });
    };