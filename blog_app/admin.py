from django.contrib import admin

from .models import Blog, UserProfileList
# Register your models here.
@admin.register(UserProfileList)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active')
    ordering = ('first_name', )
    fields = ['is_active']
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    ordering = ('title',)
    list_filter = ('title', )
    fields = ['name', 'title' , 'content', 'blog_image']