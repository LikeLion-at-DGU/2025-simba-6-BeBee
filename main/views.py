from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.

from django.shortcuts import redirect

def login_redirect(request):
    return redirect('accounts:login')

def mainpage(request, user_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if not (user_id == request.user.id or request.user.profile.followings.filter(user__id=user_id).exists()):
        return redirect('main:mainpage', user_id=request.user.id)
    
    target_user = get_object_or_404(User, pk=user_id)

    return render(request, 'main/mainpage.html',{'user_id': user_id,'target_user': target_user,})