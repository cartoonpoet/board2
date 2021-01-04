from django.urls import path
from . import views

app_name = 'front'
urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('board/', views.board_page, name='board_page'),
    path('board/edit/', views.edit_page, name='edit_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('board/view/', views.view_page, name='view_page'),
]