from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from calendar import month

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    birth_day = models.PositiveIntegerField(null=True, blank=True)
    birth_month = models.PositiveIntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.ImageField(default="profile_img.jpg", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
    
    class Meta:
        db_table = 'User Profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=100)
    content = HTMLField()
    blog_image = models.ImageField(upload_to="blog_image/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Blog Post'
        managed = True
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=1)
    comments = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    block_comment = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Blog Comment'
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        