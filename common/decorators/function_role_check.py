from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def manager_role_and_auth_check(view_func):
    def wrap(request, *args, **kwargs):
        if request.request.user.is_anonymous:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
        elif request.request.user.role == "manager":
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
    return wrap


def hr_role_and_auth_check(view_func):
    def wrap(request, *args, **kwargs):
        if request.request.user.is_anonymous:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
        elif request.request.user.role == "hr":
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
    return wrap


def hod_role_and_auth_check(view_func):
    def wrap(request, *args, **kwargs):
        if request.request.user.is_anonymous:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
        elif request.request.user.role == "hod":
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
    return wrap

def trainee_role_and_auth_check(view_func):
    def wrap(request, *args, **kwargs):
        if request.request.user.is_anonymous:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
        elif request.request.user.role == "trainee":
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
    return wrap



def manager_admin_role_and_auth_check(view_func):
    def wrap(request, *args, **kwargs):
        if request.request.user.is_anonymous:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
        elif request.request.user.role == "hr" or  request.request.user.role == "manager":
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request.request, "Please Login")
            return redirect('accounts:user_login')
    return wrap



# def manager_admin_role_and_auth_check(view_func):
#     def wrap(request, *args, **kwargs):
#         if request.request.user.is_anonymous:
#             messages.warning(request.request, "Please Login")
#             return redirect('accounts:user_login')
#         elif request.request.user.role == "hr" or  request.request.user.role == "manager" or request.request.user.role == "hod":
#             return view_func(request, *args, **kwargs)
#         else:
#             messages.warning(request.request, "Please Login")
#             return redirect('accounts:user_login')
#     return wrap






def reroute_to_respective_dashboard(view_func):
    def wrap(request, *args, **kwargs):
        if request.request.user.is_anonymous:
            return view_func(request, *args, **kwargs)
        elif request.request.user.role == "hr":
            return redirect('hr_personnel:hr_personnel_dashboard')
        elif request.request.user.role == "manager":
            return redirect('manager:manager_dashboard')
            
        elif request.request.user.role == "trainee":
            return redirect('trainee:trainee_dashboard')
        elif request.request.user.role == "hod":
            return redirect('hod_dashboard:hod_dashboard')
    return wrap

