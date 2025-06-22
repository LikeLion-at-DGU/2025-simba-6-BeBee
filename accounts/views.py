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
            return redirect('main:mainpage',user_id=user.id)
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
        return redirect('main:mainpage',user_id=user.id)

    return render(request, 'accounts/signup.html')


# 닉네임 중복 확인
def check_nickname(request):
    nickname = request.GET.get('nickname', '')
    exists = User.objects.filter(username=nickname).exists()
    return JsonResponse({'exists': exists})


# 버디페이지
@login_required
def buddypage(request, user_id):
    query = request.GET.get('q', '')
    following_ids = request.user.profile.followings.values_list('id', flat=True)

    follower_count = request.user.profile.followers.count()
    following_count = request.user.profile.followings.count()
    
    page_user = get_object_or_404(User, id=user_id)

    if query:
        users = User.objects.filter(profile__isnull=False, username__icontains=query).exclude(id=request.user.id)
    else:
        users = [request.user]

    return render(request, 'accounts/buddypage.html', {
        'users': users,
        'following_ids': following_ids,
        'followr_count': folower_count,
        'following_count': following_count,
        'page_user': page_user
    })


# 팔로우/언팔로우 기능
@login_required
def follow(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    user = request.user
    followed_user = get_object_or_404(User, pk=id)
    is_following = followed_user.profile in user.profile.followings.all()

    if is_following:
        user.profile.followings.remove(followed_user.profile)
    else:
        user.profile.followings.add(followed_user.profile)

    return JsonResponse({
        'success': True,
        'following': not is_following,
        'follower_count': followed_user.profile.followers.count(),
        'following_count': user.profile.followings.count(),
    })



@login_required
def friend_profile_api(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'exists': False})

    try:
        # 🔥 여기서 request.user가 아닌, 'username=query'로 친구 유저를 가져와야 함!
        user = User.objects.get(username=query)
        profile = user.profile
        is_following = profile in request.user.profile.followings.all()

        return JsonResponse({
            'exists': True,
            'id': user.id,  # ← 🔥 이게 친구 ID여야 함
            'username': user.username,
            'honey': getattr(profile, 'honey', 0),
            'is_following': is_following,
            'profile_image_url': profile.profile_image.url if profile.profile_image else '',
        })
    except User.DoesNotExist:
        return JsonResponse({'exists': False})
    

@login_required
def follow_lists_partial(request):
    return render(request, 'accounts/_follow_lists.html', {
        'user': request.user,
        'follower_count': request.user.profile.followers.count(),
        'following_count': request.user.profile.followings.count(),
    })
