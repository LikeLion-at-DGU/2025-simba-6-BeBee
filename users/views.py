from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from planner.models import Todo
from django.contrib.auth.models import User
from datetime import date

def mypage(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    user = get_object_or_404(User, pk=id)
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
