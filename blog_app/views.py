from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse

from .models import Blog, Profile, Comment, Gallery, Album
from .forms import *
from .validators import *
from .decorators import unautorized_access, admin_only

# Create your views here.
@login_required(login_url="log-in")
def home(request):
    blogs = (Blog.objects
             .select_related('author', 'author__profile')
             .prefetch_related('comments__author__profile')
             .order_by('-created_at')
             .filter(approved=True))
    return render(request, "blog_app/index.html", {"blog" : blogs})

@login_required(login_url="log-in")
def gallery(request):
    author = Profile.objects.get(user_id=request.user.id)
    album = Album.objects.get(author=author.user_id)
    gallery = Gallery.objects.filter(album=album)
    # return HttpResponse(images)
    return render(request, "blog_app/gallery.html",{"gallery" : gallery})
  
#------------------- Authentication ----------------------
@unautorized_access
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
                validate_password(password)
                password_validate(password)
                
                User = get_user_model()
                with transaction.atomic():
                    user = User.objects.create_user(username=username,email=email,password=password)
                    Profile.objects.create(user=user, email=user.email)
                    
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

@unautorized_access
def log_in(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_superuser:
                profile = Profile.objects.get(user_id=user.id)
                if profile.is_active:
                    login(request, user)
                    messages.success(request, "Login Successfull!")
                    return redirect("home")
                else:
                    messages.error(request, "Your account has been blocked")
                    return redirect("log-in")
            else:
                login(request, user)
                messages.success(request, "Login Successfull!")
                return redirect("home")
        else:
            messages.error(request, "Username or Password doesn't match")
            return redirect("log-in")
    return render(request, "authenticate/log_in.html", {"form":form})

@login_required(login_url="log-in")
def log_out(request):
    logout(request)
    return redirect("log-in")

@login_required(login_url="log-in")
def create_profile(request):
    user = Profile.objects.get(user_id=request.user.id)
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
    form = BlogCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Blog Successfully created!")
        return redirect("view-profile")
    return render(request, "blog_app/create_blog.html", {"form" : form})

@login_required(login_url="log-in")
def update_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)
    if blog.author != request.user and not request.user.is_staff:
        raise PermissionDenied("Not allowed to edit")
    form = BlogCreationForm(request.POST or None, request.FILES or None, instance=blog)
    if form.is_valid():
        form.save()
        messages.success(request, "Blog updated")
        return redirect("view-profile")
    return  render(request, "blog_app/update_blog.html", {"form" : form})

@login_required(login_url="log-in")
def delete_blog(request, id):
    # blog = Blog.objects.get(id=id)
    blog = get_object_or_404(Blog, pk=id)
    if blog.author != request.user and not request.user.is_staff:
        raise PermissionDenied("Not allowed to delete this blog")
    blog.delete()
    messages.success(request, "Blog successfully deleted!")
    return redirect("view-profile")

@login_required(login_url="log-in")
def view_profile(request):
    try:
        blog = Blog.objects.filter(author_id=request.user.id).select_related('author', 'author__profile').prefetch_related('comments__author__profile').order_by('-created_at')
        cont_dict = {
            "blog" : blog
        }
        return render(request, "blog_app/view_profile.html", cont_dict)
    except Blog.DoesNotExist:
        messages.error(request, "Create your profile first")
        return redirect("home")
    
@login_required(login_url="log-in")
def blog_comment(request, id):
    blog = get_object_or_404(Blog.objects.select_related('author'), pk=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        with transaction.atomic():
            Comment.objects.create(blog=blog, author=request.user, comments=form.cleaned_data["comments"])
        messages.success(request, "Comment added")
        return redirect("home")
    return render(request, "blog_app/comments.html", {"form" : form})

@login_required(login_url='log-in')
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    blog = Blog.objects.get(id=comment.blog_id)
    if blog.author == request.user:
        comment.delete()
        messages.success(request, "Comment Successfully deleted by author")
        return redirect("home") 
    if comment.author != request.user and not request.user.is_staff:
        messages.error(request, "Not allowed")
        return redirect("home")
    comment.delete()
    messages.success(request, "Comment Successfully deleted")
    return redirect("home") 

#----------------- Admin section --------------------------
@login_required(login_url="log-in")
@admin_only
def view_dashboard(request):
    user = Profile.objects.all().order_by('-created_at')
    blog = Blog.objects.all().select_related('author', 'author__profile').order_by('-created_at')
    comment = Comment.objects.all()
    cont_dict = {
        "users" : user,
        "blogs" : blog,
        "comment" : len(comment),
        "total_user" : len(user),
        "total_blog" : len(blog),
    }
    return render(request, "admin/dashboard.html", cont_dict)

@login_required(login_url="log-in")
@admin_only
def change_status(request, id):
    user = get_object_or_404(Profile, pk=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, "Account blocked")
    else:
        user.is_active = True
        user.save()
        messages.success(request, "Account active")
    return redirect("dashboard")

@login_required(login_url="log-in")
@admin_only
def approve_post(request, id):
    blog = get_object_or_404(Blog, pk=id)
    if blog.approved:
        blog.approved = False
        blog.save()
        messages.success(request, "Blog not approved")
    else:
        blog.approved = True
        blog.save()
        messages.success(request, "Blog approved")
    return redirect("dashboard")

# -------------------- Gallery section ----------------------------
@login_required(login_url="log-in")
def add_gallery_img(request):
    form = GalleryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Image successfully uploaded")
        return redirect("gallery")
    return render(request, "gallery/add_image.html", {"form" : form})

@login_required(login_url="log-in")
def create_album(request):
    form = AlbumForm(request.POST or None)
    if form.is_valid():
        author = Profile.objects.get(user=request.user)
        instance = form.save(commit=False)
        instance.author = author
        instance.save()
        messages.success(request, "Album successfully added")
        return redirect("view-profile")
    return render(request, "gallery/add_album.html", {"form" : form})