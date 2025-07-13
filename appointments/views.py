from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from appointments.helper_for_views_validation import inject_service_if_valid, inject_employee_if_valid
from appointments.models import Appointment, DayOff
from appointments.forms import AppointmentCreateForm, AppointmentEditForm, DayOffEditForm, DayOffCreateForm, \
    SlotSearchForm
from accounts.models import ClientProfile, EmployeeBio
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views import View
from appointments.utils import find_earliest_available_slots
from services.models import BaseService


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm
    template_name = 'appointments/create-appointment.html'
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        service_id = self.request.GET.get('service_id')
        employee_id = self.request.GET.get('employee_id')
        date = self.request.GET.get('date')
        start_time = self.request.GET.get('start_time')

        # THE LOGIC IS IN helper_for_views_validation.py for better UI
        kwargs = inject_service_if_valid(service_id, kwargs)
        kwargs = inject_employee_if_valid(employee_id, kwargs)
        # ------------------------------------------------------------

        if date:
            kwargs.setdefault('initial', {})['date'] = date

        if start_time:
            kwargs.setdefault('initial', {})['start_time'] = start_time

        return kwargs

    def form_valid(self, form):
        client_profile, _ = ClientProfile.objects.get_or_create(user=self.request.user)
        form.instance.client = client_profile
        form.instance.employee = form.cleaned_data.get('employee')
        form.instance.service = form.cleaned_data.get('service')

        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.request.GET.get('service_id')
        if service_id:
            context['selected_service_id'] = int(service_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get('date')
        start_time = self.request.GET.get('start_time')

        if date:
            initial['date'] = date
        if start_time:
            initial['start_time'] = start_time

        return initial


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointments-list.html'
    context_object_name = 'appointment_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_employee:
            return Appointment.objects.filter(employee__user=user).order_by("date", "start_time")
        elif user.is_client:
            return Appointment.objects.filter(client__user=user).order_by("date", "start_time")
        return Appointment.objects.none()


class CurrentAppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment-details.html'


class CurrentAppointmentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class = AppointmentEditForm
    template_name = 'appointments/appointment-edit.html'
    # pk_url_kwarg = 'pk'  # Not needed because the default is 'pk'

    def form_valid(self, form):
        client_profile, _ = ClientProfile.objects.get_or_create(user=self.request.user)

        self.object = form.save(commit=False)

        self.object.client = client_profile
        self.object.service = form.cleaned_data.get('service')
        self.object.employee = form.cleaned_data.get('employee')

        try:
            self.object.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        appointment = self.get_object()
        user = self.request.user
        return hasattr(user, "clientprofile") and appointment.client.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    def get_success_url(self):
        return reverse_lazy('appointment_details', kwargs={'pk': self.object.pk})


class CurrentAppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment-delete-confirmation.html'

    def test_func(self):
        appointment = self.get_object()
        user = self.request.user
        return hasattr(user, "clientprofile") and appointment.client.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    success_url = reverse_lazy('homepage')


# -----------------------------------
class DayOffCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DayOff
    form_class = DayOffCreateForm
    template_name = 'appointments/employee-dayoff.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        return self.request.user.is_employee

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = get_object_or_404(EmployeeBio, user=self.request.user)
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


class DayOffListView(LoginRequiredMixin, ListView):
    model = DayOff
    template_name = 'appointments/list-of-the-employee-dayoff.html'
    context_object_name = 'day_off_list'

    def get_queryset(self):
        user = self.request.user
        return DayOff.objects.select_related('employee', 'employee__user').order_by('date')


class CurrentDayOffDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DayOff
    template_name = 'appointments/dayoff-details.html'

    def test_func(self):
        day_off = self.get_object()
        user = self.request.user
        return hasattr(user, "employeebio") and day_off.employee.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))


class CurrentDayOffEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DayOff
    form_class = DayOffEditForm
    template_name = 'appointments/dayoff-edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = self.request.user.employeebio
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def test_func(self):
        day_off = self.get_object()
        user = self.request.user
        return hasattr(user, "employeebio") and day_off.employee.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    def get_success_url(self):
        return reverse_lazy('day_off_details', kwargs={'pk': self.object.pk})


class CurrentDayOffDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DayOff
    template_name = 'appointments/dayoff-delete-confirmation.html'

    def test_func(self):
        day_off = self.get_object()
        user = self.request.user
        return hasattr(user, "employeebio") and day_off.employee.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    success_url = reverse_lazy('homepage')


class AvailableSlotsView(View):
    template_name = 'appointments/available_slots.html'

    def get(self, request):
        form = SlotSearchForm()
        return render(request, self.template_name, {'form': form, 'slots': None})

    def post(self, request):
        form = SlotSearchForm(request.POST)
        slots = None

        if form.is_valid():
            employee = form.cleaned_data['employee']
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            slots = find_earliest_available_slots(employee, service, date)

        return render(request, self.template_name, {
            'form': form,
            'slots': slots
        })













