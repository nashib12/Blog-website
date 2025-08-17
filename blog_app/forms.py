from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Enter your user-name'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    
    