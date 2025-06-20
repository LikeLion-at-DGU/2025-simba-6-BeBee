from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    univ = models.CharField(max_length=10)

    profile_image = models.ImageField(upload_to='profile_images/',blank=True,null=True,default='default_images/default.png')

    honey_count=models.IntegerField(default=0)

    completed_todo_count=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'


