from django.core.mail import send_mail
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings


def sendMail(recipients=None, cc=None, subject=None, content=None, function_name=None, manager_name=None, trainee_id=None, hod_name=None, trainee_name=None, days_not_logged=None):

    if function_name == 'count_log_and_send_mail':
        template_name = 'email/trainee_onsave_notification.html'
        context = {
            "recipients": recipients,
            "cc": cc,
            "subject": subject,
            "content": content,
            "function_name": function_name,
            "website": settings.APP_WEBSITE,
            "function_name": function_name,
            "manager_name": manager_name,
            "trainee_id": trainee_id,
            "trainee_name":trainee_name
        }
    elif function_name == 'sent_for_hod_approval':
        template_name = 'email/manager_onsave_notification.html'
        context = {
            "recipients": recipients,
            "cc": cc,
            "subject": subject,
            "content": content,
            "function_name": function_name,
            "website": settings.APP_WEBSITE,
            "function_name": function_name,
            "manager_name": manager_name,
            "trainee_name": trainee_name,
            "hod_name": hod_name

        }
    elif function_name == 'end_of_the_day_email_to_unlogged_trainee':
        template_name = 'email/trainee_eod_notification.html'
        context = {
            "recipients": recipients,
            "subject": subject,
            "content": content,
            "function_name": function_name,
            "trainee_name": trainee_name,
            "website": settings.APP_WEBSITE

        }
    elif function_name == 'end_of_the_week_email_to_unlogged_trainee':
        template_name = 'email/trainee_eoweek_notification.html'
        context = {
            "recipients": recipients,
            "subject": subject,
            "content": content,
            "function_name": function_name,
            "trainee_name": trainee_name,
            "days_not_logged": days_not_logged,
            "trainee_id": trainee_id,
            "website": settings.APP_WEBSITE
        }
    else:
        pass
    html_data = render_to_string(template_name, context)
    try:
        send_mail(subject, '', settings.ADMIN_EMAIL, [
                  recipients, ], fail_silently=False, html_message=html_data)

    except BadHeaderError:

        raise Exception("Something went wrong contact admin")
