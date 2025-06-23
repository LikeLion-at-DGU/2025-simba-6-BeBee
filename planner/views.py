from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime, timedelta
from accounts.models import Profile
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Case, When, Value, IntegerField

# ⭐ user_id 변경: 전체 뷰에게 적용


def subpage(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    target_user = get_object_or_404(User, pk=user_id)
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('planner:subpage', user_id=user_id, selected_date=timezone.now().strftime('%Y-%m-%d'))

    # ✅ 여기에 status 정렬 우선순위 지정
    todos = Todo.objects.filter(user=target_user, date=date_obj).annotate(
        status_order=Case(
            When(status='completed', then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by('status_order', 'id')

    comments = Comment.objects.filter(user_id=target_user.id, date=date_obj).order_by('created_at')
    daily_goal = DailyGoal.objects.filter(user=target_user, date=date_obj).first()
    like_obj = Like.objects.filter(target_user=target_user, date=date_obj).first()
    return render(request, 'planner/subpage.html', {
        'todos': todos,
        'selected_date': selected_date,
        'daily_goal': daily_goal,
        'comments': comments,
        'target_user': target_user,
        'login_user': request.user,
        like_obj: like_obj
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

        # ✅ datetime 필드이므로 바로 사용
        start_dt = todo.started_at

        elapsed_time = now - start_dt
        todo.ended_at = now
        todo.total_elapsed_time = (todo.total_elapsed_time or timedelta()) + elapsed_time
        todo.started_at = None
        todo.save()

        return JsonResponse({
            "message": "타이머 종료됨",
            "ended_at": todo.ended_at,
            "elapsed": str(elapsed_time),
            "total_elapsed": str(todo.total_elapsed_time),
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

@require_POST
def todo_complete(request, user_id, todo_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("로그인이 필요합니다.")

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    todo = get_object_or_404(Todo, id=todo_id, user_id=user_id)
    profile = todo.user.profile
    today = timezone.now().date()
    HONEY_PER_TODO = 10

    # ✅ 날짜가 바뀌면 일일 꿀 초기화
    if profile.last_honey_earned_date != today:
        profile.daily_honey_earned = 0
        profile.last_honey_earned_date = today

    if todo.status == 'completed':
        # ✅ 체크 해제 → 꿀 차감
        todo.status = 'not_completed'
        profile.completed_todo_count = max(0, profile.completed_todo_count - 1)
        profile.honey_count = max(0, profile.honey_count - HONEY_PER_TODO)
        profile.daily_honey_earned = max(0, profile.daily_honey_earned - HONEY_PER_TODO)
    else:
        # ✅ 체크 → 꿀 지급
        todo.status = 'completed'
        profile.completed_todo_count += 1

        if profile.daily_honey_earned < 50:
            give = min(HONEY_PER_TODO, 50 - profile.daily_honey_earned)
            profile.honey_count += give
            profile.daily_honey_earned += give

    todo.save()
    profile.save()
    print("🔁 상태 저장됨:", todo.id, todo.status)

    return JsonResponse({
    'status': todo.status,
    'honey_count': profile.honey_count,  # ✅ 꿀 정보 추가
    
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

# def delete_goal(request, user_id, selected_date):
#     if not request.user.is_authenticated:
#         return redirect('accounts:login')

#     if request.user.id != user_id:
#         return HttpResponseForbidden("권한이 없습니다.")

#     date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
#     goal_obj = DailyGoal.objects.get(user_id=user_id, date=date_obj)
#     goal_obj.delete()
#     return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)


def delete_goal(request, user_id, selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.id != user_id:
        return HttpResponseForbidden("권한이 없습니다.")

    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # 안전하게 goal 객체 조회
    goal_obj = DailyGoal.objects.filter(user_id=user_id, date=date_obj).first()
    if goal_obj:
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

def like_subpage(request, user_id, selected_date):
    target_user = get_object_or_404(User, id=user_id)
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    like_obj, created = Like.objects.get_or_create(target_user=target_user, date=date_obj)

    if request.user in like_obj.like.all():
        like_obj.like.remove(request.user)
        like_obj.like_count -= 1
    else:
        like_obj.like.add(request.user)
        like_obj.like_count += 1

    like_obj.save()
    return redirect('planner:subpage', user_id=user_id, selected_date=selected_date)

