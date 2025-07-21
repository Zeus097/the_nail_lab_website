from django.contrib import admin
from services.models import BaseService

# Register your models here.


@admin.register(BaseService)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'duration']
    list_filter = ['name', 'price', 'duration']
    search_fields = ['name', 'price', 'duration']
