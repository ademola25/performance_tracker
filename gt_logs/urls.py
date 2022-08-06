from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trainee/', include('trainee.urls')),
    path('hr-personnel/', include('hr_personnel.urls')),

    path('department/', include('department.urls')),
    path('manager/', include('manager.urls')),
    # path('numbers_of_days/', include('numbers_of_days.urls')),
    path('hod/', include('hod.urls')),
    path('comments/', include('comments.urls')),


    path('', include('accounts.urls')),


    # path('login/',  user_login, name='user_login'),





]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

