from django.urls import path, include
from photos import views


urlpatterns = [
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('gallery/upload/', views.GalleryUploadView.as_view(), name='gallery_upload'),
]
