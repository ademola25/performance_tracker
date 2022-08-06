from django.contrib import admin
from .models import Department, DepartmentKeyObjective,DepartmentTrainee, DepartmentManager, DepartmentHod


admin.site.register(Department)
admin.site.register(DepartmentKeyObjective)


admin.site.register(DepartmentTrainee)
admin.site.register(DepartmentManager)
admin.site.register(DepartmentHod)






