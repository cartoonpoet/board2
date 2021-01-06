$(document).ready(function(){
    $(".next").click(function (){
        $(".selected").next().click();
        return false;
    });
    $(".pre").click(function (){
        $(".selected").prev().click();
        return false;
    })
    $(document).on("click", ".numbers", function (){
       $(".post").remove();
       if(store_data.length<=Number($(this).text())*10){
           for (var i = Number($(this).text())*10-10; i < store_data.length; i++) {
               $(".clasified").append('<div class="post"> <span>'+store_data[i].id+'</span><span><a href="view?num='+store_data[i].id+'">'+store_data[i].title+'</a></span> <span>'+moment(store_data[i].write_date).format("YYYY-MM-DD")+'</span> </div>');
           }
       }
       else{
           for (var i = Number($(this).text())*10-10; i < Number($(this).text())*10; i++) {
               $(".clasified").append('<div class="post"> <span>'+store_data[i].id+'</span><span><a href="view?num='+store_data[i].id+'">'+store_data[i].title+'</a></span> <span>'+moment(store_data[i].write_date).format("YYYY-MM-DD")+'</span> </div>');
           }
       }

       $(".numbers").removeClass("selected");
       $(this).addClass("selected");

       if(Math.ceil(store_data.length/10)==Number($(this).text())){ //마지막 페이지
           $(".next").css("display", "none");
           $(".pre").css("display", "inline-block");
       }
       else if(Number($(this).text())==1){//첫 페이지
           $(".next").css("display", "inline-block");
           $(".pre").css("display", "none");
       }
       else{
           $(".next").css("display", "inline-block");
           $(".pre").css("display", "inline-block");
       }

       return false;
    });
    $(".searching").click(function(){
        if($(".contents").val() == ""){
            alert('검색어를 입력하세요.');
            return false;
        }
        else{
            $(".post").remove();
            $(".numbers").remove();
            var filter_data = [];
            for(var i=0; i<backup_data.length; i++){
                if(backup_data[i].title.indexOf($(".contents").val()) != -1){
                    filter_data.push(backup_data[i]);
                }
            }
            store_data = filter_data;
            $(".search>span").text("□ 총 "+store_data.length+"건의 게시물");
            if(store_data.length>10) {
                for (var i = 0; i < 10; i++) {
                    $(".clasified").append('<div class="post"> <span>'+store_data[i].id+'</span><span><a href="view?num='+store_data[i].id+'">'+store_data[i].title+'</a></span> <span>'+moment(store_data[i].write_date).format("YYYY-MM-DD")+'</span> </div>');
                }
            }
            else{
                for (var i = 0; i < store_data.length; i++) {
                    $(".clasified").append('<div class="post"> <span>'+store_data[i].id+'</span><span><a href="view?num='+store_data[i].id+'">'+store_data[i].title+'</a></span> <span>'+moment(store_data[i].write_date).format("YYYY-MM-DD")+'</span> </div>');
                }
            }
            $(".pre").css("display", "none");
            if(Math.ceil(store_data.length/10)==1){
                $(".next").css("display", "none");
            }
            //페이지 수
            for(var i=1; i<=Math.ceil(store_data.length/10); i++){
                if(i==1) {
                    $(".next").before('<a href="" class="numbers selected">' + i + '</a>');
                }
                else{
                    $(".next").before('<a href="" class="numbers">' + i + '</a>');
                }
            }
        }
    });
    $(".logout").click(function (){
        $.ajax({
            type: 'DELETE',
            dataType: 'json',
            url: '../user/login/',
            data: {"user_token": getCookie("user_token")},
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(result){
                deleteCookie('user_id');
                deleteCookie('user_token');
                location.href="../"
            }
        });
    });

});
