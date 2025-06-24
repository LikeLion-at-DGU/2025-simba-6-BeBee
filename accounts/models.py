from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta
from planner.models import Todo
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    univ = models.CharField(max_length=10)
    followings = models.ManyToManyField("self", related_name="followers", symmetrical=False)

    profile_image = models.ImageField(upload_to='profile_images/',blank=True,null=True,default='default_images/default.png')


    honey_count=models.IntegerField(default=0)
    completed_todo_count=models.IntegerField(default=0)
    daily_honey_earned = models.IntegerField(default=0)
    last_honey_earned_date = models.DateField(null=True, blank=True)

    total_study_time = models.DurationField(default=timedelta()) #총 공부 시간 필드
    last_reset_date = models.DateField(null=True, blank=True) #한 달마다 공부시간 갱신하기 위한 필드


    def __str__(self):
        return f'{self.user.username} Profile'



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # 프로필 생성
        Profile.objects.create(user=instance)

        # 오늘 날짜 기준으로 기본 할일 생성
        today = timezone.now().date()
        Todo.objects.create(
            user=instance,
            content="첫 번째 미션: 오늘의 할 일 입력하기!",
            status="not_completed",
            category="기타",  # 카테고리 중에 "기타" 있지?
            date=today
        )


class GiftExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange_time = models.DateTimeField(auto_now_add=True)
    honey_used = models.PositiveIntegerField(default=2700)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.honey_used}g at {self.exchanged_at.strftime('%Y-%m-%d %H:%M')}"
