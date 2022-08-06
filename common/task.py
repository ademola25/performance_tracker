from common.send_mail import sendMail
from department.models import Department, User
from gt_hr.celery import app
import datetime
from common.utils import count_log_and_send_mail, sent_for_hod_approval
from gt_logs.models import GtLog
from numbers_of_days.models import NumbersOfDays
from common.utils import end_of_the_day_email_to_unlogged_trainee
from common.utils import end_of_the_week_email_to_unlogged_trainee

# celery -A gt_hr worker -l info --pool=solo


@app.task(name="trainee_to_manager_notification", bind=True)
def trainee_to_manager_notification(self, nod_id, nod_value, nod_department, nod_manager_name, nod_manager_email, trainee_id):
    count_log_and_send_mail(nod_id, nod_value, nod_department,
                            nod_manager_name, nod_manager_email, trainee_id)
    return True


@app.task(name="manager_to_hod_notification", bind=True)
def manager_to_hod_notification(self, managers_comment, hod_name, hod_email, trainee_name, nod_manager_name, nod_manager_email, trainee_id):
    numbers_of_days_list = list(NumbersOfDays.objects.filter(trainee__id = trainee_id).values_list('numbers_of_days', flat=True))
    if "sent_for_managers_approval"in numbers_of_days_list or "pending_all_approvals" in numbers_of_days_list:
        return False
    else:
        sent_for_hod_approval(managers_comment,
                             hod_name, 
                             hod_email,
                            trainee_name,
                            nod_manager_name,
                            nod_manager_email,
                            trainee_id
                            )
        return True


# runs 12 oclock am
@app.task(name="save_log_for_yesterday_and_check_approval_status", bind=True)
def save_log_for_yesterday_and_check_approval_status(self):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    users = User.objects.filter(role='trainee', is_active=True)

    # for user in users:
    #     log = GtLog.objects.filter(
    #         trainee=user.id, log_date__date=yesterday, saved=False).first()

    #     if log:
    #         log.saved = True
    #         log.save()

    #         for department in Department.objects.filter(trainees=user):
    #             number_of_days = NumbersOfDays.objects.filter(
    #                 trainee=user, department=department).first()
    #             gt_logs = GtLog.objects.filter(
    #                 number_of_days=number_of_days, saved=True).count()

    #             if gt_logs == number_of_days.value:
    #                 trainee_to_manager_notification.delay(
    #                     number_of_days.id, number_of_days.value, number_of_days.department.id,
    #                     number_of_days.department.manager.name, number_of_days.department.manager.email,
    #                     number_of_days.trainee.id)


@app.task(name="end_of_day_email_to_unlogged_trainee", bind=True)
def end_of_day_email_to_unlogged_trainee(self):
    today = datetime.date.today()
    todays_logs = GtLog.objects.filter(
        created_at__date=today).values_list('trainee__email')
    todays_list = list(todays_logs)
    trainees = User.objects.filter(role='trainee', is_active=True).values_list(
        'email', flat=True).exclude(email__in=todays_list)
    trainees_email = trainees.values_list(
        'email', flat=True).exclude(email__in=todays_list)
    trainees_name = trainees.values_list(
        'name', flat=True).exclude(email__in=todays_list)
    if trainees:

        for trainee_name, trainee_email in zip(trainees_name, trainees_email):
            end_of_the_day_email_to_unlogged_trainee(
                trainee_name, trainee_email)


@app.task(name="friday_email_notification", bind=True)
def friday_email_notification(self):
    now = datetime.date.today()

    monday = now - datetime.timedelta(days=now.weekday())
    this_monday = str(monday)
    friday = monday + datetime.timedelta(days=4)
    this_friday = str(friday)
    days_inbetween = friday - monday

    days = [monday + datetime.timedelta(days=i)
            for i in range(days_inbetween.days + 1)]
    days_of_the_week = [x.strftime('%Y-%m-%d') for x in list(days)]
    users = User.objects.filter(role='trainee', is_active=True)
    for user in users:

        days_logged_utc = GtLog.objects.filter(trainee=user, log_date__range=[
                                               this_monday, this_friday]).values_list('log_date', flat=True)
        days_logged = [x.strftime('%Y-%m-%d') for x in list(days_logged_utc)]
        unloged_days = set(days_of_the_week) ^ set(days_logged)
        end_of_the_week_email_to_unlogged_trainee(unloged_days, user)
