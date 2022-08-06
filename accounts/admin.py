from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import TOTPDevice, User, UserTOTPDevice, Workforce
from .forms import UserAdminRegisterForm, UserAdminUpdateForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserAdminUpdateForm
    add_form = UserAdminRegisterForm

    list_display = ('email', 'admin')
    list_filter = ('admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'staff_id', 'role', 'batch','workforce', )}),
        ('Permissions', {'fields': ('admin', 'staff')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'name', 'staff_id', 'admin', 'staff', 'password', 'password2', 'batch')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Workforce)
admin.site.register(TOTPDevice)
admin.site.register(UserTOTPDevice)


