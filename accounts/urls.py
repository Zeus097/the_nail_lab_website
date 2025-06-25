from django.contrib.auth.views import LoginView
from django.urls import path

from accounts import views

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]