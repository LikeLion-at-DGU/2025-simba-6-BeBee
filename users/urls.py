from django.urls import path
from .views import mypage, exchange_honey

app_name="users"
urlpatterns = [
    path('mypage/<int:user_id>/',mypage, name='mypage'),
    path('exchange/', exchange_honey, name='exchange_honey'),

]