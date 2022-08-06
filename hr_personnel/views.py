from django.utils.timezone import localtime
import csv

from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse
from django.views import View
from common.custom_mixins.mixins import HrRoleRequiredMixin
from department.models import Department, DepartmentHod, DepartmentKeyObjective, DepartmentManager, DepartmentTrainee
from accounts.models import User
from hod.models import Hod
from hr_personnel.Save_to_db import GrabAndSaveToDb
from hr_personnel.models import Batch, HrPersonnel

from manager.models import Manager
from numbers_of_days.models import NumbersOfDays
from .forms import BatchForm, createHodForm, createDepartmentForm, createManagerForm
from django.shortcuts import redirect, render
from .forms import BatchForm, DepartmentEditForm, UserEditForm, createHodForm, createDepartmentForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import csv
import datetime
from django.contrib.auth.decorators import login_required
from numbers_of_days.models import NumbersOfDays
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def department_update_view(request, department_id):
    obj = get_object_or_404(Department, id=department_id)
    template_name = 'hr_personnel/department/department_update.html'
    form = DepartmentEditForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message = f'You have updated {obj.department_name} department'
            messages.success(request, message)
            return redirect('hr_personnel:all_departments')
        else:
            messages.error(request, form.error)
            return redirect('hr_personnel:all_departments')
    else:
        form = DepartmentEditForm(request.POST or None, instance=obj)
    return render(request, template_name, {'form': form, 'department_id': department_id})


class DepartmentUpdateView(UpdateView):
    # specify the model you want to use
    template_name = "hr_personnel/department/department_update.html"

    model = Department
    slug_url_kwarg = 'uuid'
    slug_field = 'id'    # specify the fields
    fields = [
        "department_name",
        "key_objective"
    ]

    success_url = "hr-personnel/all-departments"


class HrPersonnelDashboardView(HrRoleRequiredMixin, View):
    trainee_dashboard_template = "hr_personnel/trainee/dashboard.html"

    def get(self, request):
        form = BatchForm()
        trainees = User.objects.filter(role='trainee')
        departments = Department.objects.all()
        managers = User.objects.filter(role='manager')
        hods = User.objects.filter(role='hod')
        context = {
            "form": form,
            "trainees": trainees,
            "departments": departments,
            "managers": managers,
            "hods": hods
        }
        return render(request, self.trainee_dashboard_template, context)

    def post(self, request):
        if request.method == 'POST':
            if 'upload_trainees' in request.POST:

                form = BatchForm(request.POST, request.FILES)
                context = {'form': form}
                if form.is_valid():

                    uploaded_csv = form.save(commit=False)

                    uploaded_csv.uploaded_by = str(
                        request.user) + ' ' + str(request.user.id) + ' ' + str(request.user.name)
                    uploaded_csv.month_year = uploaded_csv.month_year

                    uploaded_csv.save()
                    grab_save = GrabAndSaveToDb(uploaded_csv)
                    response = grab_save.Check_and_save_hod()

                    if response == 200:

                        message = "Csv file uploaded successfully"
                        messages.success(request, message)
                        return redirect('hr_personnel:all_trainees')
                    else:

                        messages.error(request, response[1])
                        return redirect('hr_personnel:hr_personnel_dashboard')
                else:
                    message = form.errors.as_json()

                    messages.error(request, message)
                    form = BatchForm()
            elif 'existing_template' in request.POST:
                today = datetime.date.today()
                todays_date = today.strftime("%B %d, %Y")
                row_list = ["TRAINEE ID", "TRAINEE NAME", "TRAINEE EMAIL", "MANAGER ID", "MANAGER NAME", "MANAGER EMAIL", "HOD ID", "HOD Name", "HOD Email", "Department", "NUMBER OF DAYS", "Key Objectives", "Year", "MAIN DEPARTMENT"]
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{todays_date} GT template.csv"'
                writer = csv.writer(response)
                writer.writerow(row_list)
                return response

            else:

                start_date = str(request.POST.get("start_date", ""))
                end_date = str(request.POST.get("end_date", ""))

                users = User.objects.filter(
                    role='trainee', is_active=True, batch__month_year__range=[start_date, end_date])
                output = []
                all_data = []
                response = HttpResponse (content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{start_date} till {end_date} GT Report.csv"'
                writer = csv.writer(response)
                writer.writerow([
                'TRAINEE ID',
                'TRAINEE NAME',
                'TRAINEE EMAIL',
                'TRAINEE DEPARTMENT',
                'MAIN DEPARTMENT',
                'NUMBER OF DAYS SPENT',
                'HOD ID',
                'HOD NAME',
                'HOD EMAIL',
                'MANAGER ID',
                'MANAGER NAME',
                'MANAGER EMAIL',
                'MANAGER COMMENT',
                'MANAGER SCORE',
                'HOD comment',
                'HOD Approval',

                ])
                try:
                    for user in users:
                        # print(user)

                        # number_of_days = NumbersOfDays.objects.filter(trainee=user).values_list('trainee__id','trainee__name','trainee__email', 'department__department_name', 'value', 'department__hod__name', 'department__manager__name', 'managers_overall_comment' ,'managers_overall_score', 'hods_overall_comment' ,'hods_overall_score')
                        number_of_days = NumbersOfDays.objects.filter(trainee=user).values_list(
                        'trainee__staff_id',
                        'trainee__name',
                        'trainee__email',
                        'department__department_name',
                         'main_department',
                        'value',
                        'department__department_departmenthod__hod__staff_id',
                        'department__department_departmenthod__hod__name',
                        'department__department_departmenthod__hod__email',

                        'department__department_departmentmanagers__manager__staff_id',
                        'department__department_departmentmanagers__manager__name',
                        'department__department_departmentmanagers__manager__email',


                         'managers_overall_comment',
                         'managers_overall_score',
                         'hods_overall_comment',
                         'numbers_of_days',
                        )
                        
                        all_data.append(number_of_days)
                    for user_data in all_data:


                        for user_details in user_data:
                            # output.append([user_details[0],user_details[1], user_details[2], user_details[3], user_details[4], user_details[5], user_details[6], user_details[7], user_details[8]])
                            output.append([user_details[0],
                                            user_details[1],
                                             user_details[2],
                                             user_details[3],
                                             user_details[4],
                                             user_details[5],
                                             user_details[6],
                                             user_details[7],
                                              user_details[8],
                                              user_details[9],
                                              user_details[10],
                                               user_details[11],
                                              user_details[12],
                                              user_details[13],
                                              user_details[14],
                                              user_details[15],


                                             ])

                    writer.writerows(output)
                    return response
                except Exception as e:
                    messages.error(request, f'Download unsuccessful: {e}')
                    return redirect('hr_personnel:hr_personnel_dashboard')

        else:
            form = BatchForm()

        return render(request, self.trainee_dashboard_template, context)

    def pre_existing_template(self):
        today = datetime.date.today()
        todays_date = today.strftime("%B %d, %Y")
        row_list = ["TRAINEE ID", "TRAINEE NAME", "TRAINEE EMAIL", "MANAGER ID", "MANAGER NAME",
                    "MANAGER EMAIL", "HOD ID", "HOD Name", "HOD Email", "Department", "NUMBER OF DAYS", "Key Objectives"]
        with open(f'{todays_date}.csv', 'w', newline='') as file:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerows(row_list)

            return response


class ManagersListView(HrRoleRequiredMixin, View):
    trainee_dashboard_template = "hr_personnel/manager/managers_list.html"

    def get(self, request):
        departments = Department.objects.all()
        managers = User.objects.filter(role="manager")
        form = createManagerForm()
        context = {
            "managers": managers, "departments": departments, 'form': form
        }

        return render(request, self.trainee_dashboard_template, context)

    def post(self, request):
        if request.method == 'POST':
            form = createManagerForm(request.POST)
            if form.is_valid():
                manager_creation_form = form.save(commit=False)
                manager_creation_form.role = "manager"
                manager_creation_form.save()

                dept = form.cleaned_data['department']
                department = Department.objects.filter(id =dept.id).first()
                DepartmentManager.objects.create(
                    department = department,
                    manager = manager_creation_form
                )
                message = f"{manager_creation_form.name} created as Manager for {dept.department_name} successfully."

                message = "Manager created successfully."
                messages.success(request, message)
                return redirect('hr_personnel:all_managers')
            else:

                messages.error(request, form.errors)
                return redirect('hr_personnel:all_managers')
        else:
            form = createManagerForm()

        return render(request, self.trainee_dashboard_template, {'form': form})
 

class HodsListView(HrRoleRequiredMixin, View):
    trainee_dashboard_template = "hr_personnel/hod/hods_list.html"

    def get(self, request):
        departments = Department.objects.all()
        hods = User.objects.filter(role="hod")
        form = createHodForm()
        context = {
            "departments": departments, "hods": hods, 'form': form,
        }
        return render(request, self.trainee_dashboard_template, context)

    def post(self, request):
        if request.method == 'POST':
            form = createHodForm(request.POST)
            if form.is_valid():
                hod_form = form.save(commit=False)
                hod_form.role = 'hod'
                hod_form.save()
                dept = form.cleaned_data['department']
                department = Department.objects.filter(id =dept.id).first()
                DepartmentHod.objects.create(
                    department = department,
                    hod = hod_form
                )
                message = f"{hod_form.name} created as Hod created for {dept.department_name} successfully."
                messages.success(request, message)
                return redirect('hr_personnel:all_hods')
            else:
                messages.error(request, form.errors)
                return redirect('hr_personnel:all_hods')
        else:
            form = createHodForm()

        return render(request, self.trainee_dashboard_template, {'form': form})


class TraineeListView(HrRoleRequiredMixin, View):
    trainee_dashboard_template = "hr_personnel/trainee/trainee_list.html"

    def get(self, request):
        form = BatchForm()
        trainees = User.objects.filter(role='trainee')

        departments = Department.objects.all()
        managers = User.objects.filter(role='manager')
        hods = User.objects.filter(role='hod')
        context = {
            "form": form,
            "trainees": trainees,
            "departments": departments,
            "managers": managers,
            "hods": hods
        }
        return render(request, self.trainee_dashboard_template, context)

    def post(self, request):
        if request.method == 'POST':
            form = BatchForm(request.POST, request.FILES)
            context = {'form': form}
            if form.is_valid():
                uploaded_csv = form.save(commit=False)
                hr_person = HrPersonnel.objects.all().first()
                uploaded_csv.uploaded_by = hr_person
                uploaded_csv.save()
                grab_save = GrabAndSaveToDb(uploaded_csv)
                response = grab_save.Check_and_save_hod()
                if response == 200:

                    message = "Csv file uploaded successfully"
                    messages.success(request, message)
                    return redirect('hr_personnel:hr_personnel_dashboard')
                else:
                    messages.error(request, response[1])
                    return redirect('hr_personnel:hr_personnel_dashboard')
            else:
                message = form.errors.as_json()

                messages.error(request, message)
                form = BatchForm()
        else:
            form = BatchForm()

        return render(request, self.trainee_dashboard_template, context)


# update view for details

# @login_required
# def department_update_view(request, department_id):
#     context ={}
#     obj = get_object_or_404(Department, id = department_id)
#     template_name = 'comments/managers_edit_comment.html'
#     form = DepartmentEditForm(request.POST or None, instance = obj)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             message = f'You have updated {obj.department_name} department'
#             messages.success(request, message )
#             return redirect('hr_personnel:all_departments')
#         else:
#             messages.error(request, form.error )
#             return redirect('hr_personnel:all_departments')
#     else:
#         form = DepartmentEditForm(request.POST or None, instance = obj)
#     return render(request, template_name, {'form': form, 'department_id':department_id})


# update view for details

@login_required
def user_update_view(request, user_id):
    obj = get_object_or_404(User, id=user_id)
    template_name = 'hr_personnel/user_edit_form.html'
    form = UserEditForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message = f'You have updated {obj.name}'
            messages.success(request, message )
            if obj.role == 'hod':
                return redirect('hr_personnel:all_hods')
            elif obj.role == 'manager':
                return redirect('hr_personnel:all_managers')
            else:
                return redirect('hr_personnel:all_trainees')

        else:
            messages.error(request, form.error)
            return redirect('hr_personnel:all_hods')
    else:
        form = UserEditForm(request.POST or None, instance=obj)
    return render(request, template_name, {'form': form, 'user_id': user_id, 'obj': obj})


@login_required
def delete_view(request, user_id):
    obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        obj.delete()
        message = f'{obj.name} deleted successful.'
        messages.success(request, message)
        return redirect('hr_personnel:all_hods')


@login_required
def manager_delete_view(request, user_id):
    obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        obj.delete()
        message = f'{obj.name} deleted successful.'
        messages.success(request, message)

        return redirect('hr_personnel:all_managers')


@login_required
def trainee_delete_view(request, user_id):
    obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        obj.delete()
        message = f'{obj.name} deleted successful.'
        messages.success(request, message)
        return redirect('hr_personnel:all_hods')


@login_required
def manager_delete_view(request, user_id):
    obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        obj.delete()
        message = f'{obj.name} deleted successful.'
        messages.success(request, message)
        return redirect('hr_personnel:all_managers')


@login_required
def trainee_delete_view(request, user_id):
    obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        obj.delete()
        message = f'{obj.name} deleted successful.'
        messages.success(request, message)
        return redirect('hr_personnel:all_trainees')


class DeleteDepartmentsView(HrRoleRequiredMixin, View):
    def post(self, request, department_id):
        obj = get_object_or_404(Department, id=department_id)
        if request.method == 'POST':
            obj.delete()
            message = f'{obj.department_name} deleted successful.'
            messages.success(request, message)
            return redirect('hr_personnel:all_departments')


class DepartmentsListView(HrRoleRequiredMixin, View):
    trainee_dashboard_template = "hr_personnel/department/departments_list.html"

    def get(self, request):
        departments = Department.objects.all()
        hods = Hod.objects.all()
        managers = Manager.objects.all()
        form = createDepartmentForm()
        context = {
            "departments": departments, "hods": hods, "managers": managers, 'form': form,
        }
        return render(request, self.trainee_dashboard_template, context)

    def post(self, request):
        if request.method == 'POST':
            form = createDepartmentForm(request.POST)
            if form.is_valid():

                create_department_form = form.save(commit=False)
                create_department_form.save()
                splitted_key_objective_array = create_department_form.key_objective.split("\n")
                for i in splitted_key_objective_array:
                    if i != "":
                        p, created = DepartmentKeyObjective.objects.get_or_create(
                            department= create_department_form,
                            key_objective=i,
                        )

                message = "Department created successfully."
                messages.success(request, message)
                return redirect('hr_personnel:all_departments')
            else:
                messages.error(request, form.errors)
                return redirect('hr_personnel:all_departments')
        else:
            form = createDepartmentForm()

        return render(request, self.trainee_dashboard_template, {'form': form})


class TraineeDetailsView (LoginRequiredMixin, View):
    trainee_details_template = "hr_personnel/trainee/trainee_details.html"

    def get(self, request, trainee_id):
        trainee = get_object_or_404(User, id=trainee_id)
        number_of_days = NumbersOfDays.objects.filter(trainee = trainee_id)
        context = {
            'trainee': trainee,
            "number_of_days": number_of_days

        }
        # if number_of_days is not None:

        return render(request, self.trainee_details_template, context)