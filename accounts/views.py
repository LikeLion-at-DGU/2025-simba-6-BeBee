from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Todo
from datetime import datetime, date, timedelta

def subpage(request, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    todos = Todo.objects.filter(user=request.user, date=selected_date)
    return render(request, 'planner/subpage.html', {'todos': todos, 'selected_date': selected_date})

def start_timer(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    now = datetime.now().time()
    todo.started_at = now
    todo.ended_at = None
    todo.elapsed_time = None
    todo.save()
    return redirect('planner:subpage', selected_date=todo.date)

def stop_timer(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if not todo.started_at:
        return redirect('planner:subpage', selected_date=todo.date)

    now = datetime.now().time()
    todo.ended_at = now

    start_dt = datetime.combine(date.today(), todo.started_at)
    end_dt = datetime.combine(date.today(), now)
    elapsed = end_dt - start_dt

    todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed

    # 초기화
    todo.started_at = None
    todo.ended_at = None
    todo.elapsed_time = None

    todo.save()
    return redirect('planner:subpage', selected_date=todo.date)

def todo_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            new_todo = Todo()
            new_todo.user = request.user
            new_todo.content = request.POST['content']
            new_todo.status = request.POST.get('status', 'not_completed')
            new_todo.category = request.POST['category']
            raw_deadline = request.POST.get('deadline')
            new_todo.deadline = raw_deadline if raw_deadline else None
            new_todo.date = request.POST.get('date')  # 꼭 필요함 (기본 필터 키니까)
            new_todo.save()
            return redirect('planner:subpage', selected_date=new_todo.date)
        else:
            return redirect('accounts:login')
    return redirect('planner:subpage', selected_date=date.today())

def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.content = request.POST['content']
        todo.category = request.POST['category']
        raw_deadline = request.POST.get('deadline')
        todo.deadline = raw_deadline if raw_deadline else None
        todo.save()
    return redirect('planner:subpage', selected_date=todo.date)

def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    selected_date = todo.date
    todo.delete()
    return redirect('planner:subpage', selected_date=selected_date)

def todo_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if todo.status == 'completed':
        return redirect('planner:subpage', selected_date=todo.date)

    todo.status = 'completed'
    todo.save()

    profile = request.user.profile
    profile.completed_todo_count += 1

    today = timezone.now().date()
    HONEY_PER_TODO = 10
    DAILY_HONEY_CAP = 50

    if profile.last_honey_earned_date != today:
        profile.daily_honey_earned = 0
        profile.last_honey_earned_date = today

    if profile.daily_honey_earned < DAILY_HONEY_CAP:
        profile.honey_count += HONEY_PER_TODO
        profile.daily_honey_earned += HONEY_PER_TODO

    profile.save()
    return redirect('planner:subpage', selected_date=todo.date)
