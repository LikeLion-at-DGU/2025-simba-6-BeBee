from django.shortcuts import render

# Create your views here.
def subpage(request):
    return render(request, 'planner/subpage.html')