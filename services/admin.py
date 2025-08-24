from django.contrib import admin
from services.models import BaseService

# Register your models here.


@admin.register(BaseService)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'max_price', 'duration', 'is_active',]
    list_editable = ['is_active',]
    list_filter = ['is_active',]
    search_fields = ['name',]
