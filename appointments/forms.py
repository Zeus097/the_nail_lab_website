from django import forms
from accounts.models import EmployeeBio
from appointments.models import Appointment, DayOff


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['employee', 'service', 'date', 'start_time', 'comment']
        labels = {
            'service': 'Услуги',
            'date': 'Дата',
            'start_time': 'Начален час',
            'comment': 'Коментар (по избор)'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'comment': forms.Textarea(attrs={
                'rows': 10, 'cols': 40, 'maxlength': 200,
                'placeholder': 'Максимален брой символи - 200',
                'style': 'padding: 10px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)

        if service:
            self.fields['service'].initial = service
            self.fields['employee'].queryset = EmployeeBio.objects.filter(services=service)
        else:
            self.fields['employee'].queryset = EmployeeBio.objects.all()

    employee = forms.ModelChoiceField(
        queryset=EmployeeBio.objects.all(),
        required=True,
        label= 'Избери служител'
    )

    def clean(self):
        return super().clean()


class AppointmentCreateForm(AppointmentForm):
    pass


class AppointmentEditForm(AppointmentForm):
    pass


# ----------------------------------------
class DayOffForm(forms.ModelForm):
    class Meta:
        model = DayOff
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'date': 'Дата'
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

        return cleaned_data


class DayOffCreateForm(DayOffForm):
    pass


class DayOffEditForm(DayOffForm):
    pass
