from django.contrib import admin

from .models import Blog, Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active')
    ordering = ('created_at', )
    fields = ['is_active']
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')
    ordering = ('title',)
    list_filter = ('title', 'author')
    fields = ['name', 'title' , 'content', 'blog_image']