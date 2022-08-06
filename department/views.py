from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.views import View

from django.shortcuts import redirect, render


def add_department(request):
    return redirect("common:dashboard_view")


def department_edit(request, id):
    return redirect("common:dashboard_view")


def delete_department(request, id):
    return redirect("common:dashboard_view")
