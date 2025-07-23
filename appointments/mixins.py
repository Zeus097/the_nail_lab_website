from appointments.helper_for_views_validation import inject_service_if_valid, inject_employee_if_valid

class AppointmentFormInitMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        request = self.request
        service_id = request.GET.get('service_id')
        employee_id = request.GET.get('employee_id')
        date = request.GET.get('date')
        start_time = request.GET.get('start_time')

        # Inject valid service and employee
        kwargs = inject_service_if_valid(service_id, kwargs)
        kwargs = inject_employee_if_valid(employee_id, kwargs)

        if employee_id:
            kwargs['employee_id'] = employee_id

        # Set initial values for date and start time
        initial = kwargs.setdefault('initial', {})
        if date:
            initial['date'] = date
        if start_time:
            initial['start_time'] = start_time

        return kwargs
