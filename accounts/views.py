from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        
        else: 
            return render(request, 'accounts/login.html')

    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':

        nickname = request.POST['nickname']
        univ = request.POST['univ']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if not nickname.strip():
            return render(request, 'accounts/signup.html', {
                'error': '닉네임을 입력해주세요.'
        })


        if User.objects.filter(username=nickname).exists():
            return render(request, 'accounts/signup.html', {
                'error': '이미 존재하는 닉네임입니다.'
            })

        if password != confirm:
            return render(request, 'accounts/signup.html', {
                'error': '비밀번호가 일치하지 않습니다.'
            })


        user = User.objects.create_user(
            username = nickname,
            password = password
        )

        profile = Profile(user=user, univ=univ)
        profile.save()

        auth.login(request, user)
        return redirect('/')
        
    return render(request, 'accounts/signup.html')