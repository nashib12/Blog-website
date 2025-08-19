from django.urls import path

from .views import *

urlpatterns = [
    path('',home,name="home"),
    
    # --------------- Authentication and registration ---------------
    path('registration/',registration,name="registration"),
    path("log_in/",log_in,name="log-in"),
    path("log_out/",log_out,name="log-out"),
    path("create_profile/", create_profile,name="create-profile"),
    
    # ------------------ Blog Section ------------------
    path("create_blog/",create_blog,name="create-blog"),
    path("update_blog/<int:id>",update_blog,name="update-blog"),
    path("delete_blog/<int:id>",delete_blog,name="delete-blog"),
]
