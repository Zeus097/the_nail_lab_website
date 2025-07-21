from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from appointments.models import Appointment, DayOff


class HomePageView(TemplateView):
    success_url = reverse_lazy('homepage')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['common/base.html']
        return ['common/home_no_profile.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = localtime().date()

        context['is_employee'] = getattr(user, 'is_employee', False)
        context['is_admin'] = user.is_superuser

        context['appointment_list'] = []
        context['day_off_list'] = []

        if user.is_authenticated:
            if user.is_superuser:
                context['appointment_list'] = Appointment.objects.filter(
                    date__gte=today
                ).order_by("date", "start_time")
                context['day_off_list'] = DayOff.objects.select_related('employee', 'employee__user').order_by('date')

            elif hasattr(user, "employeebio"):
                employee = user.employeebio
                context['appointment_list'] = Appointment.objects.filter(
                    employee=employee,
                    date__gte=today
                ).order_by("date", "start_time")
                context['day_off_list'] = DayOff.objects.select_related('employee', 'employee__user').order_by('date')

            elif hasattr(user, "clientprofile"):
                context['appointment_list'] = Appointment.objects.filter(
                    client__user=user,
                    date__gte=today
                ).order_by("date", "start_time")
                context['day_off_list'] = DayOff.objects.select_related('employee', 'employee__user').order_by('date')

        return context


def preview_404(request):
    return render(request, '404.html', status=404)
    # FOR TESTING 404 BEFORE DEPLOYMENT
