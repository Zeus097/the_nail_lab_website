from django.shortcuts import render
from django.views.generic import ListView
from services.models import BaseService


class ServiceListView(ListView):
    context_object_name = 'services'
    model = BaseService
    template_name = 'services/services-page.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset.order_by('id')
