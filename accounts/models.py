from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    univ = models.CharField(max_length=10)
    followings = models.ManyToManyField("self", related_name="followers", symmetrical=False)

    profile_image = models.ImageField(upload_to='profile_images/',blank=True,null=True,default='default_images/default.png')

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    honey_count=models.IntegerField(default=0)

    completed_todo_count=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

=======
>>>>>>> 60b1e50 (feat: #24-팔로우구현)
=======
>>>>>>> 60b1e50 (feat: #24-팔로우구현)
=======
>>>>>>> 60b1e50 (feat: #24-팔로우구현)
=======
>>>>>>> 60b1e50 (feat: #24-팔로우구현)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

