
from django.urls import path
from . import views


app_name = 'managers_comment'

urlpatterns = [



    path('manager/create-comment/<uuid:trainee_id>/<uuid:department_id>',  views.ManagersCommentView.as_view(), name='create_comment'),

    path('manager/edit-comment/<uuid:comment_id>',  views.ManagersCommentUpdateView.as_view(), name='edit_comment'),
    path('manager/create-comment-trail/<uuid:trainee_id>',  views.ManagersCommentTrailView.as_view(), name='create_comment_trail'),



   
]
