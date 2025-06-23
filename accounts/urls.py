from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    
    path('login/', login, name='login'),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name='signup'),
    path('check-nickname/', check_nickname, name='check-nickname'),
    path('buddypage/<int:user_id>/', buddypage, name='buddypage'), 
    path('follow/<int:id>/',follow, name='follow'),
    path('api/friend_profile/', friend_profile_api, name='friend_profile_api'),
    path('buddypage/partial_follow_lists/', follow_lists_partial, name='partial_follow_lists'),
]

