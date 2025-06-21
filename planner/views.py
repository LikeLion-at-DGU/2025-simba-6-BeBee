from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Todo
from django.http import JsonResponse
from .models import *

from .models import Todo, Comment

from accounts.models import Profile
from datetime import datetime, date, timedelta

def subpage(request, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('planner:subpage', selected_date=timezone.now().strftime('%Y-%m-%d'))

    todos = Todo.objects.filter(user=request.user, date=date_obj)
    daily_goal = DailyGoal.objects.filter(user=request.user, date=date_obj).first()
    comments = Comment.objects.filter(date=date_obj).select_related('writer__profile').order_by('created_at')
    return render(request, 'planner/subpage.html', {'todos': todos, 'selected_date': selected_date, 'daily_goal':daily_goal, 'comments': comments,})

# def start_timer(request, todo_id):
#     todo = get_object_or_404(Todo, id=todo_id, user=request.user)
#     if not todo.started_at:
#         todo.started_at = timezone.now()
#         todo.save()
#     return redirect('planner:subpage', selected_date=todo.date.strftime('%Y-%m-%d'))

def start_timer(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if not todo.started_at:
        todo.started_at = timezone.now()
        todo.save()
        print(f"[START] 저장됨: {todo.started_at}")
    else:
        print(f"[START] 이미 존재: {todo.started_at}")
    return JsonResponse({'status': 'started', 'started_at': str(todo.started_at)})


# def stop_timer(request, todo_id):
#     todo = get_object_or_404(Todo, id=todo_id, user=request.user)
#     if todo.started_at:
#         elapsed_time = timezone.now() - todo.started_at
#         todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed_time
#         todo.started_at = None
#         todo.save()
#     return redirect('planner:subpage', selected_date=todo.date.strftime('%Y-%m-%d'))


# def stop_timer(request, todo_id):
#     todo = get_object_or_404(Todo, id=todo_id, user=request.user)
#     if todo.started_at:
#         elapsed_time = timezone.now() - todo.started_at
#         todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed_time
#         todo.started_at = None
#         todo.save()
#     return redirect('planner:subpage', selected_date=todo.date.strftime('%Y-%m-%d'))


def stop_timer(request, todo_id):
    print("✅ stop_timer 호출됨")  # ← 추가

    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if todo.started_at:
        now = timezone.now()
        print(f"✅ 종료 시간 기록 시도: {now}")  # ← 추가

        elapsed_time = now - timezone.make_aware(datetime.combine(todo.date, todo.started_at))
        todo.ended_at = now
        todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed_time
        todo.started_at = None
        todo.save()
    return redirect('planner:subpage', selected_date=todo.date.strftime('%Y-%m-%d'))


def todo_create(request, selected_date):
    if request.method == 'POST':
        if request.user.is_authenticated:
            raw_deadline = request.POST.get('deadline')
            
            Todo.objects.create(
                user=request.user,
                content=request.POST['content'],
                status='not_completed',
                category=request.POST['category'],
                date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
                deadline=datetime.strptime(raw_deadline, '%Y-%m-%d').date() if raw_deadline else None
            )
        else:
            return redirect('accounts:login')
    
    return redirect('planner:subpage', selected_date=selected_date)

def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.content = request.POST['content']
        todo.category = request.POST['category']
        raw_deadline = request.POST.get('deadline')
        todo.deadline = datetime.strptime(raw_deadline, '%Y-%m-%d').date() if raw_deadline else None
        todo.save()
    return redirect('planner:subpage', selected_date=todo.date.strftime('%Y-%m-%d'))

def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    selected_date = todo.date.strftime('%Y-%m-%d')
    todo.delete()
    return redirect('planner:subpage', selected_date=selected_date)

def todo_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if todo.status != 'completed':
        todo.status = 'completed'
        todo.save()

        try:
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
        except Profile.DoesNotExist:
            pass
            
    return redirect('planner:subpage', selected_date=todo.date.strftime('%Y-%m-%d'))


def write_goal(request, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        goal_text = request.POST.get('goal', '').strip()  #값이 없으면 ''빈 문자열로 설정
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date() #URL에서 받은 문자열을 datetime 객체로 바꾸어줌 .date()는 그 중 날짜만 뽑는다.

        if goal_text:
            goal_obj, created = DailyGoal.objects.get_or_create(user=request.user, date=date_obj)
            goal_obj.goal = goal_text
            goal_obj.save()

    return redirect('planner:subpage', selected_date=selected_date)

def update_goal(request, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        new_goal_text = request.POST.get('goal', '').strip()
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

        if new_goal_text:
            goal_obj = DailyGoal.objects.get(user=request.user, date=date_obj)
            goal_obj.goal = new_goal_text
            goal_obj.save()

    return redirect('planner:subpage', selected_date=selected_date)

def delete_goal(request, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    goal_obj = DailyGoal.objects.get(user=request.user, date=date_obj)
    goal_obj.delete()

    return redirect('planner:subpage', selected_date=selected_date)

def view_comment(request, selected_date):
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    if request.method == 'POST':
        new_comment =  Comment()

        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.date = date_obj
        new_comment.created_at =timezone.now()
        new_comment.save()
        return redirect('planner:subpage', selected_date=selected_date)

    
    elif request.method == 'GET':
        comments = Comment.objects.filter(date=date_obj).order_by('-created_at')
        return render(request, 'planner/subpage.html', {'comments': comments,
            'selected_date': selected_date})

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.writer:
        selected_date = comment.date.strftime('%Y-%m-%d')
        comment.delete()
        return redirect('planner:subpage', selected_date=selected_date)
    
    return redirect('planner:subpage', selected_date=timezone.now().strftime('%Y-%m-%d'))