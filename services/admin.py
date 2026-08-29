from django.contrib import admin
from services.models import BaseService

# Register your models here.


@admin.register(BaseService)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'description',
        'euro_price',
        'leva_price',
        'duration',
        'is_active',
    ]

    list_editable = [
        'category',
        'is_active',
    ]

    list_filter = [
        'category',
        'is_active',
    ]

    search_fields = [
        'name',
    ]

