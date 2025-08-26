from django.urls import path, include
from appointments import views

urlpatterns = [
    path('create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('available-slots/', views.AvailableSlotsView.as_view(), name='available-slots'),
    path('day_off/', views.DayOffCreateView.as_view(), name='employee-day-off'),
    path('booked-appointments/', views.BookedAppointmentsView.as_view(), name='booked-appointments'),
    path('<int:pk>/', include([
        path('appointment-details/', views.CurrentAppointmentDetailView.as_view(), name='appointment-details'),
        path('appointment-edit/', views.CurrentAppointmentEditView.as_view(), name='appointment-edit'),
        path('appointment-delete/', views.CurrentAppointmentDeleteView.as_view(), name='appointment-delete'),

        path('day_off-details/', views.CurrentDayOffDetailView.as_view(), name='day-off-details'),
        path('day_off-edit/', views.CurrentDayOffEditView.as_view(), name='day-off-edit'),
        path('day_off-delete/', views.CurrentDayOffDeleteView.as_view(), name='day-off-delete'),
    ]))
]
