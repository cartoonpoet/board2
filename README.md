# Django-rest-framework를 이용하여 로그인/게시판 구현하기

## Conditions
1. Frontend, Backend 분리한다.
2. CustomUserModel, Serializer, Group 사용한다.
3. DB Table 정규화 시킨다.
4. PEP8 Rule 적용한다.
5. RestFul API EndPoint 구성한다.


## Problems
### 1. 파이썬 내 한글 인코딩 문제
- 한글 파일 업로드시 DB내에는 한글로 정상적으로 저장이 되었으나 Serializer로 불러와서 IDE에 print하니까 한글 출력이 되지 않음.
- User Table에 있는 사용자 이름을 가져와서 print한 결과 출력이 정상적으로 됨. DB Table charset 문제 인듯?
해결 : 클라이언트 측에서 인코딩을 진행하여 html 태그에 넣어즘.
  
### 2. 게시물 상세보기에서 이전글, 다음글 문제
- 이전글을 클릭하면 게시물 번호에 -1을 해서 조회하는데 이전 게시물이 삭제되었으면 무한 로딩 발생
- 예) 22번 게시물에서 이전글 클릭시 21번 게시물 조회, 그러나 21번 게시물은 삭제되어서 무한 로딩
<br>해결방법 1 : 삭제시 게시물 번호 항상 정리
<br>해결방법 2 : Board api return data에 이전 게시물, 다음 게시물 번호 추가

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

- 'board/' : 게시판 API
  <br> └ POST 'board/write/' : 게시물 작성
  <br> └ GET 'board/list/' : 모든 게시물 조회
  <br> └ GET 'board/(post_num)' : 단일 게시물 조회
  
### 미비사항
#### 1) 서버 API측 유효성 검사 코드가 부분적으로 삽입되어 있음..
why? - 클라이언트 측에서 유효성 검사를 해주고 데이터를 전송하기 때문에 항상 올바른 데이터만 들어올 것이라 생각 했음. 서버를 어디서든 사용할 수 있는 API라고 생각하고 개발을 했어야 했다.
   