from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    univ = models.CharField(max_length=10)



=======

# Create your models here.
>>>>>>> 851ff7b (WIP: accounts 앱 초기 구조 및 로그인 페이지 구현(#2))
