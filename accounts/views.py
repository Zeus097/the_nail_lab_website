from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import BaseUserCreationForm
from user.models import  ClientProfile


class UserRegistrationView(CreateView):
    form_class = BaseUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        ClientProfile.objects.create(user=user)
        login(self.request, user)

        return response
