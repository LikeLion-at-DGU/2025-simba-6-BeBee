from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.
def mainpage(request, user_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.user.id != user_id:
        return redirect('main:mainpage', user_id=request.user.id)

    return render(request, 'main/mainpage.html',{'user_id': user_id,})