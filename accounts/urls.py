from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views
from accounts.forms import CustomLoginForm

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
