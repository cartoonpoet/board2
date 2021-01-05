from django.urls import path
from . import views

app_name = 'front'
urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('boardlist/', views.board_page, name='board_page'),
    path('boardlist/edit/', views.edit_page, name='edit_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('boardlist/view/', views.view_page, name='view_page'),
    path('boardlist/modify/', views.modify_page, name='modify_page'),
]