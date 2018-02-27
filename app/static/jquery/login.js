$(function () {
                var alertemail="<span class='alertc'>用户不能为空</span>";
                var alertpassword="<span class='alertc'>密码不能为空</span>";
                $('.alert').fadeIn(1000).fadeOut(4000);
                $('#submit').click(function () {
                $(this).parents().find('.alertc').detach();
                if ($('#email').val()==''){
                    $('#email').css({'border':'2px solid #d45f5c','outline': 'none'});
                    $('#email').parent().append(alertemail);
                    if ($('#password').val()=='') {
                    $('#password').css({'border':'2px solid #d45f5c','outline': 'none'});
                    $('#password').parent().append(alertpassword);
                  }
                    return false;
                }
                if ($('#password').val()=='') {
                    $('#password').css({'border':'2px solid #d45f5c','outline': 'none'});
                    $('#password').parent().append(alertpassword);
                    return false;
                  }
                  $(this).val('正在登录...');
            })
             $('#email').focus(function () {
                  $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
            }).blur(function () {
                if($(this).val()!='') {
                    $(this).parent().find('.alertc').detach();
                }
                 $(this).css('border', ' 2px solid #969696');
             });
            $('#password').focus(function () {
                  $(this).css({'border':'2px solid #2aabd2','outline': 'none'});
            }).blur(function () {
                $(this).css('border',' 2px solid #969696');
                if ($(this).val()!==''){
                    $(this).parent().find('.alertc').detach();
                }
            })
            $('.forgetpassword').hover(function () {
                $(this).css("color",'black');
            },function () {
                $(this).css('color','#86989B');
            })
              $('.remember_me').hover(function () {
                $(this).css("color",'black');
            },function () {
                $(this).css('color','#86989B');
            })
            $('#submit').hover(function () {
                $(this).css('background','#2985d0');
            },function () {
                $(this).css('background','#3194d0');
            })

            $('.register').hover(function () {
                $(this).css('background','#2ac011');
            },function () {
                $(this).css('background','#42c02e');
            })
         })