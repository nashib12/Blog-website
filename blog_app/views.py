from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Blog, UserProfileList
from .forms import UserLoginForm, CustomUserCreationForm, ProfileCreationForm, BlogCreationForm

# Create your views here.
def home(request):
    try:
        blog = Blog.objects.filter(name_id=request.user.id)
        cont_dict = {
            "blog" : blog,
        }
        return render(request, "blog_app/index.html", cont_dict)
    except Blog.DoesNotExist:
        messages.error(request, "Create a blog first!")
        return render(request, "blog_app/index.html")

#------------------- Authentication ----------------------
def registration(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Account successfully created")
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.get(username=username)
        UserProfileList.objects.create(profile_id=user.id, email=user.email)
        auth = authenticate(request, username=username, password=password)
        if auth is not None:
            login(request, user)
            messages.success(request, "Login successfull")
            return redirect("create-profile")
    return render(request, "authenticate/registration.html", {"form":form})

def log_in(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfull!")
            return redirect("home")
    return render(request, "authenticate/log_in.html", {"form":form})

def log_out(request):
    logout(request)
    return redirect("log-in")

def create_profile(request):
    user = UserProfileList.objects.get(profile_id=request.user.id)
    form = ProfileCreationForm(instance=user)
    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfullyc updated")
            return redirect("home")
    return render(request, "authenticate/create_profile.html", {"form":form})
        
#---------------- Blog Section ----------------------
def create_blog(request):
    form = BlogCreationForm()
    if request.method == "POST":
        form = BlogCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['blog_image']
            
            Blog.objects.create(name_id=request.user.id, title=title, content=content, blog_image=image)
            messages.success(request, "Blog Successfully created!")
            return redirect("home")
    return render(request, "blog_app/create_blog.html", {"form" : form})

def update_blog(request, id):
    blog = Blog.objects.get(id=id)
    form = BlogCreationForm(instance=blog)
    if request.method == "POST":
        form = BlogCreationForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog Successfully Updated!")
            return redirect("home")
    return render(request, "blog_app/update_blog.html", {"form" : form})

def delete_blog(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request, "Blog successfully deleted!")
    return redirect("home")
    