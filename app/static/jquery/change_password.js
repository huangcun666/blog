$(function () {
            var minpassword="<span class='alertc'>密码太短</span>";
            var maxpassword="<span class='alertc'>密码太长</span>";
            var alertpassword="<span class='alertc'>密码不能为空</span>";
            var confirmpassworder="<span class='alertc'>密码不匹配</span>";
            var errorpassworder="<span class='alertc'>密码错误</span>";
            $('.alert').fadeIn(1000).fadeOut(4000);
            if($('.alert').length>0){
                $('#old_password').css({'border':'2px solid #d45f5c','outline':'none'});
                $('#old_password').parent().append(errorpassworder);
            }
               $('#submit').click(function () {
                   $(this).css('outline','none');
                if ($('#old_password').val()==''){
                    $('#old_password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#old_password').parent().find('.alertc').detach();
                    $('#old_password').parent().append(alertpassword);
                    return false;
                }
                if ($('#password').val()==''){
                    $('#password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password').parent().find('.alertc').detach();
                    $('#password').parent().append(alertpassword);
                    return false;
                }
                if ($('#password2').val()=='') {
                    $('#password2').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password2').parent().find('.alertc').detach();
                    $('#password2').parent().append(alertpassword);
                    return false;
                  }
                  if($(this).parents().find('.alertc').length>0){
                      return false;
                  }
                  if($('#password').val()!=$('#password2').val()){
                      $('#password2').parent().append(confirmpassworder);
                  }
            });

               $('#old_password').focus(function () {
                   $(this).css('border','');
               }).blur(function () {
                   if($(this).val()!=''){
                       $(this).parent().find('span').detach();
                   }
               })
                 $('#password').focus(function () {
                   $(this).css('border','');
               }).blur(function () {
                   if($(this).val()!=''){
                       $(this).parent().find('span').detach();
                   }
               })
             $('#password2').focus(function () {
                   $(this).css('border','');
               }).blur(function () {
                   if($(this).val()!=''){
                       $(this).parent().find('span').detach();
                   }
               })
              $('#password').blur(function () {
                $(this).css('border',' 2px solid #969696');
                $(this).parent().find('.alertc').detach();
                if ($(this).val()!==''& $(this).val().length<6){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).parent().find('.password').detach();
                    $(this).parent().append(minpassword);
                }
                else if($(this).val()!==''& $(this).val().length>12){
                    $(this).css({'border': '2px solid #d45f5c','outline':'none'});
                    $(this).parent().find('.password').detach();
                    $(this).parent().append(maxpassword);
                }
            })
            $('#password').blur(function () {
                if($(this).val()!=''&$('#password2').val()!=''& $(this).val()==$('#password2').val()) {
                    $('#password2').css('border','');
                    $('#password2').parent().find('.alertc').detach();
                }
                else if($(this).val()!=''&$('#password2').val()!=''& $(this).val()!=$('#password2').val()){
                    $('#password2').parent().find('.alertc').detach();
                    $('#password2').parent().append(confirmpassworder);
                }
            })
              $('#password2').blur(function () {
                $(this).css('border',' 2px solid #969696');
                $(this).parent().find('.alertc').detach();
                if($(this).val()!=''& $('#password').val()!=''&$(this).val()!=$('#password').val()){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).parent().append(confirmpassworder);
                }
            });
        })