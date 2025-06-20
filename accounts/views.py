from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage')
        else:
            return render(request, 'accounts/login.html', {
                'error': '아이디 또는 비밀번호가 틀렸습니다.'
            })

    return render(request, 'accounts/login.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


# 회원가입
def signup(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        univ = request.POST['univ']
        password = request.POST['password']
        confirm = request.POST['confirm']
        image = request.FILES.get('profile_image')

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
            username=nickname,
            password=password
        )

        # 시그널로 생성된 Profile 수정
        profile = user.profile
        profile.univ = univ
        if image:
            profile.profile_image = image
        profile.save()


        auth.login(request, user)
        return redirect('main:mainpage')

    return render(request, 'accounts/signup.html')


# 닉네임 중복 확인
def check_nickname(request):
    nickname = request.GET.get('nickname', '')
    exists = User.objects.filter(username=nickname).exists()
    return JsonResponse({'exists': exists})


# 버디페이지
@login_required
def buddypage(request):
    query = request.GET.get('q', '')
    following_ids = request.user.profile.followings.values_list('id', flat=True)

    if query:
        users = User.objects.filter(profile__isnull=False, username__icontains=query).exclude(id=request.user.id)
    else:
        users = [request.user]

    return render(request, 'accounts/buddypage.html', {
        'users': users,
        'following_ids': following_ids
    })


# 팔로우/언팔로우 기능
@login_required
def follow(request, id):
    user = request.user
    followed_user = get_object_or_404(User, pk=id)
    is_following = followed_user.profile in user.profile.followings.all()

    if is_following:
        user.profile.followings.remove(followed_user.profile)
    else:
        user.profile.followings.add(followed_user.profile)

    return redirect(request.META.get('HTTP_REFERER', 'accounts:buddypage'))


