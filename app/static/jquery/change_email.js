$(function () {
                var alerterroremail="<span class='alertc'>请输入正确的邮箱格式</span>";
                var alertemail="<span class='alertc'>请输入新邮箱地址</span>";
                var alertpassword="<span class='alertc'>密码不能为空</span>";
                var minpassword="<span class='alertc'>密码太短</span>";
                var maxpassword="<span class='alertc'>密码太长</span>";
               $('#email').blur(function () {
                $(this).css('border','');
                $(this).parent().find('.alertc').detach();
                if(( this.value!="" && !/.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) )){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).after(alerterroremail);
                    $(this).parent().find('.mail').detach();
                }else if (( this.value!="" && /.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) )){
                    $(this).parent().find('.alertc').detach();
                }
            });

                $('#submit').click(function () {
                   $(this).css('outline','none');
                if ($('#email').val()==''){
                    $('#email').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#email').parent().find('.alertc').detach();
                    $('#email').parent().append(alertemail);

                    if ($('#password').val()==''){
                    $('#password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password').parent().find('.alertc').detach();
                    $('#password').parent().append(alertpassword);
                     }
                    return false;
                }
                if ($('#password').val()==''){
                    $('#password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password').parent().find('.alertc').detach();
                    $('#password').parent().append(alertpassword);
                    return false;
                }
                  if($(this).parents().find('.alertc').length>0){
                      return false;
                  }
            });

                $('#password').blur(function () {
                $(this).css('border','');
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
               })