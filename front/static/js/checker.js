$(document).ready(function(){
    $(".submit").click(function(){
        if($(".nikname").val()==""){
            alert("이름을 입력해주세요.");
            return false;
        }
        else if($(".email").val()==""){
            alert("아이디를 입력해주세요.");
            return false;
        }
        else if($(".pw").val()==""){
            alert("비밀번호를 입력해주세요.");
            return false;
        }
        else if($(".pw_check").val()==""){
            alert("비밀번호 확인을 입력해주세요.");
            return false;
        }
        else{
            var queryString = $("form[name=signForm]").serialize();

            $.ajax({
               type : 'post',
               url : '/user/',
               data : queryString,
               dataType : 'json',
               error : function (xhr, status, error){
                   alert(error);
               } ,
                success : function (json){
                    console.log(json);
                }
            });
       }
    });
});