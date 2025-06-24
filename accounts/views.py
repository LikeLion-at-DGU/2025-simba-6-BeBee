from django.shortcuts import render, redirect, get_object_or_404
from .models import *
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

def buddypage(request, user_id):
    query = request.GET.get('q', '')
    following_ids = request.user.profile.followings.values_list('id', flat=True)

    follower_count = request.user.profile.followers.count()
    following_count = request.user.profile.followings.count()
    
    page_user = get_object_or_404(User, id=user_id)
    profile = page_user.profile  # ✅ 수정: 페이지 주인의 프로필 가져오기

    if query:
        users = User.objects.filter(
            profile__isnull=False,
            username__icontains=query
        ).exclude(id=request.user.id)
    else:
        users = [request.user]

    context = {
        'user': request.user,         # ✅ 현재 로그인한 사용자
        'users': users,               # ✅ 검색 또는 전체 유저 리스트
        'profile': profile,           # ✅ 현재 페이지 주인의 프로필
        'following_ids': following_ids,
        'follower_count': follower_count,
        'following_count': following_count,
        'page_user': page_user,
        'honey_count': profile.honey_count,
        'univ': profile.univ,
    }

    return render(request, 'accounts/buddypage.html', context)



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
        'honey_count': user.profile.honey_count,
        'univ' : user.profile.univ,
    })



@login_required
def friend_profile_api(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({'exists': False})
    
    # 자기 자신
    if query == 'me':
        user = request.user
    else:
        try:
            user = User.objects.get(username=query)
        except User.DoesNotExist:
            return JsonResponse({'exists': False})

    profile = user.profile
    is_following = profile in request.user.profile.followings.all()
    
    return JsonResponse({
        'exists': True,
        'id': user.id,
        'username': user.username,
        'honey_count': profile.honey_count,
        'is_following': is_following,
        'profile_image_url': profile.profile_image.url if profile.profile_image else '',
        'univ': profile.univ,  # ✅ 추가
    })

    

@login_required
def follow_lists_partial(request):
    return render(request, 'accounts/_follow_lists.html', {
        'user': request.user,
        'follower_count': request.user.profile.followers.count(),
        'following_count': request.user.profile.followings.count(),
    })
