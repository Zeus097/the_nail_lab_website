from django import forms
from django.core.exceptions import ValidationError
from accounts.models import EmployeeBio
from appointments.models import Appointment, DayOff


class AppointmentForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=EmployeeBio.objects.all(),
        required=True,
        label="Избери служител"
    )

    class Meta:
        model = Appointment
        fields = ['employee', 'service', 'date', 'start_time', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)

        if service:
            self.fields['employee'].queryset = EmployeeBio.objects.filter(services=service)

    def clean(self):
        return super().clean()


# ----------------------------------------
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
