from django import forms
from appointments.models import Appointment
from datetime import time


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'start_time']

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if not time(9, 0) <= start_time <= time(17, 59):
            raise forms.ValidationError("Часът трябва да е между 09:00 и 18:00.")
        return start_time

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.employee = self.employee
        if commit:
            appointment.save()
        return appointment
