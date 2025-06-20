from django.urls import path
from .views import *

app_name = "planner"
urlpatterns = [
    path('', subpage, name='subpage'), 
    path('start/<int:todo_id>/', start_timer, name='start_timer'),
    path('stop/<int:todo_id>/', stop_timer, name='stop_timer'),
    path('create/', todo_create, name='todo_create'),  
    path('update/<int:todo_id>/', todo_update, name='todo_update'),
    path('delete/<int:todo_id>/',todo_delete,name='todo_delete'),
    path('complete/<int:todo_id>',todo_complete,name='todo_complete'),
    
]