from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from accounts.forms import BaseUserCreationForm, CompleteProfileForm, ProfilePhotoForm, ProfileEditForm
from accounts.models import BaseUser, ClientProfile, EmployeeBio


class UserRegistrationView(CreateView):
    form_class = BaseUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        user.telephone_number = form.cleaned_data.get('telephone_number', '')
        user.save()

        # USING LogInWithEmail from authentication.py to log in with email
        login(self.request, user, backend='accounts.authentication.LogInWithEmail')
        return response


# GOOGLE LOG IN
def google_login_redirect(request):
    url = reverse('social:begin', args=['google-oauth2'])
    return redirect(url)


# GOOGLE attach user to project db if Logging for first time with GOOGLE
class CompleteProfileView(LoginRequiredMixin, UpdateView):
    form_class = CompleteProfileForm
    model = BaseUser
    template_name = 'registration/complete_profile.html'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user


class CurrentProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "accounts/profile_details.html"

    def get_object(self, queryset=None):
        user = self.request.user

        if user.is_client:
            return ClientProfile.objects.get(user=user)

        elif user.is_employee:
            return EmployeeBio.objects.get(user=user)

        raise Http404("Няма такъв профил за този потребител.")

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_client or user.is_employee)

    def handle_no_permission(self):
        return redirect(reverse_lazy("homepage"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_type'] = 'client' if user.is_client else 'employee'
        return context


class CurrentProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_client or user.is_employee)

    def handle_no_permission(self):
        return redirect(reverse_lazy("homepage"))

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clean()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_client or user.is_employee)

    def handle_no_permission(self):
        return redirect(reverse_lazy("homepage"))

    def form_valid(self, form):
        messages.success(self.request, "Паролата е променена успешно.")
        return super().form_valid(form)

    def get_success_url(self):
        self.request.session.clear()
        return reverse_lazy('homepage')



class CurrentProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'accounts/profile_delete.html'

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_client or user.is_employee)

    def handle_no_permission(self):
        return redirect(reverse_lazy("homepage"))

    def get_success_url(self):
        return reverse_lazy('homepage')



class ProfilePhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = BaseUser
    form_class = ProfilePhotoForm
    template_name = 'accounts/update_photo.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.object.pk})


class ContactListView(ListView):
    model = BaseUser
    template_name = 'accounts/address.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return BaseUser.objects.filter(is_employee=True).order_by('first_name')







