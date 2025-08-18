import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Profile

@receiver(post_delete, sender=Profile)
def profile_img_delete(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)
            print("Photo deleted!!")
            