from django.urls import path

from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('registration/',registration,name="registration"),
    path("log_in/",log_in,name="log_in"),
    path("log_out/",log_out,name="log_out"),
    path("create_profile/", create_profile,name="create-profile"),
]
