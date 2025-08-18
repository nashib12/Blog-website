from django import forms

from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Enter your user-name'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    
class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model =  Profile
        fields = ('contact', 'profile_pic')