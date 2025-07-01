from django.urls import path, include
from services import views


urlpatterns = [
    path('', views.ServiceListView.as_view(), name='services'),
]
