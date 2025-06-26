from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('', LogoutView.as_view(), name='logout'),

    
    # TODO: Add logout logic and make the button inside the profile menu
    #  and read from lecturer for logout with method POST in GitHub forumApp
    #  and the style none to be added in ceparate CSS in the logout.css, when I crate it!
    #  It has it on screenshot thoo, so I can do it in the file for logout.html..!


]