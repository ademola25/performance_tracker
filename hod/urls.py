from django.urls import path
from . import views



app_name = 'hod_dashboard'
urlpatterns = [
    path('dashboard',  views.HodDashboardView.as_view(), name='hod_dashboard'),
    path('add-hod', views.add_hod, name="add-hod"),
    path('edit-hod/<int:id>', views.hod_edit, name="hod-edit"),
    path('hod-delete/<int:id>', views.delete_hod, name="hod-delete"),

    path('trainee/logs/<uuid:manager_id>/<uuid:trainee_id>/<uuid:department_id>',  views.HodTraineeLogsView.as_view(), name='hod_trainee_logs'),
    path('trainee/details/<uuid:manager_id>/<uuid:trainee_id>/<uuid:department_id>',  views.HodTraineeDashboardView.as_view(), name='hod_trainee_details'),


    path('awaiting/approval',  views.TraineesAwaitingApprovalView.as_view(), name='awaiting_approval'),
    path('all/trainees',  views.HodTraineeListView.as_view(), name='hod_trainee_list'),
    path('all-trainee/details/<uuid:trainee_id>',  views.HodTraineeDetailsView.as_view(), name='hod_trainee_detail_list'),
    path('trainee/logs/details/<uuid:manager_id>/<uuid:trainee_id>/<uuid:department_id>',  views.HodTraineeDetailLogsView.as_view(), name='hod_trainee_logs_details'),




    # path('comment/<uuid:managers_comment>',  views.HodCommentView.as_view(), name='hod_comment'),




]