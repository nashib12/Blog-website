import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Profile, Blog

# delete file related to the profile after profile is deleted
@receiver(post_delete, sender=Profile)
def profile_img_delete(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)
            
@receiver(post_delete, sender=Blog)
def blog_img_delete(sender, instance, **kwargs):
    if instance.blog_image:
        if os.path.isfile(instance.blog_image.path):
            os.remove(instance.blog_image.path)
          
# replace the old image with new image  
@receiver(pre_save, sender=Blog)
def change_blog_image(sender, instance, **kwargs):
    if not instance.id:
        return
    try:
        old_photo = Blog.objects.get(id=instance.id).blog_image
    except Blog.DoesNotExist:
        return
  
    new_photo = instance.blog_image
    if old_photo and old_photo != new_photo:
        if os.path.isfile(old_photo.path):
            os.remove(old_photo.path)