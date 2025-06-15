from django.urls import path, include
from studio import views

urlpatterns = [
    path('', views.index, name='index'),
]
