from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views
from accounts.forms import CustomLoginForm

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('login/google/', views.google_login_redirect, name='login-google'),
    path('complete-profile/', views.CompleteProfileView.as_view(), name='complete-profile'),


    path('<int:pk>/', include([
        path('profile/', views.CurrentProfileDetailView.as_view(), name='profile-details'),
        path('profile/update-photo/', views.ProfilePhotoUpdateView.as_view(), name='update-photo'),
        path('profile-edit/', views.CurrentProfileEditView.as_view(), name='profile-edit'),
        path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
        path('profile-delete/', views.CurrentProfileDeleteView.as_view(), name='profile-delete'),
    ])),

    path('address/', views.ContactListView.as_view(), name='contact-list'),

]
