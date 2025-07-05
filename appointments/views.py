from django.urls import reverse_lazy
from django.views.generic import CreateView
from appointments.models import Appointment
from appointments.forms import AppointmentForm
from accounts.models import ClientProfile, EmployeeBio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/create-appointment.html'
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = EmployeeBio.objects.first()
        return kwargs

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.client = ClientProfile.objects.get(user=self.request.user)
        appointment.employee = EmployeeBio.objects.first()
        appointment.save()
        return super().form_valid(form)


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointments-list.html'
    context_object_name = 'appointment_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_employee:
            return Appointment.objects.filter(employee__user=user)
        elif user.is_client:
            return Appointment.objects.filter(client__user=user)
        return Appointment.objects.none()
