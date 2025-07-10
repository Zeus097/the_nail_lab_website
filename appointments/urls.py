from django.urls import path, include
from appointments import views

urlpatterns = [
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('list/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('day_off/', views.DayOffCreateView.as_view(), name='employee_dayoff'),
    path('day_off-list/', views.DayOffListView.as_view(), name='dayoff_list'),
    path('<int:pk>/', include([
        path('details/', views.CurrentAppointmentDetailView.as_view(), name='appointment_details'),
        path('edit/', views.CurrentAppointmentEditView.as_view(), name='appointment_edit'),
        # path('delete/', views.CurrentAppointmentDeleteView.as_view(), name='appointment_delete'),

    ]))

]
