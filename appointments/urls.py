from django.urls import path
from appointments import views

urlpatterns = [
    path('', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
]
