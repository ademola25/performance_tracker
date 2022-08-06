
from accounts.models import User
from comments.models import HodsComment
from common.send_mail import sendMail
from department.models import Department
from gt_logs.models import GtLog
from datetime import datetime, timedelta, time
import pandas as pd
from .mail_subjects import *
from .mail_content import *

from django.core.mail import send_mail


def weekend_or_weekday():
    today = datetime.now()
    res = len(pd.bdate_range(today, today))
    if res == 0:
        return 'weekend'
    else:
        return 'weekday'


def count_log_and_send_mail(nod_id, nod_value, nod_department, nod_manager_name, nod_manager_email, trainee_id):
    logs = GtLog.objects.filter(number_of_days=nod_id, saved=True)
    #get all logs 

    if logs is not None:

        if logs.count() == nod_value:

            trainee = logs.first().trainee.name
            department = nod_department
            manager_name = nod_manager_name
            manager_email = nod_manager_email

            #manager = department.manager
            mail_subject = "Graduate Trainee Activity Log Completion"
            #context = {'manager_name': manager_name, }
            trainee_name = User.objects.filter(id = trainee_id).first()
            sendMail(recipients=manager_email, cc=trainee, subject=mail_subject,
                     content=Trainee_log_complete_content, function_name='count_log_and_send_mail', manager_name=nod_manager_name, trainee_id=trainee_id, trainee_name=trainee_name.name)

# runs at the end of work everyday 5:pm
def todays_unlogged_trainees():
    if weekend_or_weekday() == 'weekday':
        today = datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        users = User.objects.filter(role="trainee", is_active=True)
        for user in users:
            logs = GtLog.objects.filter(
                trainee=user, create_at__gte=today, created_at__lt=tomorrow, saved=True)
            if logs is not None:
                if logs.saved == False:
                    # send mail he has not saved and log will be saved by 12
                    pass
            else:
                # send mail he has not logged
                pass


def fridays_unlogged_trainees():

    pass

# runs 12:01 everyday


def save_unsaved_logs():
    unsaved_logs = GtLog.objects.filter(
        trainee__role="trainee", trainee__is_active=True, saved=False)
    if unsaved_logs is not None:
        for log in unsaved_logs:
            log.saved = True
            log.save()


def sent_for_hod_approval(managers_comment, hod_name, hod_email, trainee_name, nod_manager_name, nod_manager_email, trainee_id):
    # HodsComment.objects.filter(managers_comment=managers_comment).first()

    
    # department = Department.objects.filter(
    #     manager__email=nod_manager_email).first()
    #hod = department.hod
    #manager = department.manager
    mail_subject = "Graduate Trainee Activity Log completion"
    sendMail(recipients=hod_email, cc=nod_manager_email, subject=mail_subject,
             content=send_for_hod_approval_content, function_name='sent_for_hod_approval', manager_name=nod_manager_name, trainee_name=trainee_name, hod_name=hod_name)

    # send email to hod


def end_of_the_day_email_to_unlogged_trainee(trainee_name, trainee_email):
    mail_subject = 'Pending Daily Activity Log'
    content = f'Dear {trainee_name}, This is a reminder to log your activities for the day'
    function_name = 'end_of_the_day_email_to_unlogged_trainee'
    sendMail(recipients=trainee_email, subject=mail_subject, content=content,
             function_name=function_name, trainee_name=trainee_name)
# trainee_email trainee_name subject


def end_of_the_week_email_to_unlogged_trainee(days_not_logged, trainee):
    mail_subject = " Pending activity logs for the week"
    content = 'This is a reminder to log your activities for all the days you missed'
    function_name = 'end_of_the_week_email_to_unlogged_trainee'
    sendMail(recipients=trainee.email, subject=mail_subject, content=content,
             function_name=function_name, trainee_name=trainee.name, days_not_logged=days_not_logged, trainee_id=trainee.id)
