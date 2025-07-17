from django.urls import path, include
from appointments import views

urlpatterns = [
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('available-slots/', views.AvailableSlotsView.as_view(), name='available_slots'),
    # path('list/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('day_off/', views.DayOffCreateView.as_view(), name='employee_dayoff'),
    # path('day_off-list/', views.DayOffListView.as_view(), name='dayoff_list'),
    path('<int:pk>/', include([
        path('appointment-details/', views.CurrentAppointmentDetailView.as_view(), name='appointment_details'),
        path('appointment-edit/', views.CurrentAppointmentEditView.as_view(), name='appointment_edit'),
        path('appointment-delete/', views.CurrentAppointmentDeleteView.as_view(), name='appointment_delete'),

        path('day_off-details/', views.CurrentDayOffDetailView.as_view(), name='day_off_details'),
        path('day_off-edit/', views.CurrentDayOffEditView.as_view(), name='day_off_edit'),
        path('day_off-delete/', views.CurrentDayOffDeleteView.as_view(), name='day_off_delete'),
    ]))
]
