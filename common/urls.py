
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'common'

urlpatterns = [
    path('search-expenses', csrf_exempt(views.search), name="search_expenses"),
    path('dashboard', views.DashboardView.as_view(), name="dashboard_view"),

    
]

