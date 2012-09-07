function modal_factory (url, id, opts) {
    var $modal = $('<div id=\"'+id+'\"></div>').load(url).dialog(opts);
    return $modal;
}

var txt_map = {
    hostname    : {url : '/pull/validate_hostname/', value : 'PLEASE ENTER JENKINS HOSTNAME'},
    jobname     : {url : '/pull/validate_job/', value : 'PLEASE ENTER JOB NAME'},
    displayname : {value: 'PLEASE ENTER DESIRED DISPLAY NAME'},
    username    : {value: 'USERNAME'},
    email       : {value: 'Email'}
}



$(function(){


    $("#add_job").button();
    $("#login").button();
    
    $("#login").on("click",function(){
    	load_login_form();
    });

    $("#add_job").on("click",function () {
    
        

    
    });
    
    $(document).on('focus', 'input[type=text]', function () {
        $("#" + $(this).attr('id') + "_err").css('display','none');
        
        if ($(this).val().toUpperCase() == txt_map[$(this).attr('id')]['value'].toUpperCase()) {
            $(this).val('');
        }
    });
    
    $(document).on('blur', 'input[type=text]', function () {
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
