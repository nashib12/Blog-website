import re

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

def email_validate(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(_(f"Email: {email} already exists !!!"))
    
def password_validate(password): 
    pattern = r"[!@#$%^&*(),.?\":{}|<>]"
    if not re.search(pattern, password):
        raise ValidationError(_("Password must contain at least one special character."))

def check_username(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError(_(f"Username: {username} already exists !!!"))