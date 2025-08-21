from django.shortcuts import redirect
from django.contrib import messages

def unautorized_access(view_func):
    def wrap_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "Unauthorized access")
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)
    return wrap_func

def admin_only(view_func):
    def wrap_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Only admin can acces this page")
            return redirect("home")
    return wrap_func