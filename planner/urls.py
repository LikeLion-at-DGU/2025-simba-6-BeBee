from django.urls import path
from .views import *

app_name = "planner"
urlpatterns = [
    path('subpage/<str:selected_date>/',subpage, name='subpage'),
    path('start/<int:todo_id>/', start_timer, name='start_timer'),
    path('stop/<int:todo_id>/', stop_timer, name='stop_timer'),
    path('create/<str:selected_date>/', todo_create, name='todo_create'),
    path('update/<int:todo_id>/', todo_update, name='todo_update'),
    path('delete/<int:todo_id>/',todo_delete,name='todo_delete'),
    path('complete/<int:todo_id>/',todo_complete,name='todo_complete'),
<<<<<<< Updated upstream
    path('goal/write/<str:selected_date>/', write_goal, name='write_goal'),
    path('goal/update/<str:selected_date>/', update_goal, name='update_goal'),
    path('goal/delete/<str:selected_date>/', delete_goal, name='delete_goal'),
=======
    path('comment/<int:id>/', view_comment, name='comment'),
>>>>>>> Stashed changes
]