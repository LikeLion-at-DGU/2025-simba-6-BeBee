from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from planner.models import Todo
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import GiftExchange


def mypage(request, user_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    user = get_object_or_404(User, pk=user_id)
    profile = user.profile

    today = date.today()
    start_of_month = today.replace(day=1)  # 이번 달 1일
    end_of_range = today  # 오늘까지

    # 이번 달 1일부터 오늘까지의 투두 필터링
    todos = Todo.objects.filter(user=user, date__range=[start_of_month, end_of_range])
    completed_todos = todos.filter(status='completed').count()
    total_todos = todos.count()
    success_rate = round((completed_todos / total_todos) * 100, 1) if total_todos else 0

    context = {
        'user': user,
        'profile': profile,
        
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'success_rate': success_rate,
        'honey_count': profile.honey_count,
    }

    return render(request, 'users/mypage.html', context)

@login_required
def exchange_honey(request):
    profile = request.user.profile

    if profile.honey_count >= 2700:
        profile.honey_count -= 2700
        profile.save()

        GiftExchange.objects.create(
            user=request.user,
            honey_used=2700,
            is_successful=True
        )

        messages.success(request, "기프티콘으로 교환되었습니다! 🎁")
    else:
        messages.error(request, "꿀이 부족해요! 최소 2700g이 필요합니다.")

    return redirect('users:mypage', user_id=request.user.id)

