$(document).ready(function(){
    $(function() {
        board_num = getParameterByName("num");
        allData = {"viewer":getCookie("user_id")};
        $.ajax({
            type: 'GET',
            dataType: 'json',
            url: '/board/'+board_num,
            data: allData,
            success: function(data){
                console.log(data);
                for(var i=0; i<data.basic_info.length; i++){
                    $(".title>input").val(data.basic_info[i].title);
                    $("#contents").html(data.basic_info[i].contents.replaceAll("<br />", "\r\n"));
                }
                _showPage();
            }
        });
    });

    $(".post_edit").click(function (){
        var form = $('.edit')[0];
        var formData = new FormData(form);
        formData.append('user', getCookie("user_id"))
        formData.append('contents', $("#contents").val().replace(/(?:\r\n|\r|\n)/g, '<br />'));
        formData.append('id', board_num);
        $.ajax({
            type: 'patch',
            enctype: 'multipart/form-data',
            dataType: 'json',
            url: '/board/'+board_num,
            processData: false,
            contentType: false,
            cache: false,
            data: formData,
            success: function(data){
                console.log(data);
                if(data.message == "modification Complete"){
                    alert('수정 완료');
                    location.href="/boardlist/view?num="+board_num;
                }
                else{
                    alert('수정 실패');
                }
            }
        });
    });

    $(".upload-hidden1").on('change', function(fileValue){
        if(window.FileReader){
            var files=$('input[name="file"]')[0].files;
            if(files.length>5){
                alert("파일은 5개까지만 추가할 수 있습니다.");
                return false;
            }
            filename = files[0].name;
            for(var i=1; i<files.length; i++){
                filename += ', '+files[i].name;
            }
            //filename = $(this)[0].files[0].name;
        }
        else {
           filename = $(this).val().split('/').pop().split('\\').pop();
        }
        $(this).siblings('.upload1').val(filename);
    });
    $(".cancel").click(function(){
       location.href="/boardlist/view?num="+board_num;
    });
    $(".post_edit").click(function (){
        // var xhttp = new XMLHttpRequest();
        // var csrf_token = $('[name=csrfmiddlewaretoken]').val();
        // xhttp.open("PUT", "", true);
        // xhttp.setRequestHeader('X-CSRFToken', csrf_token);
        // xhttp.onload = () => {
        //     if(xhttp.status == 200){
        //         let result = xhttp.response;
        //         alert(result);
        //         return result;
        //     }
        //     else{
        //         alert("ERROR"+this.status);
        //     }
        // };
        // xhttp.send();
        // return false;
    })
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}