from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import UpdateView
from pip import main
from comments.forms import ManagerGradingForm, ManagersCommentForm, ManagersCommentTrailForm, NumbersOfDaysForm

from comments.models import ManagersComment, CommentTrail, TraineeScore
from common.decorators.function_role_check import manager_role_and_auth_check
from common.utils import sent_for_hod_approval
from department.models import Department
from gt_logs.models import GtLog
from manager.models import Manager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from numbers_of_days.models import NumbersOfDays
from accounts.models import User
from django.contrib.auth.decorators import login_required
from common.task import manager_to_hod_notification



def comment_trail(comment, trainee, manager):
    CommentTrail.objects.create(comment = comment, trainee = trainee, manager = manager)
    return True




class ManagersCommentTrailView(LoginRequiredMixin, View):
    managers_comment_trail_template = "comments/managers_create_comment_trail.html"

    def get(self, request, trainee_id):
        # managers_department = Department.objects.filter(
        #     manager=request.user).first()
        # number_of_days = NumbersOfDays.objects.filter(
        #     trainee=trainee_id, department=managers_department).first()
        # gt_logs = GtLog.objects.filter(number_of_days=number_of_days)
        # form = ManagersCommentTrailForm()
        # context = {'form': form, 'trainee_id': trainee_id, 'number_of_days': number_of_days, "gt_logs": gt_logs}
        context ={}
        return render(request, self.managers_comment_trail_template, context)

    def post(self, request, trainee_id):
        if request.method == 'POST':
            form = ManagersCommentTrailForm(request.POST)
            if form.is_valid():

                trainee = User.objects.filter(id=trainee_id).first()
                manager = request.user
                comment_form = form.save(commit=False)
                comment_form.manager = manager
                comment_form.trainee = trainee
                comment_form.save()
                
                message = f'You have commented on Trainee\'s Log'
                messages.success(request, message)
                return redirect('manager:trainee_logs', id=trainee_id)
            else:
                messages.error(request, form.errors)
                return redirect('manager:create_comment', id=trainee_id)


# Create your views here.
class ManagersCommentView(LoginRequiredMixin, View):
    managers_comment_template = "comments/managers_create_comment.html"
    # login_url = '/'
    # redirect_field_name = 'managers_comment:create_comment'

    def get(self, request, trainee_id, department_id):
    
        number_of_days = NumbersOfDays.objects.filter(trainee = trainee_id, department = department_id).first()
        gt_logs = GtLog.objects.filter(number_of_days=number_of_days)
        gt_logs_count = gt_logs.count()
        if gt_logs_count >= number_of_days.value:
            trainee_log_complete = True
        else:
            trainee_log_complete = False

        today = datetime.today()
        todays_comment = ManagersComment.objects.filter(created_at__year=today.year, created_at__month=today.month,created_at__day=today.day, trainee = trainee_id, department = department_id)

        if todays_comment:
            already_created = True
        else:
            already_created = False


        form = ManagerGradingForm()
        context = {'form': form, 'trainee_id': trainee_id,'department_id':department_id,
                   'number_of_days': number_of_days, "gt_logs": gt_logs, 'already_created':already_created, 'trainee_log_complete':trainee_log_complete}
        # context = {}
        return render(request, self.managers_comment_template, context)


    def post(self, request, trainee_id, department_id):
        if request.method == 'POST':
            form = ManagerGradingForm(request.POST)
            if form.is_valid():
                trainee = User.objects.filter(id=trainee_id).first()
                manager_grading_form = form.save(commit=False)
                manager_grading_form.trainee = trainee
                manager_grading_form.manager = request.user
                manager_grading_form.department = Department.objects.filter(id = department_id).first()

                

                manager_grading_form.save()
                manager_comment_count =  ManagersComment.objects.filter(
                trainee = trainee,
                manager = request.user,
                department = Department.objects.filter(id = department_id).first()
                ).count()

                my_scoreboard = TraineeScore.objects.filter(
                   trainee = trainee,
                    department = department_id,
                ).first()
                main_hod = NumbersOfDays.objects.filter(trainee = trainee_id, main_department = True).first()
                if main_hod is not None:
                    hod_name = main_hod.department.department_departmenthod.last().hod.name
                    hod_email = main_hod.department.department_departmenthod.last().hod.email
                else:
                    highest_count_hod = NumbersOfDays.objects.filter(trainee = trainee_id).order_by('-value').first()
                    hod_name = highest_count_hod.department.department_departmenthod.last().hod.name

                    hod_email = highest_count_hod.department.department_departmenthod.last().hod.email

                if my_scoreboard:
                    #edit
                    my_scoreboard.number_comments = manager_comment_count + 1
                    my_scoreboard.aggregate_score = my_scoreboard.aggregate_score + manager_grading_form.gt_score*10
                    # my_scoreboard.save(commit=False)
                    my_scoreboard.attainable_score = my_scoreboard.attainable_score +100 #manager_comment_count * 100
                    my_scoreboard.save()
                    number_of_days = NumbersOfDays.objects.filter(trainee = trainee_id, department = department_id).first()
                    gt_logs = GtLog.objects.filter(number_of_days=number_of_days).count()


                    

                    

                    if gt_logs >= number_of_days.value:

                        number_of_days.numbers_of_days='sent_for_hods_approval'
                        number_of_days.managers_overall_comment = manager_grading_form.comment
                        number_of_days.managers_overall_score = my_scoreboard.aggregate_score
                        number_of_days.save()


                        manager_to_hod_notification.delay(
                        manager_grading_form.id,

                        
                        hod_name,
                        hod_email,

                        number_of_days.trainee.name,

                        request.user.name,
                        request.user.email,

                        number_of_days.trainee.id)

                        message = f'You have graded Trainee. Awaiting approval'
                        messages.success(request, message)
                        return redirect('manager:trainee_logs', id=trainee_id, department_id = department_id)
   
                else:

                    trainee_score =  TraineeScore.objects.create(
                    trainee = trainee,
                    manager = request.user,
                    number_comments = manager_comment_count,
                    aggregate_score = manager_grading_form.gt_score*10,
                    attainable_score = manager_comment_count *100,
                    department = Department.objects.filter(id = department_id).first()
                    )
                    number_of_days = NumbersOfDays.objects.filter(trainee = trainee_id, department = Department.objects.filter(id = department_id).first()).first()
                    gt_logs = GtLog.objects.filter(number_of_days=number_of_days).count()
                    if gt_logs >= number_of_days.value:
                        number_of_days.numbers_of_days='sent_for_hods_approval'
                        number_of_days.managers_overall_comment = manager_grading_form.comment
                        number_of_days.managers_overall_score = trainee_score.aggregate_score
                        number_of_days.save()

                        manager_to_hod_notification.delay(
                            manager_grading_form.id,
                            hod_name,
                            hod_email,
                            number_of_days.trainee.name,

                            request.user.name,
                            request.user.email,

                            number_of_days.trainee.id)

                        message = f'You have graded Trainee. Awaiting approval'
                        messages.success(request, message)
                        return redirect('manager:trainee_logs', id=trainee_id, department_id = department_id)


                messages.success(request, 'you have saved comments for this user')
                return redirect('manager:trainee_logs', id=trainee_id, department_id = department_id)
            else:
                messages.error(request, form.errors)
                return redirect('managers_comment:create_comment', trainee_id=trainee_id, department_id = department_id)

class ManagersCommentUpdateView(LoginRequiredMixin, View):
    template_name = 'comments/managers_edit_comment.html'

    def get(self, request, comment_id):
        # obj = get_object_or_404(ManagersComment, id=comment_id)
        # trainee_id = obj.trainee.id
        # trainee_log_count = GtLog.objects.filter(trainee=trainee_id).count()
        # managers_department = Department.objects.filter(
        #     manager=request.user).first()
        # number_of_days = NumbersOfDays.objects.filter(
        #     trainee=trainee_id, department=managers_department).first()
        # gt_logs = GtLog.objects.filter(number_of_days=number_of_days)
        # form = ManagersCommentForm(request.POST or None, instance=obj)
        # grading_form = ManagerGradingForm(request.POST or None, instance=obj)
        # context = {'gt_logs': gt_logs, 'managers_comment': obj, 'form': form, 'grading_form': grading_form, 'trainee_id': trainee_id,
        #            'comment_id': comment_id, 'trainee_log_count': trainee_log_count, "number_of_days": number_of_days, }
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, comment_id):
        # obj = get_object_or_404(ManagersComment, id=comment_id)
        # trainee_id = obj.trainee.id
        # if request.method == "POST":
        #     number_of_days = NumbersOfDays.objects.filter(
        #         trainee=trainee_id).first()
        #     gt_logs = GtLog.objects.filter(number_of_days=number_of_days)

        #     if 'temporarily' in request.POST:
        #         form = ManagersCommentForm(request.POST or None, instance=obj)
        #         if form.is_valid():
        #             form.save()
        #             comment_trail(form.cleaned_data['comment'], number_of_days.trainee , request.user)
        #             message = f'You have updated your commented on Trainee\'s Log'
        #             messages.success(request, message)
        #             return redirect('manager:trainee_logs', trainee_id)
        #         else:
        #             messages.error(request, form.error)
        #             return redirect('managers_comment:edit_comment', trainee_id)
        #     else:
        #         form = ManagersCommentForm(request.POST or None, instance=obj)
        #         grading_form = ManagerGradingForm(
        #             request.POST or None, instance=obj)
        #         number_of_days = NumbersOfDays.objects.filter(
        #             trainee=trainee_id).first()
        #         gt_logs = GtLog.objects.filter(number_of_days=number_of_days)
        #         if form.is_valid() and grading_form.is_valid():
        #             trainee = User.objects.filter(id=trainee_id).first()
        #             manager = request.user
        #             comment_form = form.save(commit=False)
        #             comment_form.manager = manager

        #             comment_form.trainee = trainee
        #             comment_form.sent_for_approval = True
        #             comment_trail(comment_form.comment, comment_form.trainee, comment_form.manager)
        #             manager_grading_form = grading_form.save(commit=False)

        #             comment_form.gt_score = manager_grading_form.gt_score

        #             if gt_logs.count() == number_of_days.value:
        #                 number_of_days.managers_overall_comment = comment_form.comment
        #                 number_of_days.managers_overall_score = manager_grading_form.gt_score
        #                 number_of_days.save()
        #             comment_form.save()
        #             message = f'You have graded Trainee. Awaiting approval'
        #             messages.success(request, message)
        #             return redirect('manager:trainee_logs', id=trainee_id)
        #         else:
        #             messages.error(
        #                 request, f'{form.error} {grading_form.error}')
                    # return redirect('managers_comment:edit_comment', trainee_id)
                    # the above return statement is the real rtuern statment delete this one below 
                    return redirect('managers_comment:edit_comment')
