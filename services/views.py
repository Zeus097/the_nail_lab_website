from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from services.forms import SearchForm
from services.models import BaseService


class ServiceListView(LoginRequiredMixin, ListView):
    # LoginRequiredMixin is first because of MRO

    context_object_name = 'services'
    model = BaseService
    template_name = 'services/services-page.html'
    paginate_by = 4
    query_param = "query"
    form_class = SearchForm

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_parameter = self.request.GET.get(self.query_param)
        if search_parameter:
            queryset = queryset.filter(
                Q(name__icontains=search_parameter)
                |
                Q(description__icontains=search_parameter)
            )
        return queryset.order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({
            'search_form': self.form_class,
            'query': self.request.GET.get(self.query_param, ''),
        })
        return super().get_context_data(object_list=object_list, **kwargs)


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = BaseService
    template_name = 'services/service-details.html'
    context_object_name = 'service'
