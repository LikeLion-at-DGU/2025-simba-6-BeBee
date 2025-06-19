from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path('login/', login, name='login'),
    path('lpgout/', logout, name="logout"),
    path('signup/', signup, name='signup'),
]

