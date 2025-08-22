from django import forms
from accounts.models import EmployeeBio
from appointments.models import Appointment, DayOff
from services.models import BaseService


class AppointmentForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=EmployeeBio.objects.all(),
        required=True,
        label='Избери служител'
    )

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
        employee_id = kwargs.pop('employee_id', None)
        super().__init__(*args, **kwargs)

        if not employee_id:
            if self.instance and self.instance.employee_id:
                employee_id = self.instance.employee_id
            elif self.data.get('employee'):
                employee_id = self.data.get('employee')
            elif self.initial.get('employee'):
                employee_id = self.initial.get('employee')

        if employee_id:
            try:
                employee = EmployeeBio.objects.get(pk=employee_id)
                self.fields['service'].queryset = employee.services.filter(is_active=True)
            except EmployeeBio.DoesNotExist:
                self.fields['service'].queryset = BaseService.objects.none()
        else:
            self.fields['service'].queryset = BaseService.objects.filter(is_active=True)

        if service:
            self.fields['service'].initial = service

        self.service_queryset = self.fields['service'].queryset

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('service'):
            self.add_error('service', 'Моля, изберете услуга.')
        return cleaned_data


class AppointmentCreateForm(AppointmentForm):
    pass


class AppointmentEditForm(AppointmentForm):
    pass


class SlotSearchForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=EmployeeBio.objects.all(), label="Служител")
    service = forms.ModelChoiceField(queryset=BaseService.objects.filter(is_active=True), label="Услуга")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата")


    def __init__(self, *args, **kwargs):
        # Needed in order to filter services by current employee

        employee_id = kwargs.pop('employee_id', None)
        super().__init__(*args, **kwargs)

        if not employee_id:
            if self.data.get('employee'):
                employee_id = self.data.get('employee')
            elif self.initial.get('employee'):
                employee_id = self.initial.get('employee')

        if employee_id:
            try:
                employee = EmployeeBio.objects.get(pk=employee_id)
                self.fields['service'].queryset = employee.services.filter(is_active=True)
            except EmployeeBio.DoesNotExist:
                self.fields['service'].queryset = BaseService.objects.none()



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
