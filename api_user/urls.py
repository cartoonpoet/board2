from django.urls import path
from . import views

app_name = 'api_user'
urlpatterns = [
    # User에 관한 API를 처리하는 view로 Request를 넘긴다.
    path('', views.UserView.as_view()),
    # User id 전달한다.
    path('<user_id>', views.UserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('group/', views.GroupView.as_view()),
]