from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from datetime import date, timedelta
from planner.models import Todo

# Create your views here.

def login_redirect(request):
    return redirect('accounts:login')

def mainpage(request, user_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if not (user_id == request.user.id or request.user.profile.followings.filter(user__id=user_id).exists()):
        return redirect('main:mainpage', user_id=request.user.id)
    
    target_user = get_object_or_404(User, pk=user_id)

    today = date.today() #오늘 날짜
    start_of_month = today.replace(day=1) #매월 1일로 바꿈
    num_days = (today - start_of_month).days + 1 #오늘 날짜가 22일이라면 22번 반복
    profile = target_user.profile 

    daily_success_list = []
    for i in range(num_days):
        target_date = start_of_month + timedelta(days=i)
        rate = get_daily_success_rate(target_user, target_date)
        daily_success_list.append({
            'date': target_date,
            'success_rate': rate, #딕셔너리 형태로 그 날짜와 성공률을 리스트에 저장
        })

    return render(request, 'main/mainpage.html',{
        'user_id': user_id,
        'target_user': target_user,
        'daily_success_list':daily_success_list,
        'honey_count': profile.honey_count,
        })

#매일 수행률을 계산하는 함수
def get_daily_success_rate(user, target_date):
    todos = Todo.objects.filter(user=user, date=target_date)
    total = todos.count()
    completed = todos.filter(status='completed').count()
    return round((completed / total) * 100, 1) if total else 0

def firstpage(request):
    return render(request, 'main/firstpage.html')

