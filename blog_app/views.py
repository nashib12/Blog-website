from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from .models import Blog, UserMessage, Profile
from .forms import UserLoginForm, ProfileCreationForm

# Create your views here.
def home(request):
    user = User.objects.all()
    blog = Blog.objects.all()
    profile = Profile.objects.all()
    message = UserMessage.objects.all()
    
    cont_dict = {
        "user" : user,
        "blog" : blog,
        "profile" : profile,
        "message" : message,
    }
    return render(request, "blog_app/index.html", cont_dict)

#------------------- Authentication ----------------------
def registration(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.get(username=username)
        Profile.objects.create(id_id=user.id)
        auth = authenticate(request, username=username, password=password)
        if auth is not None:
            login(request, user)
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
            return redirect("home")
    return render(request, "authenticate/log_in.html", {"form":form})

def log_out(request):
    logout(request)
    return redirect("home")

def create_profile(request):
    user = Profile.objects.get(id_id=request.user.id)
    form = ProfileCreationForm(instance=user)
    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "authenticate/create_profile.html", {"form":form})
        
        
        