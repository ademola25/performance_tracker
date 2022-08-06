
from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('',  views.userLogin.as_view(), name='user_login'),
    path('logout',  views.user_logout, name='user_logout'), 
]

