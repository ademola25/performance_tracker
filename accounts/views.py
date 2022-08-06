from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
from django.contrib.auth import logout
from django.utils.http import is_safe_url
from accounts.forms import LoginForm
from accounts.models import User
from common.auth import BasicAuthentication
# Use the login_required() decorator to ensure only those logged in can access the view.


@login_required
def user_logout(request):
    logout(request)
    # message = ""
    # messages.error(request, message)
    return redirect('accounts:user_login')


class userLogin(View):
    template = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template)

    # @reroute_to_respective_dashboard
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            employee = User.objects.filter(email=email).first()
            if employee:
                allow = BasicAuthentication.ad_auth_web(
                    email, password, employee,
                    request
                )
                if allow:
                    user = authenticate(
                        email=email, password=password, request=request)
                    if user:
                        if user.is_active:
                            route_to_two_fa = False
                            if settings.ENABLE_2FA and hasattr(employee, 'totp_device'):
                                if employee.totp_device.confirmed:
                                    route_to_two_fa = True
                            if route_to_two_fa:
                                cx = {
                                    'email': email,
                                    'password': password,
                                    'next': self.request.POST.get("next", '')
                                }
                                token = request.POST.get('token', None)
                                if token:
                                    if employee.totp_device.device.verify_token(token):
                                        login(request, user)
                                        if "next" in self.request.POST:
                                            redirect_url = self.request.POST["next"]
                                            if is_safe_url(
                                                    redirect_url,
                                                    allowed_hosts=settings.ALLOWED_HOSTS
                                            ):
                                                self.success_url = redirect_url
                                        return self.dispatch(request, args, kwargs)
                                    else:
                                        error = True
                                        message = "Invalid 2FA Token"
                                else:
                                    return render(request, 'accounts/2fa.html', context=cx)
                            else:
                                login(request, user)
                                if "next" in self.request.POST:
                                    redirect_url = self.request.POST["next"]
                                    if is_safe_url(
                                            redirect_url,
                                            allowed_hosts=settings.ALLOWED_HOSTS
                                    ):
                                        return redirect(redirect_url)
                                user_role = user.role
                                if user_role == 'trainee':
                                    return redirect('trainee:trainee_dashboard')
                                elif user_role == 'hr':
                                    return redirect('hr_personnel:hr_personnel_dashboard')
                                elif user_role == 'manager':
                                    return redirect('manager:manager_dashboard')
                                elif user_role == 'hod':
                                    return redirect('hod_dashboard:hod_dashboard')
                                else:
                                    message = "you do not have a role yet. Contact admin"
                                    messages.error(request, message)
                                    return redirect('accounts:user_login')
                        else:
                            message = "your account has been disabled, contact admin"
                            messages.error(request, message)
                            return redirect('accounts:user_login')

        message = "Invalid login details supplied."
        messages.error(request, message)
        return redirect('accounts:user_login')
