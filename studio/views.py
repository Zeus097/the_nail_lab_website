from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.timezone import localtime, now
from appointments.models import Appointment, DayOff
from django.core.paginator import Paginator



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

        appointment_qs = Appointment.objects.none()
        current_dt = now()

        if user.is_authenticated:
            if user.is_superuser:
                appointment_qs = Appointment.objects.filter(
                    Q(date__gt=current_dt.date())
                    |
                    Q(date=current_dt.date(), start_time__gte=current_dt.time())
                ).order_by("date", "start_time")

                context['day_off_list'] = DayOff.objects.filter(
                    date__gte=today
                ).select_related(
                    'employee', 'employee__user'
                ).order_by('date')

            elif hasattr(user, "employeebio"):
                employee = user.employeebio
                appointment_qs = (
                    Appointment.objects
                    .filter(date__gte=today)
                    .filter(Q(employee=employee) | Q(created_by=user))
                    .order_by("date", "start_time")
                )

                context['day_off_list'] = DayOff.objects.filter(
                    date__gte=current_dt.date()
                ).select_related(
                    'employee', 'employee__user'
                ).order_by('date')


            elif hasattr(user, "clientprofile"):
                appointment_qs = Appointment.objects.filter(
                    client__user=user,
                    date__gte=today
                ).order_by("date", "start_time")

            # Using Paginator, because I don't use ListView here
            paginator = Paginator(appointment_qs, 5)
            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context['appointment_list'] = page_obj.object_list
            context['page_obj'] = page_obj
            context['is_paginated'] = page_obj.has_other_pages()
            context['paginator'] = paginator

        return context


def preview_404(request):
    return render(request, '404.html', status=404)
    # FOR TESTING 404 BEFORE DEPLOYMENT
