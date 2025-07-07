from django.db import models

from appointments.validators import AppointmentModelCleanValidator
from services.models import BaseService
from accounts.models import EmployeeBio, ClientProfile
from datetime import datetime, timedelta, time, date
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeBio, on_delete=models.CASCADE)
    service = models.ForeignKey(BaseService, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Записване на час"
        verbose_name_plural = "Записване на часове"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            raise ValueError("Записът на час задължително трябва да има служител.")
        super().save(*args, **kwargs)

    @property
    def end_time(self):
        if not self.date or not self.start_time or not self.service:
            return None
        start_dt = datetime.combine(self.date, self.start_time)
        return (start_dt + timedelta(minutes=self.service.duration)).time()

    def clean(self):
        validator = AppointmentModelCleanValidator()
        validator(self)

    def __str__(self):
        return f"{self.client} - {self.date} - {self.start_time} - {self.service}"


class DayOff(models.Model):
    employee = models.ForeignKey(EmployeeBio, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ["employee", "date"]

    def clean(self):
        if not self.employee or not self.date:
            return

        if Appointment.objects.filter(employee=self.employee, date=self.date).exists():
            raise ValidationError({"date": "Не може да отбележиш ден като почивен, защото има записани клиенти."})

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"
