from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Case, When, Value, IntegerField
from .models import DailyHoney

# 시간+분 으로 바꿔주는 함수
def format_timedelta(td):   
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}시간 {minutes}분 {seconds}초"# 시간+분 



def subpage(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    target_user = get_object_or_404(User, pk=user_id)
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('planner:subpage', user_id=user_id, selected_date=timezone.now().strftime('%Y-%m-%d'))

    # default 할 일 
    if not Todo.objects.filter(user=target_user, date=date_obj).exists():
        Todo.objects.create(
            user=target_user,
            content="첫 번째 미션: 오늘의 할 일 입력하기!",
            status="not_completed",
            category="기타",
            date=date_obj
        )

    # 정렬 우선순위
    todos = Todo.objects.filter(user=target_user, date=date_obj).annotate(
        status_order=Case(
            When(status='completed', then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by('status_order', 'id')

    for todo in todos:
        if todo.total_elapsed_time:
            seconds = int(todo.total_elapsed_time.total_seconds())
            h, r = divmod(seconds, 3600)
            m, s = divmod(r, 60)
            todo.formatted_time = f"{h:02}:{m:02}:{s:02}"  # 타이머용
            todo.formatted_time_hms = f"{h}시간 {m}분 {s}초"  # 서브페이지 리스트용
            todo.formatted_time_hm = f"{h}시간 {m}분"         # 마이페이지용
        else:
            todo.formatted_time = "00:00:00"
            todo.formatted_time_hms = "0시간 0분 0초"
            todo.formatted_time_hm = "0시간 0분"

    comments = Comment.objects.filter(user_id=target_user.id, date=date_obj).order_by('created_at')
    daily_goal = DailyGoal.objects.filter(user=target_user, date=date_obj).first()
    like_obj = Like.objects.filter(target_user=target_user, date=date_obj).first()

    profile = target_user.profile
    formatted_time_hm = format_timedelta(profile.total_study_time or timedelta())

    is_liked = False
    if like_obj and request.user in like_obj.like.all():
        is_liked = True

    daily_honey = DailyHoney.objects.filter(user=target_user, date=date_obj).first()
    earned = daily_honey.honey_earned if daily_honey else 0

    return render(request, 'planner/subpage.html', {
        'todos': todos,
        'selected_date': selected_date,
        'daily_goal': daily_goal,
        'comments': comments,
        'target_user': target_user,
        'login_user': request.user,
        'like_obj': like_obj,
        'formatted_time_hm': formatted_time_hm,
        'is_liked': is_liked,
        'earned': earned,
    })





def start_timer(request, user_id, todo_id, selected_date):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("로그인이 필요합니다.")
    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    if not todo.started_at:
        todo.started_at = timezone.now()
        todo.save()
    return JsonResponse({"message": "타이머 시작됨", "started_at": todo.started_at})



def stop_timer(request, user_id, todo_id, selected_date):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("로그인이 필요합니다.")
    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    if todo.started_at:
        now = timezone.now()

    
        start_dt = todo.started_at
        
        
        elapsed_time = now - start_dt
        todo.ended_at = now
        todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed_time
        todo.started_at = None
        todo.save()

        # 프로필 총 공부시간 
        profile = request.user.profile
        profile.total_study_time = (profile.total_study_time or timedelta()) + elapsed_time
        profile.save()

        return JsonResponse({
            "message": "타이머 종료됨",
            "ended_at": todo.ended_at,
            "elapsed": str(elapsed_time),
            "total_elapsed": format_timedelta(todo.total_elapsed_time),
            "total_seconds": int(todo.total_elapsed_time.total_seconds()), 
        })

    return JsonResponse({"error": "타이머가 시작되지 않았습니다."}, status=400)

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

def todo_delete(request, user_id, todo_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    selected_date = todo.date.strftime('%Y-%m-%d')
    todo.delete()
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)


@require_POST
def todo_complete(request, user_id, todo_id):
    if not request.user.is_authenticated or request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    today = todo.date or timezone.now().date()

    daily_honey, _ = DailyHoney.objects.get_or_create(user=request.user, date=today)
    profile = request.user.profile
    HONEY_PER_TODO = 10

    if todo.status == 'completed':
    # 체크 해제
        todo.status = 'not_completed'
        profile.completed_todo_count = max(0, profile.completed_todo_count - 1)
        todo.save()

        
        remaining_completed = Todo.objects.filter(user=request.user, date=today, status='completed').count()

        # 5개 이하일 때는 계속 깎이게 하되, 0 이하로는 안 내려가게
        if remaining_completed < 5 and daily_honey.honey_earned > 0:
            profile.honey_count = max(0, profile.honey_count - HONEY_PER_TODO)
            daily_honey.honey_earned = max(0, daily_honey.honey_earned - HONEY_PER_TODO)


    else:
        
        todo.status = 'completed'
        profile.completed_todo_count += 1

        if daily_honey.honey_earned < 50:
            give = min(HONEY_PER_TODO, 50 - daily_honey.honey_earned)
            profile.honey_count += give
            daily_honey.honey_earned += give

        todo.save()

    profile.save()
    daily_honey.save()

    return JsonResponse({
        'status': todo.status,
        'honey_count': profile.honey_count,
        'daily_earned': daily_honey.honey_earned,
    })



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

    
    goal_obj = DailyGoal.objects.filter(user_id=user_id, date=date_obj).first()
    if goal_obj:
        goal_obj.delete()

    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)


def view_comment(request, selected_date):
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    if request.method == 'POST':
        target_user_id = request.POST.get('user_id')  
        target_user = get_object_or_404(User, id=target_user_id)

        Comment.objects.create(
            writer=request.user,
            user=target_user,  
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
        target_user_id = comment.user.id
        comment.delete()
        return redirect('planner:subpage', user_id=target_user_id, selected_date=selected_date)
    
    return redirect('planner:subpage',user_id=comment.user.id, selected_date=timezone.now().strftime('%Y-%m-%d'))

@require_POST
def like_subpage(request, user_id, selected_date):
    target_user = get_object_or_404(User, id=user_id)
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    like_obj, created = Like.objects.get_or_create(target_user=target_user, date=date_obj)

    liked = False
    if request.user in like_obj.like.all():
        like_obj.like.remove(request.user)
        like_obj.like_count -= 1
    else:
        like_obj.like.add(request.user)
        like_obj.like_count += 1
        liked = True

    like_obj.save()

    return JsonResponse({
        "liked": liked,
        "like_count": like_obj.like_count
    })
