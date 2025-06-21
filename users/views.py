from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from planner.models import Todo
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.

# Create your views here.
def mypage(request,id,selected_date):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    user=get_object_or_404(User,pk=id)
    profile=user.profile

    date_obj=datetime.strptime(selected_date,'%Y-%m-%d').date()

    todos=Todo.objects.filter(user=user,date=date_obj)
    completed_todos=todos.filter(status='completed').count()
    total_todos=todos.count()
    success_rate=round((completed_todos / total_todos) * 100, 1) if total_todos else 0
    
    context = {
        'user': user,
        'profile': profile,
        'selected_date': selected_date,
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'success_rate': success_rate,
        'honey_count': profile.honey_count,
    }

    return render(request, 'users/mypage.html', context)