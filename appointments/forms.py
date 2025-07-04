from django import forms
from datetime import datetime, timedelta, time
from django.core.exceptions import ValidationError
from appointments.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)  # подаваш от view
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        start_time = cleaned_data.get('start_time')
        date = cleaned_data.get('date')
        employee = self.employee

        if not all([service, start_time, date, employee]):
            return  # Ако няма някое от полетата, пропускаме за сега

        # Изчисляваме крайно време
        end_time = (datetime.combine(date, start_time) + timedelta(minutes=service.duration)).time()

        # Проверка за работно време
        if start_time < time(9, 0) or end_time > time(18, 0):
            raise ValidationError("Процедурата трябва да е в рамките на работното време (09:00 - 18:00).")

        # Проверка за припокриване с други часове на същия служител
        overlapping = Appointment.objects.filter(
            employee=employee,
            date=date,
        )
        # Ако това е редакция (update), изключваме текущия запис, ако има pk
        if self.instance.pk:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        this_start = datetime.combine(date, start_time)
        this_end = datetime.combine(date, end_time)

        for appt in overlapping:
            other_start = datetime.combine(appt.date, appt.start_time)
            other_end = datetime.combine(appt.date, appt.end_time)
            if not (this_end <= other_start or this_start >= other_end):
                raise ValidationError("Часът се припокрива с друга процедура.")
