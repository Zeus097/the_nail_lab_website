from django.urls import path, include
from photos import views


urlpatterns = [
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('gallery/upload/', views.GalleryUploadView.as_view(), name='gallery_upload'),
    path('certificate_upload/', views.CertificateUploadView.as_view(), name='certificate_upload'),
    path('<int:pk>/gallery/delete/', views.GalleryDeleteView.as_view(), name='gallery_delete'),
]
