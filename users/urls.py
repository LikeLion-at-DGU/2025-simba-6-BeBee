from django.urls import path
from .views import *

app_name="users"
urlpatterns = [
    path('mypage/<int:user_id>/',mypage, name='mypage'),
    path('exchange/', exchange_honey, name='exchange_honey'),
    path('update/<int:user_id>/', update_profile, name='update_profile'),
]