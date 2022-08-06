
from django.urls import path
from . import views



app_name = 'trainee'


urlpatterns = [
    path('dashboard',  views.TraineeDashboardView.as_view(), name='trainee_dashboard'),
    path('no-department',  views.NoDepartmentView.as_view(), name='trainee_no_department'),

    path('details/<uuid:trainee_id>/<uuid:department_id>',  views.TraineeDetailPage.as_view(), name='trainee_details'),

    path('log/past-day/<str:day>/<str:month>',  views.LogPastDays.as_view(), name='log_days'),

    path('log/past-day/<str:year>/<str:month>/<str:day>/<uuid:user_id>',  views.UnloggedDaysView.as_view(), name='log_past_days'),



    path('qw',  views.trainee_log_update, name='update'),


    
]
