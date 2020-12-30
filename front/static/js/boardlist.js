$(document).ready(function(){
    $(".searching").click(function(){
        if($(".contents").val() == ""){
            alert('검색어를 입력하세요.');
            return false;
        }
        else{
            $("form").submit();
        }
    });
    $(".logout").click(function (){
        $.ajax({
            type: 'DELETE',
            dataType: 'json',
            url: '../user/login/',
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(result){

            }
        });
    });

});
var _showPage = function(){
    var loader = $("div.loader");
    var container = $("#wrap");
    loader.css("display", "none");
    container.css("display", "inline-block");
};