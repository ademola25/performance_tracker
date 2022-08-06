from django.urls import path
from . import views


app_name = 'manager'

urlpatterns = [
    path('dashboard',  views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('add-manager', views.add_manager, name="add_manager"),
    path('edit-manager/<int:id>', views.manager_edit, name="manager_edit"),
    path('manager-delete/<int:id>', views.delete_manager, name="manager_delete"),
 
    path('trainee/logs/<uuid:id>/<uuid:department_id>',  views.TraineeLogsView.as_view(), name='trainee_logs'),

    path('trainee/dashboard/<uuid:trainee_id>/<uuid:department_id>',  views.managerTraineeDashboardView.as_view(), name='manager_trainee_dashboard_view'),
    path('all/trainees',  views.ManagerTraineeListView.as_view(), name='manager_trainee_list'),

]

