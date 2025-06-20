from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from django.http import JsonResponse

# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else: 
            return render(request, 'accounts/login.html', {
                'error': '아이디 또는 비밀번호가 틀렸습니다.'
            })

    return render(request, 'accounts/login.html')

# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('/')

# 회원가입
def signup(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        univ = request.POST['univ']
        password = request.POST['password']
        confirm = request.POST['confirm']

        # 닉네임 공백 검사
        if not nickname.strip():
            return render(request, 'accounts/signup.html', {
                'error': '닉네임을 입력해주세요.'
            })

        # 중복 닉네임 검사
        if User.objects.filter(username=nickname).exists():
            return render(request, 'accounts/signup.html', {
                'error': '이미 존재하는 닉네임입니다.'
            })

        # 비밀번호 일치 검사
        if password != confirm:
            return render(request, 'accounts/signup.html', {
                'error': '비밀번호가 일치하지 않습니다.'
            })

        # 유저 생성
        user = User.objects.create_user(
            username=nickname,
            password=password
        )

        # ✅ Profile도 반드시 생성!
        Profile.objects.create(user=user, univ=univ)

        # 로그인 처리 후 메인으로 리다이렉트
        auth.login(request, user)
        return redirect('/')

    return render(request, 'accounts/signup.html')

# 닉네임 중복 확인
def check_nickname(request):
    nickname = request.GET.get('nickname', '')
    exists = User.objects.filter(username=nickname).exists()
    return JsonResponse({'exists': exists})
        


def buddypage(request):
    return render(request, 'accounts/buddypage.html')


