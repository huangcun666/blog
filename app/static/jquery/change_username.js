$(function () {
    var alertuser="<span class='alertc'>请输入用户名</span>";
     var alertusermax="<span class='alertc'>用户名太长</span>";
    $('#submit').click(function () {
                    $('#username').parent().find('.alertc').detach();
            if ($('#username').val()==''){
                    $('#username').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#username').parent().append(alertuser);
                    return false
                }
                if($('#username').val()!=''&$('#username').val().length>9){
                    $('#username').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#username').after(alertusermax);
                    return false
                }
              })
            $('#username').blur(function () {
                $(this).css('border',' 2px solid #969696');
                $(this).parent().find('.alertc').detach();
                if($(this).val().length>8){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).after(alertusermax);
                }
            })
            $('#username').focus(function () {
                if($(this).val().length>8) {
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                }else {
                    $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
                }
            })

})