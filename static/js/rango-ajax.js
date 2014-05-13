$(document).ready(function() {
    $('#likes').click(function() {
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like_category/', {category_id: catid}, function(data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

    $('#suggestion').keyup(function(){
        var query;
        query= $(this).val();
        $.get('/rango/suggest_category/',{suggestion:query },function(data){
            $('#cats').html(data);
        });
    });

    $('.rango-add').click(function() {

        var title1;
        title1=$(this).attr("data-title");
        var url1;
        url1=$(this).attr("data-url");
        var catid1;
        catid1=$(this).attr("data-catid");
        $.get('/rango/auto_add_page/',{title:title1,url:url1,category_id:catid1},function(data){
            $('#page').html(data);

        });
        $(this).hide();
    });

});