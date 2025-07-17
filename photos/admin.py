from django.contrib import admin
from photos.models import GalleryPhoto, CertificateImage


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploader', 'upload_date')
    search_fields = ('name', 'description')
    readonly_fields = ('upload_date',)


@admin.register(CertificateImage)
class CertificateImageAdmin(admin.ModelAdmin):
    list_display = ['photo', 'uploader']

