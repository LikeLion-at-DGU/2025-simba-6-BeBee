from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from . models import *
from datetime import datetime, date
# Create your views here.

def subpage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    todos=Todo.objects.filter(user=request.user)
    return render(request, 'planner/subpage.html', {'todos': todos})

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
    if not todo.started_at:
        return redirect('planner:subpage')
    now = datetime.now().time()
    todo.ended_at = now
    start_dt=datetime.combine(date.today(),todo.started_at)
    end_dt=datetime.combine(date.today(),todo.ended_at)
    todo.elapsed_time = end_dt-start_dt
    todo.save()
    return redirect('planner:subpage')


def todo_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            new_todo = Todo()  # 객체 먼저 생성

            new_todo.user = request.user
            new_todo.content = request.POST['content']
            new_todo.status = request.POST.get('status', 'not_completed')
            new_todo.category = request.POST['category']
            raw_deadline = request.POST.get('deadline')
            new_todo.deadline = raw_deadline if raw_deadline else None


            new_todo.save()  # 마지막에 저장

        else:
            return redirect('accounts:login')

        return redirect('planner:subpage')

    return redirect('planner:subpage')


def todo_update(request, todo_id):
    new_todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        new_todo.content = request.POST['content']
        new_todo.category = request.POST['category']
        raw_deadline = request.POST.get('deadline')
        new_todo.deadline = raw_deadline if raw_deadline else None
        
        new_todo.save()
        return redirect('planner:subpage')
    # 만약 GET 요청이면, 수정 폼을 보여주거나, 그냥 subpage로 리다이렉트
    return redirect('planner:subpage')

def todo_delete(request, todo_id):
    todo_remove=get_object_or_404(Todo,id=todo_id,user=request.user)
    todo_remove.delete()
    return redirect('planner:subpage')