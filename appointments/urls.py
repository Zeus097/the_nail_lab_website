from django.urls import path
from appointments import views

urlpatterns = [
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('list/', views.AppointmentListView.as_view(), name='appointment_list'),
]
