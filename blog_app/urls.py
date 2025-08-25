from django.urls import path

from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('gallery', gallery, name="gallery"),
    
    # --------------- Authentication and registration ---------------
    path('registration/',registration,name="registration"),
    path("log_in/",log_in,name="log-in"),
    path("log_out/",log_out,name="log-out"),
    path("create_profile/", create_profile,name="create-profile"),
    path("change_password/",change_password,name='change-password'),
    
    # ------------------ Blog Section ------------------
    path("create_blog/",create_blog,name="create-blog"),
    path("update_blog/<int:id>",update_blog,name="update-blog"),
    path("delete_blog/<int:id>",delete_blog,name="delete-blog"),
    path("view_profile/",view_profile,name="view-profile"),
    path("comment/<int:id>",blog_comment,name="comment"),
    path("delete_comment/<int:id>",delete_comment,name='delete-comment'),
    path("block_comment/<int:id>",block_comment,name="block-comment"),
    path("like_post/<int:id>", count_like,name="like"),
    
    #-------------- Admin section ----------------
    path("dashboard/",view_dashboard,name="dashboard"),
    path("change_status/<int:id>",change_status,name="change-status"),
    path("approve_post/<int:id>",approve_post,name="approve-post"),
    
    # -------------------- Gallery Section --------------
    path("add_image/",add_gallery_img,name="add-image"),
    path("album/",create_album,name="create-album"),
]
