from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    content = HTMLField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Blog Post'
        managed = True
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
    
class Profile(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact = models.IntegerField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_img/", blank=True, null=True, default="imgg/profile_img.jpg")
    
    class Meta:
        db_table = 'user_profile_list'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class UserMessage(User):
    contact = models.IntegerField(blank=True, null=True)
    message = models.TextField()
    
    class Meta:
        db_table = 'user_message'
        managed = True
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'