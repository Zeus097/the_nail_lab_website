from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import BaseUser, EmployeeBio,ClientProfile


@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    model = BaseUser
    list_display = ('username', 'email', 'is_client', 'is_employee', 'is_staff', 'is_superuser')
    list_filter = ('is_client', 'is_employee', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Ролева информация', {
            'fields': ('is_client', 'is_employee',)
        }),
    )

@admin.register(EmployeeBio)
class EmployeeBioAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user__email', 'phone',]

