
$(document).ready(function(){

    board_num = getParameterByName("num");
    allData = {"viewer":getCookie("user_id")};

    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/board/'+board_num,
        data: allData,
        success: function(data){
            console.log(data);
            $(".title>h1").text(data.basic_info[0].title);
            $(".writer").text("작성자 : "+data.basic_info[0].user.name);
            $(".write_date").text(moment(data.basic_info[0].write_date).format("YYYY-MM-DD HH:MM"));
            $(".content").html(data.basic_info[0].contents);

            for(var i=0; i<data.file_info.length; i++){
                $(".download").append('<h1><a href="'+data.file_info[i].file+'" download>'+decodeURI(data.file_info[i].file.split("/")[3])+'</a></h1>')
            }
            var pre="/board/view?num=";
            var next="/board/view?num=";
            pre+=Number(board_num)-1;
            next+=Number(board_num)+1;

            $(".Previous>a").attr("href", pre);
            $(".next>a").attr("href", next);

            //같은 그룹인지 체크
            var equal_cnt=0;
            for(var i=0; i<data.viewer_info.length; i++){
                for(var o=0; o<data.writer_info.length; o++){
                    if(data.viewer_info[i].group_id == data.writer_info[0].group_id){
                        equal_cnt++;
                        break;
                    }
                }
            }

            // 같은 그룹 소속이면 0이 아님
            if(equal_cnt != 0){
                $(".modify").attr("href", "/boardlist/modify?num="+board_num);
                $(".delete>a").attr("href", "");
            }
            else{ //0이면 같은 그룹이 아님
                $(".modify").remove();
                $(".delete").remove();
            }

            _showPage();
        }
    });

    $(".delete>a").click(function (e){
        e.preventDefault();
        if(confirm('정말로 삭제하시겠습니까?')){
            $.ajax({
                type: 'DELETE',
                dataType: 'json',
                url: '/board/'+board_num,
                success: function(data){
                    console.log(data);
                    if(data.message == "Deleted") {
                        location.href = "/boardlist/";
                        return false;
                    }
                    else{
                        return false;
                    }

                }
            });
        }
    })
});