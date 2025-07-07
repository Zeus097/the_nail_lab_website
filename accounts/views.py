from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from accounts.forms import BaseUserCreationForm, CompleteProfileForm
from accounts.models import BaseUser


class UserRegistrationView(CreateView):
    form_class = BaseUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        user.telephone_number = form.cleaned_data.get('telephone_number', '')
        user.save()

        login(self.request, user, backend='accounts.authentication.LogInWithEmail')
        return response


def google_login_redirect(request):
    url = reverse('social:begin', args=['google-oauth2'])
    return redirect(url)


class CompleteProfileView(LoginRequiredMixin, UpdateView):
    form_class = CompleteProfileForm
    model = BaseUser
    template_name = 'registration/complete_profile.html'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user
