from django.urls import path
from studio import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('preview-404/', views.preview_404),
]
