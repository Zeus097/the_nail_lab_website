from django.urls import path, include
from services import views


urlpatterns = [
    path('', views.ServiceListView.as_view(), name='services'),
    path('<int:pk>/', views.service_details, name='service_details'),
]
