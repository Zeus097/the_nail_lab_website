from django.contrib import admin
from services.models import BaseService

# Register your models here.

@admin.register(BaseService)
class ServiceAdmin(admin.ModelAdmin):
    pass
