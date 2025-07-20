from django.db import models
from django.utils.timezone import now

from appointments.validators import AppointmentModelCleanValidator
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    client = models.ForeignKey('accounts.ClientProfile', on_delete=models.CASCADE)
    employee = models.ForeignKey('accounts.EmployeeBio', on_delete=models.CASCADE)
    service = models.ForeignKey('services.BaseService', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    comment = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Записване на час"
        verbose_name_plural = "Записване на часове"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            raise ValueError("Записът на час задължително трябва да има служител.")
        if not self.service_id:
            raise ValueError("Записът на час задължително трябва да има услуга.")
        super().save(*args, **kwargs)



    @property
    def end_time(self):
        if not self.date or not self.start_time or not self.service:
            return None
        start_dt = datetime.combine(self.date, self.start_time)
        return (start_dt + timedelta(minutes=self.service.duration)).time()

    def clean(self):
        if not self.service_id or not self.employee_id or not self.date or not self.start_time:
            return

        validator = AppointmentModelCleanValidator()
        validator(self)

    def __str__(self):
        return f"{self.client} - {self.date} - {self.start_time} - {self.service}"


# --------------------------------
class DayOff(models.Model):
    class Meta:
        verbose_name = "Почивен ден"
        verbose_name_plural = "Почивни дни"


    employee = models.ForeignKey('accounts.EmployeeBio', on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ["employee", "date"]

    def clean(self):
        if not self.employee or not self.date:
            return

        if self.date < now().date():
            raise ValidationError({"date": "Не може да отбележиш ден като почивен в миналото."})

        if Appointment.objects.filter(employee=self.employee, date=self.date).exists():
            raise ValidationError({"date": "Не може да отбележиш ден като почивен, защото има записани клиенти."})

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"
