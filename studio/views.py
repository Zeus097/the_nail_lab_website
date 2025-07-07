from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.timezone import now

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
        today = now().date()

        context['is_employee'] = getattr(user, 'is_employee', False)
        context['is_admin'] = user.is_superuser  # добавяме, за да ползваме в шаблона ако искаш

        if user.is_authenticated:

            if user.is_superuser:
                # Админ вижда всички часове и почивни дни
                context['appointment_list'] = Appointment.objects.filter(
                    date__gte=today
                ).order_by("date", "start_time")
                context['day_off_list'] = DayOff.objects.select_related('employee').order_by('date')

            elif hasattr(user, "employeebio"):
                # Служителят вижда само часовете за себе си
                employee = user.employeebio
                context['appointment_list'] = Appointment.objects.filter(
                    employee=employee,
                    date__gte=today
                ).order_by("date", "start_time")
                # Почивни дни може да вижда всички или само свои, ако искаш — тук всички:
                context['day_off_list'] = DayOff.objects.select_related('employee').order_by('date')

            elif hasattr(user, "clientprofile"):
                # Клиентът вижда само собствените си часове
                context['appointment_list'] = Appointment.objects.filter(
                    client__user=user,
                    date__gte=today
                ).order_by("date", "start_time")
                context['day_off_list'] = []  # Клиентите не виждат почивни дни

            else:
                context['appointment_list'] = []
                context['day_off_list'] = []

        else:
            context['appointment_list'] = []
            context['day_off_list'] = []

        return context
