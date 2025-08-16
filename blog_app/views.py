from django.shortcuts import render

from .models import Blog

# Create your views here.
def home(request):
    blog = Blog.objects.all()
    return render(request, "blog_websites/index.html" ,{"blog" : blog})