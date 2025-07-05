from django.views.generic import TemplateView
from django.urls import reverse_lazy
from appointments.models import Appointment
from datetime import date


class HomePageView(TemplateView):
    success_url = reverse_lazy('homepage')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['common/base.html']
        return ['common/home-no-profile.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

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

        return context
