
from django.urls import path
from . import views


urlpatterns = [
    #path('dashboard',  views.DepartmentDashboardView.as_view(), name='manager_dashboard'),
    path('add-department', views.add_department, name="add-department"),
    path('edit-department/<int:id>', views.department_edit, name="department-edit"),
    path('department-delete/<int:id>', views.delete_department, name="department-delete"),
]
