from django.shortcuts import get_object_or_404, render, redirect
from django import views
import json
from comments.models import ManagersComment
from common.custom_mixins.mixins import ManagerRoleRequiredMixin
from common.decorators.function_role_check import manager_admin_role_and_auth_check, manager_role_and_auth_check
from department.models import Department, DepartmentManager, DepartmentTrainee
from accounts.models import User
from gt_logs.models import GtLog
from manager.forms import ManagerGradingForm
from numbers_of_days.models import NumbersOfDays
from trainee.models import Trainee
from . models import Manager
from django.contrib import messages
#from django.core.paginator import Paginator
from django.db.models import Count

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.views import View

#from common.utils import count_log_and_send_mail, sent_for_hod_approval

from datetime import date, datetime

from django.views.generic import UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from common.custom_mixins.mixins import HodRoleRequiredMixin, ManagerRoleRequiredMixin, HrRoleRequiredMixin, TraineeRoleRequiredMixin

from django.db.models import Sum


class ManagerDashboardView(ManagerRoleRequiredMixin, View):
    manager_dashboard_template = "manager/dashboard.html"

    # @manager_role_and_auth_check
    def get(self, request):
        manager = request.user
        department = list(DepartmentManager.objects.filter(manager=manager).values_list('department__department_name', flat=True))
        print(department)
        

    
            # trainees = DepartmentTrainee.objects.filter(department__department_name__in = department)


        trainees = DepartmentTrainee.objects.filter(department__department_name__in = department).count()
        trainees_awaiting_hod = NumbersOfDays.objects.filter(department__department_name__in= department, numbers_of_days = 'sent_for_hods_approval').count()
        trainees_pending_all = NumbersOfDays.objects.filter(department__department_name__in= department, numbers_of_days = 'pending_all_approvals').count()
        trainees_approved = NumbersOfDays.objects.filter(department__department_name__in= department,numbers_of_days = 'approved_by_hod' ).count()

        trainees_awaiting_manager = NumbersOfDays.objects.filter(department__department_name__in= department,numbers_of_days = 'sent_for_managers_approval' ).count()
        trainees_disapproved = NumbersOfDays.objects.filter(department__department_name__in= department,numbers_of_days = 'disapproved_by_hod' ).count()

            # trainees = department.department.department_departmenttrainees.all()
#             print(trainees, trainees_awaiting_hod,
# trainees_pending_all,
# trainees_approved,
# trainees_awaiting_manager,
# trainees_disapproved)

        context = {
        'manager': manager,
        'department': department,
        'trainees': trainees,
        'trainees_count':trainees,
        'trainees_awaiting_hod':trainees_awaiting_hod,
        'trainees_pending_all':trainees_pending_all,
        'trainees_approved':trainees_approved,
        'trainees_awaiting_manager':trainees_awaiting_manager,
        'trainees_disapproved':trainees_disapproved,
        }

        return render(request, self.manager_dashboard_template, context)


# class TraineeDetailsView (HrRoleRequiredMixin, View):
#     trainee_details_template = "hr_personnel/trainee/trainee_details.html"
#     def get(self, request, trainee_id):
#         trainee = get_object_or_404(User, id=trainee_id)
#         #department = Department.objects.filter(trainees=trainee_id).first()
#         number_of_days = NumbersOfDays.objects.filter(trainee = trainee_id)
#         context = {
#                     'trainee':trainee,
#                     "number_of_days":number_of_days
                
#                 }
#         #if number_of_days is not None:
            
#         return render(request, self.trainee_details_template, context)


class TraineeLogsView (LoginRequiredMixin, View):
    trainee_log_template = "manager/trainee_log.html"
    login_url = 'accounts:user_login'
    redirect_field_name = 'manager:trainee_logs'

    # @manager_admin_role_and_auth_check
    def get(self, request, id, department_id):
        if request.user.role == 'manager':
           
            trainee = get_object_or_404(User, id=id)

            department = trainee.trainee_departmenttrainees.filter(department = department_id, trainee = id).first()

            gt_logs = GtLog.objects.filter(trainee=id, department = department_id)
            number_of_days = NumbersOfDays.objects.filter(trainee =id, department = department_id).last()
            object_num_of_days = number_of_days
            
            if gt_logs.count() >= number_of_days.value:
                show_approval = True
            else:
                show_approval = False
            manager = request.user
            managers_comment = ManagersComment.objects.filter( trainee=id, manager=manager).first()
            context = {
                'trainee':trainee,
                'number_of_days':number_of_days,
                'trainee_id': id,
                'gt_logs': gt_logs,
                'managers_comment': managers_comment,
                'department':department,
                'show_approval':show_approval,
                'object_num_of_days':object_num_of_days
            }
        else:
            gt_logs = GtLog.objects.filter(trainee=id)
            trainee = get_object_or_404(User, id= id)
            number_of_days = NumbersOfDays.objects.filter(trainee =id)
            department = Department.objects.filter(department_departmenttrainees=id).first()
            context = {
                'trainee':trainee,
                'number_of_days':number_of_days,
                'trainee_id': id,
                'gt_logs': gt_logs,
                'department':department
            }
        return render(request, self.trainee_log_template, context)


class managerTraineeDashboardView (LoginRequiredMixin, View):
    template = "manager/manager_trainee_dashboard.html"
    login_url = 'accounts:user_login'
    redirect_field_name = 'manager:manager_trainee_dashboard_view'
    # @manager_admin_role_and_auth_check

    def get(self, request, trainee_id, department_id):
        sent_for_approval = ManagersComment.objects.filter(trainee=trainee_id, manager=request.user).first()
        form = ManagerGradingForm()
        trainee = get_object_or_404(User, id=trainee_id)
        department = trainee.trainee_departmenttrainees.filter(department = department_id, trainee = trainee_id).first()
        number_of_days = NumbersOfDays.objects.filter(trainee=trainee_id).first()

        context = {
            'trainee': trainee,
            "department": department,
            "number_of_days": number_of_days,
            "form": form,
            "log_count": trainee.gtlog_set.all().count(),
            'sent_for_approval': sent_for_approval
        }
        
        return render(request, self.template, context)

    def post(self, request, trainee_id, department_id):
        # if request.method == 'POST':
        #     sent_for_approval = ManagersComment.objects.filter(
        #         trainee=trainee_id, manager=request.user).first()
        #     if sent_for_approval is None:
        #         message = 'you have not given your comment on this Trainee!'
        #         messages.error(request, message)
        #         return redirect('manager:manager_dashboard')
        #     else:
        #         form = ManagerGradingForm(request.POST)
        #         if form.is_valid():
        #             grading_form = form.save(commit=False)
        #             sent_for_approval.gt_score = grading_form.gt_score
        #             sent_for_approval.sent_for_approval = True
        #             sent_for_approval.save()
        #             send_for_approval(sent_for_approval)

        #             message = "Trainee graded successfully And sent for approval."
        #             send_for_approval(sent_for_approval)
        #             messages.success(request, message)
        #             return redirect('manager:manager_dashboard')
        #         else:
        #             messages.error(request, form.errors)
        #             return redirect('manager:manager_dashboard')
        # else:
        #     form = ManagerGradingForm()

        return render(request, self.template) #this return statement shpuld be changed to the one below

        # return render(request, self.template, {'form': form})


# @manager_role_check
def add_manager(request):
    template = "manager/check.html"
    context = {}
    return render(request, template, context)


def manager_edit(request, id):
    pass


def delete_manager(request, id):
    pass


class ManagerTraineeListView(ManagerRoleRequiredMixin, View):
    trainee_dashboard_template = "manager/manager_trainee_list.html"
    def get(self, request):
        department_manager = list(DepartmentManager.objects.filter(manager = request.user).values_list('department__department_name', flat=True))
        # print(request.user.hod_departmenthod.first().department.id)
        trainees = DepartmentTrainee.objects.filter(department__department_name__in = department_manager )
        # departments = Department.objects.filter(id = request.user.manager_departmentmanagers.first().department.id).first()
        # managers = User.objects.filter(role='manager')
        # hods = User.objects.filter(role='hod')
        context = {
            "trainees": trainees,
            # "departments": departments,
            # "managers": managers,
            # "hods": hods
        }
        return render(request, self.trainee_dashboard_template, context)
   