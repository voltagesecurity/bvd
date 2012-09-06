function modal_factory (url, id, opts) {
    var $modal = $('<div id=\"'+id+'\"></div>').load(url).dialog(opts);
    return $modal;
}

var txt_map = {
    hostname    : {url : '/pull/validate_hostname/', value : 'PLEASE ENTER JENKINS HOSTNAME'},
    jobname     : {url : '/pull/validate_job/', value : 'PLEASE ENTER JOB NAME'},
    displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'}
}


$(function(){


    $("#add_job").button();

    $("#add_job").on("click",function () {
    
        id = 'add_job_modal';
        var $modal;
    
        var buttons = [
                        {
                            text: "Ok",
                            click: function() {
                                var data = {};
                                for (id in txt_map) {data[id] = $("#" + id + "").val();}
                                
                                do_ajax('post', 
                                            '/pull/retrieve_job/', 
                                            data,
                                            function(data) {
                                                data = eval(data);
                                                if (data[0].status != 500){
                                                    $("#hostname_err").css('display','none');
                                                    $("#hostname_err").html('Invalid URL');
                                                    create_new_widget(data[0]);
                                                    $modal.remove();
                                                    
                                                } else {
                                                    $("#hostname_err").css('display','block');
                                                    $("#hostname_err").html('Server Error!');
                                                }
                                            }, 
                                            function(data) {}
                                        );
                                
                            }
                        },
                        {
                            text: "Cancel",
                            click: function() { $modal.remove(); }
                        }
                    ];
                    
        var opts =      {
            		    width : 600,
            			height : 300,
                        autoOpen: true,
                        title: 'Adding a Jenkins Job',
                        resizable : false,
                        modal : true,
                        buttons: buttons
            		}
    
    
        $modal = modal_factory('/pull/get_modal?template=add_job',id, opts);

    
    });
    
    $(document).on('focus', '#hostname, #jobname, #displayname', function () {
        $("#" + $(this).attr('id') + "_err").css('display','none');
        
        if ($(this).val().toUpperCase() == txt_map[$(this).attr('id')]['value'].toUpperCase()) {
            $(this).val('');
        }
    });
    
    $(document).on('blur', '#hostname, #jobname', function () {
        var self = $(this);
        if ($(this).val() == '') {
            $(this).val(txt_map[$(this).attr('id')]['value']);
        }
        
        var data = {};
        for (id in txt_map) {data[id] = $("#" + id + "").val();}
        
        var success = function(data) {
            data = eval(data);
            if (data[0].status == 200){
                $("#" + self.attr('id') + "_err").css('display','none');
            } else {
                $("#" + self.attr('id') + "_err").css('display','block');
            }
        }
        
        do_ajax('post', txt_map[self.attr('id')]['url'], data, success);
        
    });
    
    $(document).on('keyup','#hostname', function() {
        $(this).autocomplete({
            minLength : 2,
            source : function(request,response) {
                var data = {};
                data['txt'] = request.term;
                var result = do_ajax('post','/pull/autocomplete_hostname/',data,function(data) {response(eval(data))});
            }
        });
    });
    
    
});
