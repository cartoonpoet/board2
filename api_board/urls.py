from django.urls import path
from . import views

app_name = 'api_board'
urlpatterns = [
    # User에 관한 API를 처리하는 view로 Request를 넘긴다.
    path('', views.BoardView.as_view(), name='board_API'),
    path('write/', views.BoardView.as_view()),
    path('list/', views.BoardView.as_view()),
    path('<int:post_num>', views.BoardView.as_view(), name='board_API'),
]