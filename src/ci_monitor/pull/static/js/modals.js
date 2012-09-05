function modal_factory (url, id, opts) {
    var $modal = $('<div id=\"'+id+'\"></div>').load(url).dialog(opts);
    return $modal;
}

var txt_map = {
    hostname    : {url : '/pull/validate_hostname/', value : 'PLEASE ENTER JENKINS HOSTNAME'},
    jobname     : {url : '/pull/retrieve_job/', value : 'PLEASE ENTER JOB NAME'},
    displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'}
}

$(function(){


    $("#add_job").button();

    $("#add_job").on("click",function () {
    
        id = 'add_job_modal';
    
        var buttons = { buttons : 
                        { "One" : function() { 
                                $("#"+id+"").dialog("close");
                                }
                        }
                    }
                    
        var opts =      {
            		    width : 600,
            			height : 300,
                        autoOpen: true,
                        title: 'Adding a Jenkins Job',
                        resizable : false,
                        modal : true,
                        buttons: buttons
            		}
    
    
        var $modal = modal_factory('/pull/get_modal?template=add_job',id, opts);

    
    });
    
    $(document).on('focus', '#hostname, #jobname, #displayname', function () {
        $("#" + $(this).attr('id') + "_err").css('display','none');
        
        if ($(this).val().toUpperCase() == txt_map[$(this).attr('id')]['value'].toUpperCase()) {
            $(this).val('');
        }
    });
    
    $(document).on('blur', '#hostname, #jobname, #displayname', function () {
        var self = $(this);
        if ($(this).val() == '') {
            $(this).val(txt_map[$(this).attr('id')]['value']);
        }
        
        var data = {};
        for (id in txt_map) {data[id] = $("#" + id + "").val();}
        
        do_ajax('post', 
                    txt_map[self.attr('id')]['url'], 
                    data,
                    function () {$("#" + self.attr('id') + "_err").css('display','none');}, 
                    function() {$("#" + self.attr('id') + "_err").css('display','block');}
                );
        
    });
    
    
});
