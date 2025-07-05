from django.db import models

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

    @property
    def end_time(self):
        if not self.date or not self.start_time or not self.service:
            return None
        start_dt = datetime.combine(self.date, self.start_time)
        return (start_dt + timedelta(minutes=self.service.duration)).time()

    def clean(self):
        if not self.employee_id or not self.service_id or not self.date or not self.start_time:
            return

        if self.date < date.today():
            raise ValidationError("Не може да се записва процедура за минала дата.")

        working_start = time(9, 0)
        working_end = time(18, 0)
        end_time = self.end_time

        if end_time is None:
            return

        if self.start_time < working_start or end_time > working_end:
            raise ValidationError("Процедурата трябва да е в рамките на работното време (09:00 - 18:00).")

        overlapping = Appointment.objects.filter(employee=self.employee, date=self.date).exclude(pk=self.pk)

        appointment_start = datetime.combine(self.date, self.start_time)
        appointment_end = datetime.combine(self.date, end_time)

        for appointment in overlapping:
            other_start = datetime.combine(appointment.date, appointment.start_time)
            other_end = datetime.combine(appointment.date, appointment.end_time)
            if not (appointment_end <= other_start or appointment_start >= other_end):
                raise ValidationError("Часът се припокрива с друга процедура.")

        if DayOff.objects.filter(employee=self.employee, date=self.date).exists():
            raise ValidationError("Денят е отбелязан като почивен.")

    def __str__(self):
        return f"{self.client} - {self.date} - {self.start_time} - {self.service}"


class DayOff(models.Model):
    employee = models.ForeignKey(EmployeeBio, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ["employee", "date"]

    def clean(self):
        if not self.employee_id or not self.date:
            return

        if Appointment.objects.filter(employee=self.employee, date=self.date).exists():
            raise ValidationError({"date": "Не може да отбележиш ден като почивен, защото има записани клиенти."})

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"
