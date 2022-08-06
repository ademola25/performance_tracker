from email import message
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import AccessMixin


# Custom  roles start 
class HrRoleRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and role is appropriate."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:user_login')
        if request.user.role != 'hr': 
            return redirect('common:dashboard_view')
        return super().dispatch(request, *args, **kwargs)

class TraineeRoleRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and role is appropriate."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:user_login')
        if  request.user.role !='trainee': 
            return redirect('common:dashboard_view')
        return super().dispatch(request, *args, **kwargs)


class ManagerRoleRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and role is appropriate."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:user_login')
        if  request.user.role !='manager': 
            return redirect('common:dashboard_view')
        return super().dispatch(request, *args, **kwargs)


class HodRoleRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and role is appropriate."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:user_login')
        if  request.user.role !='hod': 
            return redirect('common:dashboard_view')
        return super().dispatch(request, *args, **kwargs)
