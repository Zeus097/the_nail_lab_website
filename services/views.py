from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from services.models import BaseService


class ServiceListView(LoginRequiredMixin, ListView):
    # LoginRequiredMixin is first because of MRO

    context_object_name = 'services'
    model = BaseService
    template_name = 'services/services-page.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset.order_by('id')


def service_details(request, pk):
    service = BaseService.objects.get(pk=pk)
    context = {'service': service}

    return render(request, 'services/service-details.html', context)
