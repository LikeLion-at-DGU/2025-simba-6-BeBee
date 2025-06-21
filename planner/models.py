from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
# 카테고리 모델: 이름만 저장
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# 할 일 모델
class Todo(models.Model):
    CATEGORY_CHOICES = [
        ('대외활동', '대외활동'),
        ('과제', '과제'),
        ('시험공부', '시험공부'),
        ('자격증', '자격증'),
        ('알바', '알바'),
        ('동아리', '동아리'),
        ('취미활동', '취미활동'),
        ('기타', '기타'),
    ]
    STATUS_CHOICES = [
        ('not_completed', '미완료'),
        ('completed', '완료'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    content = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_completed')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    deadline = models.DateField(null=True, blank=True)
    started_at = models.TimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.DurationField(null=True, blank=True)
    total_elapsed_time = models.DurationField(default=timedelta())
    date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} ({self.category})"

class DailyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # 목표가 적용되는 날짜
    goal = models.CharField(max_length=200)  # 오늘의 목표 내용


class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, null=False, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.writer.username}: {self.content[:20]}"
