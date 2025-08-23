from django.urls import path
from services import views


urlpatterns = [
    path('', views.ServiceListView.as_view(), name='services'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='service_details'),
    path('service-prices', views.ServicePricePageView.as_view(), name='service-prices'),
]
