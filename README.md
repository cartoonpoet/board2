# Django-rest-framework를 이용하여 로그인/게시판 구현하기

## Conditions
1. Frontend, Backend 분리한다. - ok
2. CustomUserModel, Serializer, Group(Many-to-Many) 사용한다. - ok
3. DB Table 정규화 시킨다. - ok
4. PEP8 Rule 적용한다. - ~ing
5. RestFul API EndPoint 구성한다. - ok
6. 중복 쿼리 - 최소화 시킴


## Problems
### 1. 파이썬 내 한글 인코딩 문제
- 한글 파일 업로드시 DB내에는 한글로 정상적으로 저장이 되었으나 Serializer로 불러와서 IDE에 print하니까 한글 출력이 되지 않음.
- User Table에 있는 사용자 이름을 가져와서 print한 결과 출력이 정상적으로 됨. DB Table charset 문제 인듯?
해결 : 클라이언트 측에서 디코딩을 하여 html 태그에 넣어즘.
  
### 2. 게시물 상세보기에서 이전글, 다음글 문제
- 이전글을 클릭하면 게시물 번호에 -1을 해서 조회하는데 이전 게시물이 삭제되었으면 무한 로딩 발생
- 예) 22번 게시물에서 이전글 클릭시 21번 게시물 조회, 그러나 21번 게시물은 삭제되어서 무한 로딩
<br>해결방법 1 : 삭제시 게시물 번호 항상 정리 - 삭제할 때 마다 다수의 컬럼들에 대해 num값을 재배치(수정) 시켜줘야 함 비효율적이라 생각이 듬.
<br>해결방법 2 : Board api return data에 이전 게시물, 다음 게시물 번호 추가 - 이 방법 선택하여 해결
<br>해결방법 3 : 전체 글 게시판에서 load시 불러온 게시물 배열을 현재 게시물의 이전, 다음에 위치한 게시물 번호 같이전송 - 이전 글 또는 다음 글 클릭시 해당 게시물은 전체 글 게시판에서 온게 아니기 때문에 이전 글, 다음 글 게시물의 번호를 가져오는게 불가능

### 3. Serializer Multiple Table Join 문제
- Board 테이블을 참조하면서 User, UserGroup도 불러와야 하는데 User는 불러와지나 UserGroup은 안불러와짐.
해결 : Board Serializer는 User의 id를 참조하고 있어서 불러와지는 것, Board와 User_Group은 연관관계가 없으므로 안 불러와짐. 따라서 UserGroup의 Join을 위한 Serailizer를 만들어서 사용함.
  
### 4. 게시물 삭제 기능 구현 중 삭제 버튼을 클릭 시 새로고침 되는 문제
- 서버 측에서 해당 게시물은 삭제가 되었으므로 해당 페이지를 새로고침하면 무한로딩이 발생한다.
해결 : e.preventDefault()를 사용하여 해결함. - 버튼은 A태그로 이루어져 있어서 링크 이동 속성인 href를 중단시킴으로써 새로고침이 발생하지 않음. 
  

## Page URL
- 'admin/' : 관리자 페이지
- '' : 로그인 페이지(메인화면)
  <br> └ GET 'boardlist/' : 메인 게시판 페이지
  <br> └ GET 'boardlist/edit/' : 게시판 작성 페이지
  <br> └ GET 'boardlist/view/?num='게시물 번호'' : 게시물 조회 페이지
  <br> └ GET 'signup/' : 회원가입 페이지
  <br> └ GET 'boardlist/modify/?num='게시물 번호' : 게시물 수정 페이지
  
- 'user/' : User API
  <br> └ GET 'user/' : 모든 사용자 정보 불러오기 
  <br> └ GET 'user/(user_id)' : 특정 사용자 정보 불러오기
  <br> └ POST 'user/' : 회원가입 
  <br> └ PATCH 'user/(user_id)' : 회원정보 수정 
  <br> └ DELETE 'user/(user_id)' : 회원탈퇴 
  <br> └ POST 'user/login/' : 로그인
  <br> └ DELETE 'user/login/' : 로그아웃 
  <br> └ POST 'user/group/' : 그룹 생성 
  <br> 

- 'board/' : 게시판 API
  <br> └ POST 'board/write/' : 게시물 작성
  <br> └ GET 'board/list/' : 모든 게시물 조회
  <br> └ GET 'board/(post_num)' : 단일 게시물 조회
  <br> └ PATCH 'board/(post_num)' : 단일 게시물 수정
  <br> └ DELETE 'board/(post_num)' : 단일 게시물 삭제

  
### 미비사항
#### 1) 서버 API측 유효성 검사 코드가 부분적으로 삽입되어 있음..
why? - 클라이언트 측에서 유효성 검사를 해주고 데이터를 전송하기 때문에 항상 올바른 데이터만 들어올 것이라 생각 했음. 서버를 어디서든 사용할 수 있는 API라고 생각하고 개발을 했어야 했다.
#### 2) AuthToken 인증 문제
why? - User가 로그인 시 AuthToken을 생성하여 DB에 저장 후 해당 토큰의 digest를 반환하는데 이 digest가 table에 저장되어 있는 digest 값과 다름. digest가 암호화되어 table에 삽입되는 것도 아님

## 의문사항
#### 1) 수정(patch) 또는 삭제(delete) 등등 각종 요청을 보낼 시 해당 작업을 수행하기 전에 해당 사용자의 권한 검사를 수행하는가? 아니면 오로지 수정 또는 삭제에 대한 데이터만 검사를 하는가?
- 만약 해당 사용자의 권한 검사까지 하게되면 해당 Http request에 대해 할일이 추가됨으로써 한가지 기능만 한다는 게 모호해지는 것이 아닌가? 하는 의문


## 데이터베이스 테이블 모델링
![db](https://user-images.githubusercontent.com/38898759/103713779-7e0dfc80-5000-11eb-8286-8af11633f4d0.png)
