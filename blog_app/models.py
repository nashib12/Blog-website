from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    content = HTMLField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Blog Post'
        managed = True
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
    
    
