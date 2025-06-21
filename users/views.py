from django.shortcuts import render

# Create your views here.

# Create your views here.
def mypage(request):
    return render(request, 'users/mypage.html')