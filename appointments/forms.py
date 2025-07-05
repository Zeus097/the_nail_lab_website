from django import forms
from datetime import datetime, timedelta, time, date
from django.core.exceptions import ValidationError
from appointments.models import Appointment, DayOff


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'start_time', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'style': 'background-color:white'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        start_time = cleaned_data.get('start_time')
        date_value = cleaned_data.get('date')
        employee = self.employee

        if not all([service, start_time, date_value, employee]):
            return

        if date_value < date.today():
            self.add_error('date', "Не може да запишеш час за минала дата.")
            return

        if DayOff.objects.filter(employee=employee, date=date_value).exists():
            self.add_error('date', "Денят е отбелязан като почивен.")
            return

        start_dt = datetime.combine(date_value, start_time)
        end_dt = start_dt + timedelta(minutes=service.duration)
        end_time = end_dt.time()

        working_start = time(9, 0)
        working_end = time(18, 0)

        if start_time < working_start or end_time > working_end:
            self.add_error('start_time', "Процедурата трябва да е в рамките на работното време (09:00 - 18:00).")
            return

        overlapping = Appointment.objects.filter(employee=employee, date=date_value)
        if self.instance.pk:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        for appt in overlapping:
            other_start = datetime.combine(appt.date, appt.start_time)
            other_end = datetime.combine(appt.date, appt.end_time)

            if not (end_dt <= other_start or start_dt >= other_end):
                self.add_error('start_time', "Часът се припокрива с друга процедура.")
                return


class DayOffForm(forms.ModelForm):
    class Meta:
        model = DayOff
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date_value = cleaned_data.get("date")

        if date_value and DayOff.objects.filter(employee=self.employee, date=date_value).exists():
            self.add_error('date', "Вече има отбелязан почивен ден за тази дата.")
            return

        self.instance.employee = self.employee
        self.instance.date = date_value

        try:
            self.instance.clean()
        except ValidationError as e:
            for field, messages in e.message_dict.items():
                for msg in messages:
                    self.add_error(field, msg)