from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.db.models import Q

from appointments.config import MAX_SLOTS_PER_DAY
from appointments.mixins import AppointmentFormPrefillMixin
from appointments.models import Appointment, DayOff
from appointments.forms import AppointmentCreateForm, AppointmentEditForm, DayOffEditForm, DayOffCreateForm, \
    SlotSearchForm
from appointments.utils import find_earliest_available_slots

from accounts.models import EmployeeBio, ClientProfile
from accounts.utils import send_mailjet_email


class AppointmentCreateView(LoginRequiredMixin, AppointmentFormPrefillMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm
    template_name = 'appointments/appointment_create.html'
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.request.GET.get('service_id')
        if service_id:
            context['selected_service_id'] = int(service_id)
        return context

    def form_valid(self, form):
        client_profile = get_object_or_404(ClientProfile, user=self.request.user)
        form.instance.client = client_profile
        form.instance.employee = form.cleaned_data.get('employee')
        form.instance.service = form.cleaned_data.get('service')

        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)


        response = super().form_valid(form)

        client_email = self.request.user.email
        employee_email = getattr(self.object.employee.user, 'email', None)
        subj_message = "Часът е запазен успешно!"

        if client_email and employee_email:
            send_mailjet_email(
                subject=subj_message,
                client_email=client_email,
                employee_email=employee_email,
                template_name="appointments/email_notification_appointment.html",
                context={
                    "subj_message": subj_message,
                    "employee": self.object.employee,
                    "client": self.object.client,
                    "service": self.object.service,
                    "date": self.object.date,
                    "time": self.object.start_time,
                    "comment": self.object.comment or "",
                }
            )

        return response


    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get('date')
        start_time = self.request.GET.get('start_time')

        if date:
            initial['date'] = date
        if start_time:
            initial['start_time'] = start_time

        return initial


class CurrentAppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_details.html'


class CurrentAppointmentEditView(LoginRequiredMixin, UserPassesTestMixin, AppointmentFormPrefillMixin, UpdateView):
    model = Appointment
    form_class = AppointmentEditForm
    template_name = 'appointments/appointment_edit.html'
    # pk_url_kwarg = 'pk'  # Not needed because the default is 'pk'

    def form_valid(self, form):
        client_profile = get_object_or_404(ClientProfile, user=self.request.user)

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


        response = super().form_valid(form)


        client_email = self.request.user.email
        employee_email = getattr(self.object.employee.user, 'email', None)
        subj_message = "Часът е променен успешно!"

        if client_email and employee_email:
            send_mailjet_email(
                subject=subj_message,
                client_email=client_email,
                employee_email=employee_email,
                template_name="appointments/email_notification_appointment.html",
                context={
                    "subj_message": subj_message,
                    "employee": self.object.employee,
                    "client": self.object.client,
                    "service": self.object.service,
                    "date": self.object.date,
                    "time": self.object.start_time,
                    "comment": self.object.comment or "",
                }
            )

        return response




    def test_func(self):
        appointment = self.get_object()
        user = self.request.user
        return hasattr(user, "clientprofile") and appointment.client.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    def get_success_url(self):
        return reverse_lazy('appointment-details', kwargs={'pk': self.object.pk})


class CurrentAppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_delete_confirmation.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        appointment = self.get_object()
        user = self.request.user
        return hasattr(user, "clientprofile") and appointment.client.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        client_email = self.request.user.email
        employee_email = getattr(self.object.employee.user, 'email', None)
        subj_message = "Часът е отменен!"

        if client_email and employee_email:
            send_mailjet_email(
                subject=subj_message,
                client_email=client_email,
                employee_email=employee_email,
                template_name="appointments/email_notification_appointment.html",
                context={
                    "subj_message": subj_message,
                    "employee": self.object.employee,
                    "client": self.object.client,
                    "service": self.object.service,
                    "date": self.object.date,
                    "time": self.object.start_time,
                    "comment": self.object.comment or "",
                }
            )

        return super().post(request, *args, **kwargs)


# -----------------------------------------------------------------------------------------------
class DayOffCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DayOff
    form_class = DayOffCreateForm
    template_name = 'appointments/day_off_employee.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        return self.request.user.is_employee

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = get_object_or_404(EmployeeBio, user=self.request.user)
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


class CurrentDayOffDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DayOff
    template_name = 'appointments/day_off_details.html'

    def test_func(self):
        day_off = self.get_object()
        user = self.request.user
        return hasattr(user, "employeebio") and day_off.employee.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))


class CurrentDayOffEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DayOff
    form_class = DayOffEditForm
    template_name = 'appointments/day_off_edit.html'

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
        return reverse_lazy('day-off-details', kwargs={'pk': self.object.pk})


class CurrentDayOffDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DayOff
    template_name = 'appointments/day_off_delete_confirmation.html'

    def test_func(self):
        day_off = self.get_object()
        user = self.request.user
        return hasattr(user, "employeebio") and day_off.employee.user == user

    def handle_no_permission(self):
        return redirect(reverse_lazy('homepage'))

    success_url = reverse_lazy('homepage')


# -----------------------------------------------------------------------------------------------
class AvailableSlotsView(View):
    template_name = 'appointments/available_slots.html'

    def get(self, request):
        employee_id = request.GET.get('employee_id')
        initial_data = {}

        if employee_id:
            initial_data['employee'] = employee_id

        form = SlotSearchForm(initial=initial_data, employee_id=employee_id)
        return render(request, self.template_name, {'form': form, 'slots': None})

    def post(self, request):
        form = SlotSearchForm(request.POST)
        slots = None

        if form.is_valid():
            employee = form.cleaned_data['employee']
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            slots = find_earliest_available_slots(employee, service, date, MAX_SLOTS_PER_DAY)

        return render(request, self.template_name, {
            'form': form,
            'slots': slots
        })



class BookedAppointmentsView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list_for_employees.html'
    context_object_name = 'appointment_list'
    paginate_by = 8


    def test_func(self):
        return self.request.user.is_employee

    def get_queryset(self):
        now = timezone.localtime()
        query = Appointment.objects.filter(
            Q(date__gt=now.date())
            |
            Q(date=now.date(), start_time__gte=now.time())
        )

        return query.order_by('date', 'start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_appointments'] = self.get_queryset().count()
        return context
