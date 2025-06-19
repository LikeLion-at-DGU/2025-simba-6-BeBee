from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from . models import *
from datetime import datetime, date
# Create your views here.

def start_timer(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    now = datetime.now().time()
    todo.started_at = now
    todo.ended_at = None
    todo.elapsed_time = None
    todo.save()
    return redirect('planner:todo_create') 

def stop_timer(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    now = datetime.now().time()
    todo.ended_at = now
    start_dt=datetime.combine(date.today(),todo.started_at)
    end_dt=datetime.combine(date.today(),todo.ended_at)
    todo.elapsed_time = end_dt-start_dt
    todo.save()
    return redirect('planner:todo_create')  

def todo_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # 로그인 URL 네임에 맞게 필요시 수정
    if request.method == 'POST':
        new_todo=Todo()
        if request.user.is_authenticated:
            new_todo.user=request.user
        new_todo.content=request.POST['content']
    
        new_todo.status=request.POST.get('status','not_completed')
        new_todo.category=request.POST['category']
        new_todo.deadline=request.POST.get('deadline',None)

        new_todo.save()
        return redirect('planner:todo_create') 

    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)

    return render(request, 'planner/subpage.html', {'todos': todos})
