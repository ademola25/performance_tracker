
from django.views import View
from datetime import datetime, date
from comments.models import ManagersComment, TraineeScore
from common.custom_mixins.mixins import HodRoleRequiredMixin, ManagerRoleRequiredMixin
from department.models import Department, DepartmentHod, DepartmentManager, DepartmentTrainee
from accounts.models import User

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from common.decorators.function_role_check import hod_role_and_auth_check
from django.contrib.auth.mixins import LoginRequiredMixin

from gt_logs.models import GtLog
from hod.forms import HodCommentForm
import numbers_of_days
from numbers_of_days.models import NumbersOfDays

# from common.custom_mixins.mixins import HodRoleRequiredMixin, ManagerRoleRequiredMixin, HrRoleRequiredMixin, TraineeRoleRequiredMixin

class HodDashboardView(HodRoleRequiredMixin, View):

    hod_dashboard_template = "hod/dashboard.html"

    # @hod_role_and_auth_check
    def get(self, request):
        today = date.today()
        todays_date = today.strftime("%B %d, %Y")
        hod = request.user
        department = DepartmentHod.objects.filter(hod=hod).first()
 

        try:
            trainees = DepartmentTrainee.objects.filter(department = department.department).count()
            trainees_awaiting_hod = NumbersOfDays.objects.filter(department= department.department.id, numbers_of_days = 'sent_for_hods_approval').count()
            trainees_pending_all = NumbersOfDays.objects.filter(department= department.department.id, numbers_of_days = 'pending_all_approvals').count()
            trainees_approved = NumbersOfDays.objects.filter(department= department.department.id,numbers_of_days = 'approved_by_hod' ).count()

            trainees_awaiting_manager = NumbersOfDays.objects.filter(department= department.department.id,numbers_of_days = 'sent_for_managers_approval' ).count()
            trainees_disapproved = NumbersOfDays.objects.filter(department= department.department.id,numbers_of_days = 'disapproved_by_hod' ).count()
           
            
            context = {
            'hod':hod,
            'department':department,
            'trainees':trainees,
            'trainees_count':trainees,
            'trainees_awaiting_hod':trainees_awaiting_hod,
            'trainees_pending_all':trainees_pending_all,
            'trainees_approved':trainees_approved,
            'trainees_awaiting_manager':trainees_awaiting_manager,
            'trainees_disapproved':trainees_disapproved,
            'error':''

            }
        except Exception as e:
            if department is None:
                error = 'You have not been assigned to a department on this plartform. contact admin.'
            else:
                error = 'something went wrong please contact admin'
        
            trainees = []

            context = {
                'hod':hod,
                'department':department,
                'trainees':0,
                'trainees_count':0,
                'trainees_awaiting_hod':0,
                'trainees_pending_all':0,
                'trainees_awaiting_manager':0,
                "trainees_approved":0,
                'trainees_disapproved':0,
                "error":error,
                }
        return render(request, self.hod_dashboard_template, context)


def add_hod(request):
    pass


def hod_edit(request, id):
    pass


def delete_hod(request, id):
    pass


class ManagerDashboardView(ManagerRoleRequiredMixin, View):
    # @manager_role_and_auth_check
    def get(self, request):
        manager = request.user
        department = Department.objects.filter(manager=manager).first()
        try:
            trainees = department.trainees.all()
        except Exception as e:
            trainees = []

        context = {
            'manager': manager,
            'department': department,
            'trainees': trainees
        }
        return render(request, self.manager_dashboard_template, context)


class HodTraineeLogsView (HodRoleRequiredMixin, View):
    template = "hod/hod_trainee_log.html"
    def get(self, request, trainee_id, manager_id, department_id):

        trainee = get_object_or_404(User, id=trainee_id)
        number_of_days = NumbersOfDays.objects.filter(department = department_id, trainee = trainee_id).first()
        gt_logs = GtLog.objects.filter(trainee = trainee_id)
        form = HodCommentForm()
        context = {
                    "trainee_id":trainee_id,
                    "manager_id":manager_id,
                    "department_id":department_id,
                    'trainee':trainee,
                    "number_of_days":number_of_days,
                    'gt_logs':gt_logs,   
                    'form':form        
                }


       
        return render(request, self.template , context)


    def post(self, request, trainee_id, manager_id, department_id):

        manager = User.objects.filter(id=manager_id).first()
        form = HodCommentForm(request.POST)
        if form.is_valid():

            number_of_days = NumbersOfDays.objects.filter(trainee = trainee_id, department = department_id).first()

            comment_form = form.save(commit=False)
            comment_form.hod = request.user
            comment_form.managers_comment = manager
            comment_form.save()
            number_of_days.hods_overall_comment = comment_form.comment
            number_of_days.hods_overall_score = comment_form.hod_gt_score
            if "approve" in request.POST:
                number_of_days.numbers_of_days = "approved_by_hod"
                number_of_days.save()
                message = f"{number_of_days.trainee.name} has been Approved."
                messages.success(request, message)
                return redirect('hod_dashboard:hod_trainee_logs', manager_id, trainee_id, department_id)
            else:
                number_of_days.numbers_of_days = "disapproved_by_hod"
                number_of_days.save()
                message = f"{number_of_days.trainee.name} has been Disapproved."
                messages.warning(request, message)
                return redirect('hod_dashboard:hod_trainee_logs', manager_id, trainee_id, department_id)     
        else:
            messages.error(request, form.errors)
            return redirect('hod_dashboard:hod_trainee_logs', manager_id, trainee_id, department_id)


class TraineesAwaitingApprovalView (HodRoleRequiredMixin, View):
    template = "hod/trainees_awaiting_approval.html"

    @hod_role_and_auth_check
    def get(self, request):
        error = False
        try:
            department = DepartmentHod.objects.filter(hod = request.user).first()
            managers_coments = NumbersOfDays.objects.filter(department= department.department.id, numbers_of_days="sent_for_hods_approval")
            context = {"managers_coments":managers_coments, 'error':error}

        except Exception as e:
            # print(e)
            error = True
            message = 'You are not assigned to a department please contact admin'
            managers_coments = []
            context = {"managers_coments": managers_coments,
                       'error': error, 'message': message}

        return render(request, self.template, context)


class HodTraineeDashboardView (HodRoleRequiredMixin, View):
    template = "hod/hod_trainee_details.html"

    @hod_role_and_auth_check
    def get(self, request, trainee_id, manager_id, department_id):
        trainee = get_object_or_404(User, id=trainee_id)
        number_of_days = NumbersOfDays.objects.filter(department = department_id, trainee = trainee_id).first()
        gt_logs = GtLog.objects.filter(number_of_days = number_of_days)

        context = {
                    "trainee_id":trainee_id,
                    "manager_id":manager_id,
                    "department_id":department_id,
                    'trainee':trainee,
                    "number_of_days":number_of_days,
                    'gt_logs':gt_logs,               
                }

        return render(request, self.template, context)


class HodTraineeListView(HodRoleRequiredMixin, View):
    trainee_dashboard_template = "hod/hod_trainee_list.html"

    def get(self, request):
        # print(request.user.hod_departmenthod.first().department.id)
        trainees = DepartmentTrainee.objects.filter(department = request.user.hod_departmenthod.first().department.id )
        departments = Department.objects.filter(id = request.user.hod_departmenthod.first().department.id).first()
        # managers = User.objects.filter(role='manager')
        # hods = User.objects.filter(role='hod')
        context = {
            "trainees": trainees,
            # "departments": departments,
            # "managers": managers,
            # "hods": hods
        }
        return render(request, self.trainee_dashboard_template, context)





class HodTraineeDetailsView (LoginRequiredMixin, View):
    trainee_details_template = "hod/trainee_details.html"

    def get(self, request, trainee_id):
        trainee = get_object_or_404(User, id=trainee_id)
        #department = Department.objects.filter(trainees=trainee_id).first()
        number_of_days = NumbersOfDays.objects.filter(trainee=trainee_id)
        context = {
                    'trainee':trainee,
                    "number_of_days":number_of_days,
                }
        if number_of_days is not None:
            
            return render(request, self.trainee_details_template, context)


class HodTraineeDetailLogsView (LoginRequiredMixin ,View):
    template = "hod/hod_trainee_log_details.html"
    def get(self, request, trainee_id, manager_id, department_id):
        managers_comment = ManagersComment.objects.filter(trainee = trainee_id, manager=manager_id, department=department_id)
        aggregate = TraineeScore.objects.filter(trainee = trainee_id, manager=manager_id).first()
        numbers_of_days = NumbersOfDays.objects.filter(trainee = trainee_id, department=department_id).first()

        dept = get_object_or_404(DepartmentManager, department = department_id, manager = manager_id)


        context={
            'trainee_id':trainee_id,
            'managers_comment':managers_comment,
            'aggregate':aggregate,
            'numbers_of_days':numbers_of_days,
            'dept':dept
        }
        
        return render(request, self.template , context)
