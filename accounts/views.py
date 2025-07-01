from django.contrib.auth import login
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import BaseUserCreationForm
from accounts.models import ClientProfile, EmployeeBio


class UserRegistrationView(CreateView):
    form_class = BaseUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('homepage')
    # Uses signal to attach the ClientProfile

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        EmployeeBio.objects.create(user=user)
        login(self.request, user, backend='accounts.authentication.LogInWithEmail')
        return response
