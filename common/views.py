import email
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 


from accounts.models import User


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def handler403(request, exception):
    return render(request, '403.html', status=200)


def handler429(request, exception=None):
    return render(request, '429.html', status=429)

class DashboardView(LoginRequiredMixin , View):
    def get(self, request,**kwargs):
        print("olololol")
        if request.user.role=='trainee':
            return redirect('trainee:trainee_dashboard')
        elif request.user.role == 'hr':
            return redirect('hr_personnel:hr_personnel_dashboard')
        elif request.user.role=='manager':
            return redirect('manager:manager_dashboard')
        elif request.user.role=='hod':
            return redirect('hod_dashboard:hod_dashboard')
        else:
           pass



def search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        trainee = User.objects.filter(name__istartswith=search_str, email__istartswith=search_str) | User.objects.filter(role___istartswith=search_str, staff_id__istartswith=search_str) 
    data = trainee.values()
    return JsonResponse(list(data), safe=False)


