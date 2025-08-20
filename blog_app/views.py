from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required

from .models import Blog, UserProfileList, Comment
from .forms import *
from .validators import *
# Create your views here.
@login_required(login_url="log-in")
def home(request):
    try:
        profile = UserProfileList.objects.all()
        blog = Blog.objects.all().order_by('?')
        comment = Comment.objects.all()
        cont_dict = {
            "profile" : profile,
            "blog" : blog,
            "comment" : comment,
        }
        return render(request, "blog_app/index.html", cont_dict)
    except Blog.DoesNotExist:
        messages.error(request, "Create a blog first!")
        return render(request, "blog_app/index.html")

#------------------- Authentication ----------------------
def registration(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        cpassword = form.cleaned_data['cpassword']
        if password == cpassword:
            try:
                check_username(username)
                email_validate(email)
                password_validation(password)
                password_validate(password)
                
                User.objects.create_user(username=username,email=email,password=password)
                messages.success(request, "Account successfully created")
            
                user = User.objects.get(username=username)
                UserProfileList.objects.create(profile_id=user.id, email=user.email)
                auth = authenticate(request, username=username, password=password)
                if auth is not None:
                    login(request, user)
                    return redirect("create-profile")
            except Exception as e:
                messages.error(request, e)
                return redirect("registration")
        else:
            messages.error(request, "Both password must be same")
            return redirect("registration")
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

@login_required(login_url="log-in")
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

@login_required(login_url="log-in")
def change_password(request):
    form = CustomPasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            password_validate(form.cleaned_data['new_password1'])
            form.save()
            messages.success(request, "Password change successfully")
            return redirect("log-in")
    return render(request, "authenticate/change_password.html", {"form" : form})
        
        
#---------------- Blog Section ----------------------
@login_required(login_url="log-in")
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
            return redirect("view-profile")
    return render(request, "blog_app/create_blog.html", {"form" : form})

@login_required(login_url="log-in")
def update_blog(request, id):
    blog = Blog.objects.get(id=id)
    form = BlogCreationForm(instance=blog)
    if request.method == "POST":
        form = BlogCreationForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog Successfully Updated!")
            return redirect("view-profile")
    return render(request, "blog_app/update_blog.html", {"form" : form})

@login_required(login_url="log-in")
def delete_blog(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request, "Blog successfully deleted!")
    return redirect("view-profile")

@login_required(login_url="log-in")
def view_profile(request):
    try:
        prfoile = UserProfileList.objects.get(profile_id=request.user.id)
        blog = Blog.objects.filter(name_id=request.user.id)
        cont_dict = {
            "profile" : prfoile,
            "blog" : blog
        }
        return render(request, "blog_app/view_profile.html", cont_dict)
    except UserProfileList.DoesNotExist:
        messages.error(request, "Create your profile first")
        return redirect("home")
    
@login_required(login_url="log-in")
def blog_comment(request, id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.cleaned_data['comments']
        Comment.objects.create(blog_id=id, commenter_id = request.user.id, comments=comment)
        messages.success(request, "Success")
        return redirect("home")
    return render(request, "blog_app/comments.html", {"form" : form})