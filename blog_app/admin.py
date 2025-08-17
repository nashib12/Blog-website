from django.contrib import admin

from .models import Blog, UserMessage, Profile
# Register your models here.
admin.site.register([Blog, UserMessage, Profile])