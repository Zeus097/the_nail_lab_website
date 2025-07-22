from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import BaseUser, EmployeeBio,ClientProfile


@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    model = BaseUser

    list_display = [
        'username',
        'email',
        'telephone_number',
        'is_client',
        'is_employee',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login'
    ]
    list_filter = [
        'is_client',
        'is_employee',
    ]
    search_fields = [
        'username',
        'email'
    ]
    ordering = [
        '-date_joined',
    ]


    # Choose the profile role
    fieldsets = UserAdmin.fieldsets + (
        ('Ролева информация', {
            'fields': ('is_client', 'is_employee',)
        }),
    )


@admin.register(EmployeeBio)
class EmployeeBioAdmin(admin.ModelAdmin):
    model = EmployeeBio

    list_display = [
        'name',
        'user_email',
    ]
    filter_horizontal = ['services']
    # Allow to add services through Admin Panel

    # In order to show user_email, because is BaseUserAdmin attribute
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Имейл'


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    model = ClientProfile

    list_display = [
        'name',
        'user_email',
    ]

    # In order to show user_email, because is BaseUserAdmin attribute
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Имейл'


