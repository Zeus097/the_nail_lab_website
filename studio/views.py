from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from accounts.models import EmployeeBio
from appointments.models import Appointment, DayOff


class HomePageView(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy('homepage')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['common/base.html']
        return ['common/home-no-profile.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_employee'] = getattr(user, 'is_employee', False)

        if user.is_authenticated:
            if hasattr(user, "clientprofile"):
                context['appointment_list'] = Appointment.objects.filter(
                    client__user=user,
                ).order_by("date", "start_time")

            elif hasattr(user, "employeebio"):
                context['appointment_list'] = Appointment.objects.filter(
                    employee__user=user,
                ).order_by("date", "start_time")
            else:
                context['appointment_list'] = []

            context['day_off_list'] = DayOff.objects.select_related('employee').order_by('date')

        else:
            context['appointment_list'] = []
            context['day_off_list'] = []

        return context
