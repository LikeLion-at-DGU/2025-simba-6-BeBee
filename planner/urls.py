from django.urls import path
from .views import *

app_name = "planner"
urlpatterns = [
    path('', todo_create, name='todo_create'),
    path('start/<int:todo_id>/', start_timer, name='start_timer'),
    path('stop/<int:todo_id>/', stop_timer, name='stop_timer'),
]
