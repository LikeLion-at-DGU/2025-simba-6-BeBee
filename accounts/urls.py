from django.urls import path
<<<<<<< HEAD
from .views import *

app_name = "accounts"
urlpatterns = [
    path('login/', login, name='login'),
    path('lpgout/', logout, name="logout"),
    path('signup/', signup, name='signup'),
    path('check-nickname/', check_nickname, name='check-nickname'), 
    path('check-nickname/', check_nickname, name='check_nickname'),
]

=======
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
>>>>>>> 851ff7b (WIP: accounts 앱 초기 구조 및 로그인 페이지 구현(#2))
