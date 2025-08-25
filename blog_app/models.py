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
        
class Tag(models.Model):
    tag = models.CharField(max_length=100)
    
    def __str__(self):
        return self.tag
    
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=100)
    content = HTMLField()
    blog_image = models.ImageField(upload_to="blog_image/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, default=None, blank=True)
    likes = models.PositiveIntegerField(default=0, blank=True)
    
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

class Album(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=200)
    descriprion = models.CharField(max_length=255, default="No Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'album'
        managed = True
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'
        ordering = ["-created_at"]

class Gallery(models.Model):
    album = models.ForeignKey(Album, related_name="images", on_delete=models.CASCADE, default=None)
    images = models.ImageField(upload_to="gallery_image/")
    captions = models.CharField(max_length=50,default="", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'gallery'
        managed = True
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ["-uploaded_at"]
        
# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
#     post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
#     count = models.IntegerField(default=0)
    
#     class Meta:
#         db_table = 'like'
#         managed = True
#         verbose_name = 'Like'
#         verbose_name_plural = 'Likes'

class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="total_like")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'liked'
        managed = True
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ['user', 'post']
        
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers", blank=True, null=True)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", blank=True, null=True)
    
    class Meta:
        db_table = 'follower'
        managed = True 
        
class BlockUser(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blockusers")
    block_status = models.BooleanField(default=False)
    blocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'blockuser'
        managed = True
        ordering = ['-blocked_at']