from django.urls import path
from .views import *

app_name = "planner"

urlpatterns = [
    path('subpage/<int:user_id>/<str:selected_date>/', subpage, name='subpage'),
    path('start/<int:user_id>/<int:todo_id>/<str:selected_date>/', start_timer, name='start_timer'),
    path('stop/<int:user_id>/<int:todo_id>/<str:selected_date>/', stop_timer, name='stop_timer'),
    path('create/<int:user_id>/<str:selected_date>/', todo_create, name='todo_create'),
    path('delete/<int:user_id>/<int:todo_id>/', todo_delete, name='todo_delete'),
    path('complete/<int:user_id>/<int:todo_id>/', todo_complete, name='todo_complete'),
    path('goal/write/<int:user_id>/<str:selected_date>/', write_goal, name='write_goal'),
    path('goal/update/<int:user_id>/<str:selected_date>/', update_goal, name='update_goal'),
    path('goal/delete/<int:user_id>/<str:selected_date>/', delete_goal, name='delete_goal'),
    path('comment/<str:selected_date>/', view_comment, name='comment'),
    path('comment/delete/<int:comment_id>/', comment_delete , name='comment_delete'),
    path('toggle/<int:user_id>/<int:todo_id>/', todo_complete, name='todo_toggle'),
    path('like/<int:user_id>/<str:selected_date>/', like_subpage , name='like_subpage'),
]


