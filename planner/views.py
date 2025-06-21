from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime, timedelta
from accounts.models import Profile
from django.contrib.auth.models import User

# ⭐ user_id 변경: 전체 뷰에게 적용

def subpage(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    target_user = get_object_or_404(User, pk=user_id)
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('planner:subpage', user_id=user_id, selected_date=timezone.now().strftime('%Y-%m-%d'))

    todos = Todo.objects.filter(user=target_user, date=date_obj)
    daily_goal = DailyGoal.objects.filter(user=target_user, date=date_obj).first()

    comments = Comment.objects.filter(
    user_id=target_user.id,  # ❗ 댓글이 속한 사용자
    date=date_obj).select_related('writer__profile').order_by('created_at')

    return render(request, 'planner/subpage.html', {'todos': todos, 'selected_date': selected_date, 'daily_goal':daily_goal, 'comments': comments, 'target_user': target_user,
    'login_user': request.user,
    })

def start_timer(request, user_id, todo_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')


    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    if not todo.started_at:
        todo.started_at = timezone.now()
        todo.save()

    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)


def stop_timer(request, user_id, todo_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    if todo.started_at:
        now = timezone.now()
        elapsed_time = now - timezone.make_aware(datetime.combine(todo.date, todo.started_at))
        todo.ended_at = now
        todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed_time
        todo.started_at = None
        todo.save()

    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)


def todo_create(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        if request.user.id != user_id:
            return HttpResponseForbidden("권한이 없습니다.")

        target_user = get_object_or_404(User, pk=user_id)
        raw_deadline = request.POST.get('deadline')
        Todo.objects.create(
            user=target_user,
            content=request.POST['content'],
            status='not_completed',
            category=request.POST['category'],
            date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
            deadline=datetime.strptime(raw_deadline, '%Y-%m-%d').date() if raw_deadline else None
        )
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)

def todo_update(request, user_id, todo_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    if request.method == 'POST':
        todo.content = request.POST['content']
        todo.category = request.POST['category']
        raw_deadline = request.POST.get('deadline')
        todo.deadline = datetime.strptime(raw_deadline, '%Y-%m-%d').date() if raw_deadline else None
        todo.save()
    return redirect('planner:subpage', user_id=user_id, selected_date=todo.date.strftime('%Y-%m-%d'))

def todo_delete(request, user_id, todo_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    selected_date = todo.date.strftime('%Y-%m-%d')
    todo.delete()
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)

def todo_complete(request, user_id, todo_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    if todo.status != 'completed':
        todo.status = 'completed'
        todo.save()

        try:
            profile = todo.user.profile
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



def write_goal(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    if request.method == 'POST':
        goal_text = request.POST.get('goal', '').strip()
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        if goal_text:
            user = get_object_or_404(User, pk=user_id)
            goal_obj, created = DailyGoal.objects.get_or_create(user=user, date=date_obj)
            goal_obj.goal = goal_text
            goal_obj.save()
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)

def update_goal(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    if request.method == 'POST':
        new_goal_text = request.POST.get('goal', '').strip()
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        if new_goal_text:
            goal_obj = DailyGoal.objects.get(user_id=user_id, date=date_obj)
            goal_obj.goal = new_goal_text
            goal_obj.save()
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)

def delete_goal(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    goal_obj = DailyGoal.objects.get(user_id=user_id, date=date_obj)
    goal_obj.delete()
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)



def view_comment(request, selected_date):
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()


    if request.method == 'POST':
        target_user_id = request.POST.get('user_id')  # ✅ 폼에서 숨겨서 전달받기
        target_user = get_object_or_404(User, id=target_user_id)

        Comment.objects.create(
            writer=request.user,
            user=target_user,  # ⭐ target_user 기준으로 저장
            content=request.POST['content'],
            date=date_obj,
            created_at=timezone.now()
        )
        return redirect('planner:subpage', user_id=target_user.id, selected_date=selected_date)
    
    elif request.method == 'GET':
        comments = Comment.objects.filter(date=date_obj).order_by('-created_at')
        return render(request, 'planner/subpage.html', {'comments': comments,
            'selected_date': selected_date})

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.writer:
        selected_date = comment.date.strftime('%Y-%m-%d')
        comment.delete()
        return redirect('planner:subpage', user_id=request.user.id, selected_date=selected_date)
    
    return redirect('planner:subpage',user_id=request.user.id, selected_date=timezone.now().strftime('%Y-%m-%d'))


