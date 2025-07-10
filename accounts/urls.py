from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views
from accounts.forms import CustomLoginForm

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('login/google/', views.google_login_redirect, name='login-google'),
    path('complete-profile/', views.CompleteProfileView.as_view(), name='complete-profile'),

    path('<int:pk>/', include([
        path('profile-details/', views.CurrentProfileDetailView.as_view(), name='profile_details'),
    #     path('profile-edit/', views.CurrentProfileEditView.as_view(), name='profile_edit'),
    #     path('profile-delete/', views.CurrentProfileDeleteView.as_view(), name='profile_delete'),
    ]))











]
