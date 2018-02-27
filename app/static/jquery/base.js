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

})