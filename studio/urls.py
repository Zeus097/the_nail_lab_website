from django.urls import path, include
from studio import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
]
