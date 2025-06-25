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
        login(self.request, user)

        #Закачване на потребителския профил
        ClientProfile.objects.create(user=user)

        # try:
        #     profile = ClientProfile.objects.create(user=user)
        #     print(f"✅ Профил създаден за {user.username}")
        # except Exception as e:
        #     print(f"❌ Грешка при създаване на профил: {e}")


        return response

    # def form_invalid(self, form):
    #     print("❌ ФОРМАТА Е НЕВАЛИДНА")
    #     print(form.errors)
    #     return super().form_invalid(form)
