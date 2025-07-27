from django.contrib import admin

from appointments.models import Appointment, DayOff


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'client',
        'employee',
        'service',
        'date'
    ]
    list_filter = [
        'client',
        'employee',
    ]
    ordering = ['-date',]


@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'date',
    ]
    list_filter = [
        'employee',
        'date'
    ]
    ordering = ['-date',]
