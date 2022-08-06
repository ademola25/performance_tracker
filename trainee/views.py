from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
# from datetime import date
import datetime

from numpy import number
from common.custom_mixins.mixins import TraineeRoleRequiredMixin
from common.decorators.function_role_check import trainee_role_and_auth_check
from django.shortcuts import get_object_or_404, redirect, render
#from numpy import number
from pkg_resources import EGG_DIST
from comments.forms import NumbersOfDaysForm
from comments.models import ManagersComment
import department
from department.models import Department, DepartmentKeyObjective, DepartmentManager, DepartmentTrainee, User
from common.utils import count_log_and_send_mail
from gt_logs.models import GtLog
from numbers_of_days.models import NumbersOfDays

from trainee.forms import LogPastDaysForm, TraineeLogForm, TraineeLogUpdateForm
from django.contrib import messages
from datetime import datetime, timedelta
from calendar import HTMLCalendar

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

from trainee.models import Trainee
from .calender import Calendar
from django.views.generic.list import ListView
from django.utils.safestring import mark_safe
from common.task import trainee_to_manager_notification

from django.db.models import Sum


from django.contrib.auth.decorators import login_required


class TraineeDashboardView(TraineeRoleRequiredMixin ,View):
    trainee_dashboard_template = "trainee/dashboard.html"
    
    def get(self, request,**kwargs):
        date_today = datetime.today()
        todays_date = date_today.strftime("%d/%m/%Y")
        form = TraineeLogForm()
        trainee = request.user
        calender_context = {}
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_day = datetime.now().day

        d = get_date(self.request.GET.get('month', None))
        this_date = str(d)
        stringed_month = this_date[5:7]
        stringed_year = this_date[:4]
        num_days = calendar.monthrange(int(stringed_year), int(stringed_month))[1]

        import datetime as dd
        days = [dd.date(int(stringed_year), int(stringed_month), day).strftime('%Y-%m-%d') for day in range(1, num_days+1)]
        weekends = []
        for day in days:
            if len(pd.bdate_range(day, day)) == 0:
                weekends.append(int(day[8:]))
        cal = Calendar(d.year, d.month, d.day, trainee, weekends)
        html_cal = cal.formatmonth(withyear=True)
        calender_context['calendar'] = mark_safe(html_cal)
        number_of_days_sum = NumbersOfDays.objects.filter(trainee=trainee).aggregate(Sum('value'))
        trainee_logs_count = GtLog.objects.filter(trainee=trainee).count()



        now =datetime.today()
        monday = now - timedelta(days = now.weekday())
        this_monday = str(monday)
        friday = monday + timedelta(days=4)
        this_friday = str(friday)
        delta =friday - monday
        days = [monday + timedelta(days=i) for i in range (delta.days + 1)]
        days_of_the_week= [x.strftime('%Y-%m-%d') for x in list(days)]
        days_logged_utc = GtLog.objects.filter(trainee=request.user, log_date__range=[this_monday, this_friday]).values_list('log_date', flat=True)
        days_logged = [x.strftime('%Y-%m-%d') for x in list(days_logged_utc)]
        unloged_days = set(days_of_the_week) ^ set(days_logged)

        # print(type(prev_month(d)), 'gjgjgjg')


        try:
            # print(prev_month(d))
            # trainee_departments = Department.objects.filter(trainees=trainee)
            trainee_departments = DepartmentTrainee.objects.filter(trainee = request.user)
            context = {
                'todaysDate': todays_date,
                'form': form,
                'trainee': trainee,
                'trainee_departments': trainee_departments,
                'calender_context': calender_context,
                'aggregate_nod': number_of_days_sum['value__sum'],
                'trainee_logs_count': trainee_logs_count,
                'unloged_days': list(unloged_days),
                'prev_month': prev_month(d),
                'next_month': next_month(d),
                'current_month':current_month,
               'current_year':current_year, 
                'current_day':current_day,

                # 'weekends':weekends
            }
            return render(request, self.trainee_dashboard_template, context)
        except Exception as e:
            message = 'sorry you have not been assigned to any department yet, contact admin.'
            messages.warning(request, message)
            return redirect('trainee:trainee_dashboard')



    def post(self, request):
        if request.method == 'POST':
            form = TraineeLogForm(request.POST)

            context = {'form': form}
            if form.is_valid():
                log_form = form.save(commit=False)
                # fake trainie replace with real trainie later
                trainee = request.user
                number_of_days = NumbersOfDays.objects.filter(
                    trainee=trainee.id).first()
                log_form.trainee = trainee
                log_form.number_of_days = number_of_days
                log_form.save()
                message = self.message_status(log_form)

                messages.success(request, message)
                return redirect('trainee:trainee_dashboard')
            else:
                messages.error(request, form.errors)
                return render(request, self.trainee_dashboard_template, context)

    def message_status(self, form_object):
        form_saved = form_object.saved
        if form_saved == True:
            message = 'Your log was successfully saved '
            return message

        else:
            message = 'Your log has been saved temporarily.'
            return message



import calendar

def get_date(req_month):
    from datetime import datetime, timedelta, date
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class TraineeDetailPage(TraineeRoleRequiredMixin, View):
    trainee_details_template = "trainee/trainee_detail.html"
    def get(self, request,  trainee_id, department_id):
        today = datetime.today()
        todays_date = today.strftime("%B %d, %Y")
        trainee = request.user
        department = Department.objects.filter(id=department_id).first()
        manager = DepartmentManager.objects.filter(department = department_id).first()

        number_of_days_details = NumbersOfDays.objects.filter(
            department=department, trainee=trainee).first()

        # temporary gt logs for today 
        tempoary_gt_log = GtLog.objects.filter(
            trainee=trainee, log_date__year=today.year, log_date__month=today.month, log_date__day=today.day).first()

        # parmanent gt logs for today 
        todays_gt_log = GtLog.objects.filter(
            trainee=trainee, log_date__year=today.year, log_date__month=today.month, log_date__day=today.day).first() 

        #all parmanent gtlogs in this department for his number of days
        all_permanent_gt_log = GtLog.objects.filter(number_of_days = number_of_days_details)
        departments_kpi = DepartmentKeyObjective.objects.filter(department = department_id)

   

        create_log_form = TraineeLogForm()
        update_log_form = TraineeLogForm(instance=tempoary_gt_log)

        context = {'todays_date': todays_date,
                 'tempoary_gt_log': tempoary_gt_log,
                  'all_permanent_gt_log': all_permanent_gt_log,
                   'todays_gt_log': todays_gt_log,
                   'create_log_form': create_log_form,
                    'update_log_form': update_log_form,
                     'trainee': trainee,
                      'department': department,
                       'number_of_days_details': number_of_days_details,
                       'departments_kpi':departments_kpi
                       }
        return render(request, self.trainee_details_template, context)

    def post(self, request, trainee_id, department_id):
        trainee = request.user
        today = datetime.today()
        manager = DepartmentManager.objects.filter(department = department_id).first()
        if request.method == 'POST':
            form = TraineeLogForm(request.POST)
            context = {'form': form}
            if form.is_valid():
                number_of_days = NumbersOfDays.objects.filter(
                    trainee=trainee, department=department_id).first()
                if 'create_log_permanently' in request.POST:
                    create_log_form = form.save(commit=False)
                    selected_kpi = request.POST.get("key_objective", "")
                    create_log_form.trainee = trainee
                    create_log_form.number_of_days = number_of_days
                    create_log_form.saved = True
                    if selected_kpi != "":
                        selected_kpi = DepartmentKeyObjective.objects.filter(id = selected_kpi).last()
                        create_log_form.department = selected_kpi.department
                        create_log_form.kpi = selected_kpi
                        create_log_form.save()
                        trainee_to_manager_notification.delay(
                            number_of_days.id,
                            number_of_days.value,
                            number_of_days.department.id,

                            manager.manager.name,
                            manager.manager.email,
                            number_of_days.trainee.id
                            )
                        message = self.message_status(create_log_form)
                        messages.success(request, message)
                        return redirect('trainee:trainee_dashboard')
                    else:
                        messages.warning(request, "Please select a Kpi")
                        return redirect('trainee:trainee_details', trainee_id, department_id)
                elif 'edit_log_permanently' in request.POST:
                    obj = get_object_or_404(
                        GtLog, trainee=trainee, log_date__year=today.year, log_date__month=today.month, log_date__day=today.day)
                    update_log_form = TraineeLogForm(
                        request.POST or None, instance=obj)
                    selected_kpi = request.POST.get("key_objective", "")

                    if selected_kpi != "":
                        selected_kpi_object = DepartmentKeyObjective.objects.filter(id = selected_kpi).last()
                        obj.kpi = selected_kpi_object
                    

                    obj.saved = True
                    obj.save()
                    update_log_form.save()
                    context = {'update_log_form': update_log_form}
                    message = "your Log has been saved!"
                    messages.success(request, message)
                    return redirect('trainee:trainee_dashboard')
                else:

                    message = 'something went wrong, Try again or contact admin'
                    messages.warning(request, message)
                    return redirect('trainee:trainee_dashboard')
            else:
                messages.error(request, update_log_form.errors)
                return redirect('trainee:trainee_dashboard')

        else:
            create_log_form = TraineeLogForm()
            update_log_form = TraineeLogForm()
            return render(request, self.trainee_details_template, {'create_log_form': create_log_form, 'update_log_form': update_log_form})


    def message_status(self, form_object):
        form_saved = form_object.saved
        if form_saved == True:
            message = 'Your log was successfully saved '
            return message
        else:
            message = 'Your log has been saved temporarily.'
            return message


def trainee_detailed_page(request):
    pass


# update view for details
@login_required
def trainee_log_update(request):
    # dictionary for initial data with
    # field names as keys

    trainee_dashboard_template = "trainee/components/updatetime.html"
    # fetch the object related to passed id
    log = GtLog.objects.filter(log_date__startswith=datetime.today()).first()

    # pass the object as instance in form
    update_form = TraineeLogForm(request.POST or None, instance=log)
    context = {'update_form': update_form}

    # save the data from the form and
    # redirect to detail_view
    if update_form.is_valid():
        update_form.save()
        return redirect('trainee:trainee_dashboard')
    else:
        context = {'update_form': update_form,
                   'error': 'The form was not updated successfully. Please enter in a title and content'}

    # add form dictionary to context
    return render(request, trainee_dashboard_template, context)


class LogPastDays(TraineeRoleRequiredMixin, View):
    trainee_details_template = "trainee/log_past_days.html"
    @trainee_role_and_auth_check
    def get(self, request,  day, month):
        trainee = request.user
        
        
        todays_date = datetime.today()
        current_year = str(todays_date.year)
        selected_date = f'{current_year}-{month}-{day}'
        res = len(pd.bdate_range(selected_date, selected_date))
        if res == 0:
            message = 'sorry you Can not log on a weekend.'
            messages.warning(request, message)
            return redirect('trainee:trainee_dashboard')

        else:
            my_department = list(DepartmentTrainee.objects.filter(trainee = request.user).values_list('department__department_name', flat=True))
            departments_kpi = DepartmentKeyObjective.objects.filter(department__department_name__in = my_department)
            log_for_this_day = GtLog.objects.filter(trainee=trainee, log_date__month=month, log_date__day=day).last()
            if log_for_this_day is None:
                form = LogPastDaysForm()
                today = datetime.today()
                todays_date = today.strftime("%B %d, %Y")
                context = {'form': form, "month": month, "day": day, 'log_type':"create", "departments_kpi":departments_kpi}
                return render(request, self.trainee_details_template, context)
            else:
                form = TraineeLogUpdateForm(request.POST or None, instance=log_for_this_day)

                

                context = {'form': form, "month": month, "day": day, 'log_type':"edit", "departments_kpi":departments_kpi}
                return render(request, self.trainee_details_template, context)
                            
    def post(self, request, day, month):
        if request.method == 'POST':
            if 'edit' in request.POST:
                log_for_this_day = GtLog.objects.filter(trainee=request.user, log_date__month=month, log_date__day=day).last()
                form = TraineeLogUpdateForm(request.POST or None, instance=log_for_this_day)
                if form.is_valid():
                    selected_kpi = request.POST.get("key_objective", "")
                    if selected_kpi != "":
                        selected_kpi_object = DepartmentKeyObjective.objects.filter(id = selected_kpi).last()
                        trainee_log_update_form = form.save(commit=False)
                        trainee_log_update_form.kpi = selected_kpi_object
                        trainee_log_update_form.department = selected_kpi_object.department
                        trainee_log_update_form.save()
                        message = 'you have succesfully edited your logged'
                        messages.success(request, message)
                        return redirect('trainee:trainee_dashboard') 
                    else:
                        messages.warning(request, "Please select a Kpi")
                        return redirect('trainee:log_days', day, month)
                else:
                    # print(form.errors)
                    messages.warning(request, form.errors)
                    return redirect('trainee:trainee_dashboard')
            else:
                # form = LogPastDaysForm(request.POST, user = request.user)
                form = LogPastDaysForm(request.POST)

                if form.is_valid():
                    selected_kpi = request.POST.get("key_objective", "")
                    if selected_kpi != "":
                        selected_kpi_object = DepartmentKeyObjective.objects.filter(id = selected_kpi).last()
                        my_number_of_days = NumbersOfDays.objects.filter(trainee = request.user, department =selected_kpi_object.department ).first()
                        my_department_logs = GtLog.objects.filter(number_of_days = my_number_of_days).count()
                    else:
                        messages.warning(request, "Please select a Kpi")
                        return redirect('trainee:log_days', day, month)
                    if my_department_logs >=  my_number_of_days.value:
                        messages.warning(request, f"your Logs for {my_number_of_days.department.department_name} department has been completed. Log for another department")
                        return redirect('trainee:log_days', day, month)

                    else:

                        todays_date = datetime.today()
                        current_year = str(todays_date.year)
                        selected_date = f'{current_year}-{month}-{day}'
                        log_past_dates = form.save(commit=True)
                        log_past_dates.saved = True
                        log_past_dates.log_date = selected_date
                        log_past_dates.trainee = request.user
                        log_past_dates.number_of_days = my_number_of_days
                        if selected_kpi != "":
                            log_past_dates.department = selected_kpi_object.department
                            log_past_dates.kpi = selected_kpi_object
                        log_past_dates.save()
                        my_departments = Department.objects.filter(id= selected_kpi_object.department.id).last()
                        departmet_manager = DepartmentManager.objects.filter(
                            department = my_departments
                        ).last()
                        trainee_to_manager_notification.delay(
                            my_number_of_days.id,
                            my_number_of_days.value,
                            selected_kpi_object.department.id,

                            departmet_manager.manager.name,
                            departmet_manager.manager.email,
                            my_number_of_days.trainee.id,
                        )
                        
                        message = f'you have logged for {selected_date}'
                        messages.success(request, message)
                        return redirect('trainee:trainee_dashboard')
                else:
                    # print(form.errors)
                    messages.warning(request, form.errors)
                    return redirect('trainee:trainee_dashboard')


class UnloggedDaysView(TraineeRoleRequiredMixin, View):
    trainee_dashboard_template = "trainee/unlogged_day_view.html"
    def get(self, request,  year, month, day, user_id):
        date = year+'-'+month+'-'+day

        form = LogPastDaysForm(user = request.user)
        context={
            'date':date,
            'user_id':user_id,
            'form':form
        }

        return render(request, self.trainee_dashboard_template, context)

    def post(self, request, year, month, day, user_id):
        date = year+'-'+month+'-'+day
        if request.method == 'POST':

            form = LogPastDaysForm(request.POST, user = request.user)
            context = {'form': form}



            if form.is_valid():
                my_number_of_days = NumbersOfDays.objects.filter(trainee = request.user, department =form.cleaned_data['departments'] ).first()
                my_department_logs = GtLog.objects.filter(number_of_days = my_number_of_days).count()
                if my_department_logs >=  my_number_of_days.value:
                    messages.warning(request, f"your Logs for {my_number_of_days.department.department_name} department has been completed. Log for another department")
                    return redirect('trainee:log_past_days', year, month, day, request.user.id)
                else:
                    todays_date = datetime.today()
                    current_year = str(todays_date.year)
                    # selected_date = f'{current_year}-{month}-{day}'
                    log_past_dates = form.save(commit=True)
                    log_past_dates.saved = True
                    log_past_dates.log_date = date
                    log_past_dates.trainee = request.user
                    log_past_dates.number_of_days = my_number_of_days
                    log_past_dates.save()
                    trainee_to_manager_notification.delay(
                        my_number_of_days.id,
                        my_number_of_days.value,
                        my_number_of_days.department.id,
                        my_number_of_days.trainee.id,
                        my_number_of_days.department.manager.name,
                        my_number_of_days.department.manager.email,
                        )

                    message = f'you have logged for {date}'
                    messages.success(request, message)
                    return redirect('trainee:trainee_dashboard')
            else:
                messages.warning(request, form.errors)
                return redirect('trainee:trainee_dashboard')




class NoDepartmentView(View):
    trainee_dashboard_template = "trainee/no_dashboard.html"

    @trainee_role_and_auth_check
    def get(self, request):
        context = {}
        return render(request, self.trainee_dashboard_template, context)
