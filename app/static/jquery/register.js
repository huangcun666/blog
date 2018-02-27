$(function () {
            var alertemail="<span class='alertc'>请输入邮箱地址</span>";
            var alertpassword="<span class='alertc'>请输入邮箱密码</span>";
            var alertusermax="<span class='alertc'>用户名太长</span>";
            var minpassword="<span class='alertc'>密码太短</span>";
            var maxpassword="<span class='alertc'>密码太长</span>";
            var alerterroremail="<span class='alertc'>请输入正确的邮箱格式</span>";
            var confirmpassword="<span class='alertc'>请验证你的密码</span>";
            var confirmpassworder="<span class='alertc'>密码不匹配</span>";
            var alertuser="<span class='alertc'>请输入用户名</span>";

            $('#register-email').blur(function () {
                $(this).css('border',' 2px solid #969696');
                $(this).parent().find('.alertc').detach();
                if(( this.value!="" && !/.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) )){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).after(alerterroremail);
                    $(this).parent().find('.mail').detach();
                }else if (( this.value!="" && /.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) )){
                    $(this).parent().find('.alertc').detach();
                }
            });

                $('#register-email').focus(function () {
                     if($(this).val()!="" && !/.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) ) {
                         $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                     }else{
                         $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
                     }
                });

            $('#register').click(function () {
                if ($('#register-email').val()==''){
                    $('#register-email').parent().find('.alertc').detach();
                    $('#register-email').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#register-email').parent().append(alertemail);
                     if ($('#user').val()==''){
                    $('#user').parent().find('.alertc').detach();
                    $('#user').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#user').parent().append(alertuser);
                }
                if ($('#password').val()=='') {
                    $('#password').parent().find('.alertc').detach();
                    $('#password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password').parent().append(alertpassword);
                  }
                   if ($('#password1').val()==''){
                     $('#password1').parent().find('.alertc').detach();
                     $('#password1').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password1').parent().append(confirmpassword);
                  }
                    return false;
                }
                if ($('#user').val()==''){
                    $('#user').parent().find('.alertc').detach();
                    $('#user').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#user').parent().append(alertuser);
                if ($('#password').val()=='') {
                    $('#password').parent().find('.alertc').detach();
                    $('#password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password').parent().append(alertpassword);
                  }
                   if ($('#password1').val()==''){
                     $('#password1').parent().find('.alertc').detach();
                     $('#password1').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password1').parent().append(confirmpassword);
                  }
                    return false;
                }


                if ($('#password').val()=='') {
                    $('#password').parent().find('.alertc').detach();
                    $('#password').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password').parent().append(alertpassword);
                      if ($('#password1').val()==''){
                     $('#password1').parent().find('.alertc').detach();
                     $('#password1').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password1').parent().append(confirmpassword);
                  }
                    return false;
                }
                  if ($('#password1').val()==''){
                     $('#password1').parent().find('.alertc').detach();
                     $('#password1').css({'border':'2px solid #d45f5c','outline':'none'});
                    $('#password1').parent().append(confirmpassword);
                    return false;
                  }
                  if($(this).parents().find('.alertc').length>0){
                      return false;
                  }
                  if($('#password').val()!=$('#password1').val()){
                      $('#password1').parent().append(confirmpassworder);
                  }
                  $(this).val('正在注册...')
            });

            $('#user').blur(function () {
                $(this).css('border',' 2px solid #969696');
                $(this).parent().find('.alertc').detach();
                if($(this).val().length>8){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).after(alertusermax);
                }
            })
            $('#user').focus(function () {
                if($(this).val().length>8) {
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                }else {
                    $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
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
                if($(this).val()!=''&$('#password1').val()!=''& $(this).val()==$('#password1').val()) {
                       $(this).css('border',' 2px solid #969696');
                    $('#password1').parent().find('.alertc').detach();
                }
                else if($(this).val()!=''&$('#password1').val()!=''& $(this).val()!=$('#password1').val()){
                    $('#password1').parent().find('.alertc').detach();
                    $('#password1').parent().append(confirmpassworder);
                }
            })
                 $('#password').focus(function () {
                    if(($(this).val()!=''&$(this).val().length<6)|($(this).val()!=''&$(this).val().length>12)) {
                        $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    }else {
                        $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
                    }
                });

            $('#password1').blur(function () {
                $(this).css('border',' 2px solid #969696');
                $(this).parent().find('.alertc').detach();
                if($(this).val()!=''& $('#password').val()!=''&$(this).val()!=$('#password').val()){
                    $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                    $(this).parent().append(confirmpassworder);
                }
            });
            $('#password1').focus(function () {
                 if($(this).val()!=''& $(this).val()!=$('#password').val()) {
                     $(this).css({'border':'2px solid #d45f5c','outline':'none'});
                 }else {
                     $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
                 }
            });

            $('#register').hover(function () {
                $(this).css('background','#2ac011');
            },function () {
                $(this).css('background','#42c02e');
            })
            if($('.error-email').text().length>7){
                $('.error-email').show();
            }
            if($('.error-username').text().length>8){
                $('.error-username').show();
            }
         })