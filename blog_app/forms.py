import calendar

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from tinymce.widgets import TinyMCE

from .models import UserProfileList, Blog, Comment

class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control fs-4', 'id' : 'username'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class' : 'form-control fs-4', 'id' : 'password'}))

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class' : 'form-control fs-4', 'id' : 'username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class' : 'form-control fs-4', 'id' : 'email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class' : 'form-control fs-4' , 'id' : 'password'}))
    cpassword = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class' : 'form-control fs-4' , 'id' : 'password1'}))

#  Create a user form with cutsom email filed using user creation CustomUserCreationForm
# from django.contrib.auth.forms import UserCreationForm  
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class' : 'form-control fs-4', 'id' : 'email'}))
    
#     class Meta:
#         model =  User
#         fields = ('username', 'email', 'password1', 'password2')
        
#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
#         self.fields['username'].widget.attrs['class'] = 'form-control fs-4'
#         self.fields['username'].widget.attrs['id'] = 'username'
#         self.fields['username'].label = ''
        
#         self.fields['password1'].widget.attrs['class'] = 'form-control fs-4'
#         self.fields['password1'].widget.attrs['id'] = 'password'
#         self.fields['password1'].label = ''
        
#         self.fields['password2'].widget.attrs['class'] = 'form-control fs-4'
#         self.fields['password2'].widget.attrs['id'] = 'password1'
#         self.fields['password2'].label = ''
    
class ProfileCreationForm(forms.ModelForm):
    class Meta:
        gender_choices = [
            ('' , 'Select a gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
            ('Prefer not to say', 'Pefer not to say')
        ]
        model = UserProfileList
        fields = ('first_name', 'last_name', 'birth_year', 'birth_month', 'birth_day', 'gender', 'profile_pic')
        labels = {
            'first_name' : '',
            'last_name' : '',
            'birth_year' : '',
            'birth_month' : '',
            'birth_day' : '',
            'gender' : '',
            'profile_pic' : ''
        }
        
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control fs-4', 'id' : 'first_name'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control fs-4', 'id' : 'last_name'}),
            'birth_year' : forms.Select(choices=[('', 'Year')] + [(y, y) for y in range(1900, datetime.now().year + 1)], attrs={'class' : 'form-control fs-4', 'id' : 'year'}),
            'birth_month' : forms.Select(choices=[('', 'Month')] + [(i, calendar.month_name[i]) for i in range(1, 13)], attrs={'class' : 'form-control fs-4', 'id' : 'month'}),
            'birth_day' : forms.Select(choices=[('', 'Day')] + [(i, i) for i in range(1, 32)], attrs={'class' : 'form-control fs-4', 'id' : 'day'}),
            'gender' : forms.Select(choices=gender_choices, attrs={'class' : 'form-control fs-4', 'id' : 'gender'}),
            'profile_pic' : forms.FileInput(attrs={'class' : 'form-control fs-4', 'id' : 'profile_pic'})
        }
        
class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'blog_image')
        labels = {
            'title' : '',
            'content' : '',
            'blog_image' : ''
        }
        
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control fs-4', 'id' : 'title'}),
            'content' : TinyMCE(attrs={'cols': 15, 'row' : 10,'class' : 'form-control fs-4', 'id' : 'content'}),
            'blog_image' : forms.FileInput(attrs={'class' : 'form-control fs-4', 'id' : 'blog-image'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
     def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].label = ''
        self.fields['old_password'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['old_password'].widget.attrs['id'] = 'old_password'
        
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['new_password1'].widget.attrs['id'] = 'password'
        
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['new_password2'].widget.attrs['id'] = 'password1'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comments', )
        
        labels = {
            'comments' : '',
        }
        
        widgets = {
            'comments' : TinyMCE(attrs={'row' : 10, 'cols' : 5, 'class' : 'form-control fs-5', 'id' : 'comment`'}),
        }