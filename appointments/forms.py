from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from appointments.models import Appointment, DayOff


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'start_time', 'comment']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'YYYY-MM-DD',
                    'style': 'background-color:white'
                }
            ),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # Не викай instance.full_clean() тук
        # Просто сетвай instance.employee, за да го ползва clean() на модела
        self.instance.employee = self.employee
        return cleaned_data



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
        date_value = cleaned_data.get('date')

        if not date_value:
            self.add_error('date', "Моля, въведете валидна дата.")
            return cleaned_data

        self.instance.employee = self.employee
        self.instance.date = date_value

        try:
            self.instance.full_clean()
        except ValidationError as e:

            for field, messages in e.message_dict.items():
                for msg in messages:
                    self.add_error(field, msg)

        return cleaned_data