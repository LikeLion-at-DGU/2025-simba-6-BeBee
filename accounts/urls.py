from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name='signup'),
    path('check-nickname/', check_nickname, name='check-nickname'),
    path('buddypage/', buddypage, name='buddypage'), 
    path('follow/<int:id>/',follow, name='follow')
]

