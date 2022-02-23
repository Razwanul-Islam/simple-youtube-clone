from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.conf import settings
from django.utils import timezone
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    channel_name = models.CharField(max_length=150,null=True)
    profile_pic = models.ImageField(upload_to='channel/profile/',null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        unique_together = ['email', "username"]
    objects = UserManager()

class PlayList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    
class Video(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    thumbnail = models.ImageField(upload_to = 'images/thumbnail/', null=True)
    description = models.TextField()
    play_list = models.ForeignKey(PlayList,null=True, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/')
    tags = models.CharField(max_length = 250)
    uploaded_at = models.DateTimeField(auto_now=True)

class LikeDislike(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class Subscription(models.Model):
    channel = models.IntegerField()
    subscriber = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    
    
    
    
    
    
    
    
    