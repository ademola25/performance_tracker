
from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

app_name="hr_personnel"
urlpatterns = [
    path('dashboard',  views.HrPersonnelDashboardView.as_view(), name='hr_personnel_dashboard'),
    path('all-trainees',  views.TraineeListView.as_view(), name='all_trainees'),

    path('all-managers',  views.ManagersListView.as_view(), name='all_managers'),
    path('all-hods',  views.HodsListView.as_view(), name='all_hods'),
    path('all-departments',  views.DepartmentsListView.as_view(), name='all_departments'),
    path('edit-user/<uuid:user_id>',  views.user_update_view, name='edit_user'),
    path('delete-user/<uuid:user_id>',  views.delete_view, name='delete_user'),
    path('manager-delete/<uuid:user_id>',  views.manager_delete_view, name='delete_manager'),

    path('trainee-delete/<uuid:user_id>',  views.trainee_delete_view, name='delete_manager'),

    
    path('delete-department/<uuid:department_id>',  views.DeleteDepartmentsView.as_view(), name='delete_department'),
    path('manager-delete/<uuid:user_id>',  views.manager_delete_view, name='delete_manager'),

    path('trainee-delete/<uuid:user_id>',  views.trainee_delete_view, name='delete_trainee'),

    path('trainee/details/<uuid:trainee_id>',  views.TraineeDetailsView.as_view(), name='trainee_details_view'),



    path('update/<uuid:department_id>', views.department_update_view, name = "department_update"),

    # path('update/<uuid:id>', views.DepartmentUpdateView.as_view(), name = "department_update"),

]

