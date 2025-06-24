from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from planner.models import Todo
from django.contrib.auth.models import User
from datetime import date,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import GiftExchange


def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}시간 {minutes}분"

def mypage(request, user_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    user = get_object_or_404(User, pk=user_id)
    profile = user.profile

    today = date.today()
    start_of_month = today.replace(day=1)  
    end_of_range = today  # 오늘까지
    current_month = today.month
    
    #한 달이 지나면 총 공부시간 초기화 
    if profile.last_reset_date != start_of_month:
        profile.total_study_time = timedelta()  # 시간 초기화
        profile.last_reset_date = start_of_month  


    # 이번 달 1일부터 오늘까지의 투두 필터링
    todos = Todo.objects.filter(user=user, date__range=[start_of_month, end_of_range])
    completed_todos = todos.filter(status='completed').count()
    total_todos = todos.count()
    success_rate = round((completed_todos / total_todos) * 100, 1) if total_todos else 0
    formatted_time = format_timedelta(profile.total_study_time)

    context = {
        'user': user,
        'profile': profile,
        
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'success_rate': success_rate,
        'honey_count': profile.honey_count,
        'formatted_time': formatted_time,
        'current_month': current_month,
        'univ': profile.univ,
    }

    return render(request, 'users/mypage.html', context)

def update_profile(request,user_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.method=='POST':
        user=get_object_or_404(User,pk=user_id)
        profile=user.profile

        
        new_profile_image=request.FILES.get('profile_image')
        if new_profile_image:
            profile.profile_image=new_profile_image
            profile.save()
        
        new_username=request.POST.get('username')
        if new_username:
            if User.objects.filter(username=new_username).exclude(pk=user.id).exists():
                return render(request, 'users/mypage.html', {
            'user': user,
            'profile': profile,
            'error': '이미 존재하는 닉네임입니다.'
        })
        user.username=new_username
        user.save()

        return redirect('users:mypage',user_id=user.id)


    return redirect('users:mypage',user_id=user_id)

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




