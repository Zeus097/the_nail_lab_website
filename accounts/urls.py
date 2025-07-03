from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views
from accounts.forms import CustomLoginForm

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

        #
        # TODO: Add logout logic and make the button inside the profile menu
        #
        # TODO: Read from lecturer for logout with method POST in GitHub forumApp
        #     and the style none to be added in separate CSS in the logout.css, when I crate it!
        #
        # TODO: It has it on screenshot tho, so I can do it in the file for logout.html..!
        #

]