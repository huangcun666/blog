$(function () {
    var maxlen = "<span class='alertc' style='color:#ea6f5a;'>长度不能超过5</span>";
    $('#name').blur(function () {
        $(this).css('border', '')
        $(this).parent().find('.alertc').detach();
        if ($(this).val().length > 5) {
            $(this).css({'border': '2px solid #d45f5c', 'outline': 'none'});
            $(this).parent().append(maxlen);
        } else {
            $(this).css('border', '');
        }
    })
    $('.writebtn').mouseenter(function () {
        $(this).css({'backgroundColor':'#ea584b','color':'#fff'});
    }).mouseleave(function () {
        $(this).css('backgroundColor','#ea6f5a');
    })
    $('.search-input').focus(function () {
        $('.form-wrapper').animate({width:'210px'},'slow');
    }).blur(function () {
        $('.form-wrapper').animate({width:'170px'},'slow');
    })
    $('.r').click(function () {
        var name=$(this).attr('name');
        var value=$(this).text();
        if (value=='关注'){
             $.getJSON("http://127.0.0.1:8000/user_follow/"+name,
            function(data){
      });
        $(this).removeClass('btn btn-primary r');
        $(this).addClass('btn btn-default r');
        $(this).text('已关注');
        }else {
            $.getJSON("http://127.0.0.1:8000/user_unfollow/"+name,
            function(data){
      });
        $(this).removeClass('btn btn-default r');
        $(this).addClass('btn btn-primary r');
        $(this).text('关注');
        }

    })
    $('.l').click(function () {
        var id=$(this).attr('id');
        var cla=$(this).attr('class');
        var love=parseInt($('.k').text());
        if(cla=='btn_like l') {
            $.getJSON("http://127.0.0.1:8000/love/" + id,
                function (data) {
                });
            $(this).removeClass('btn_like l');
            $(this).addClass('btn_like1 l');
            $('.j').removeClass('ic-like');
            $('.j').addClass('ic-unlike');
            $('.k').removeClass('ic-like1');
            $('.k').addClass('ic-unlike1');
            $('.k').text(love+1);
        }else {
            $.getJSON("http://127.0.0.1:8000/notlove/" + id,
                function (data) {
                });
            $(this).removeClass('btn_like1 l');
            $(this).addClass('btn_like l');
            $('.j').removeClass('ic-unlike');
            $('.j').addClass('ic-like');
            $('.k').removeClass('ic-unlike1');
            $('.k').addClass('ic-like1');
            $('.k').text(love-1);
            }
        })

})