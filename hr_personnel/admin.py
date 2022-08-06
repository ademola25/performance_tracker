from django.contrib import admin

from .models import HrPersonnel, Batch, HodCreationError


admin.site.register(HrPersonnel)
admin.site.register(Batch)
admin.site.register(HodCreationError)


