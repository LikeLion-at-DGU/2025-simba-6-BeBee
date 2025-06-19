from django.urls import path
from .views import *

app_name = "planner"
urlpatterns = [
    path('subpage/', subpage, name='subpage'),
]
