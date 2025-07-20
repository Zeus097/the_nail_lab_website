from django.db import models


class GalleryPhoto(models.Model):
    class Meta:
        verbose_name = "Галерия"

    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='gallery_photos',)

    uploader = models.ForeignKey(
        to='accounts.EmployeeBio',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='uploaded_photos',
    )

    def __str__(self):
        return f"{self.name} - {self.description} - {self.upload_date}"


class CertificateImage(models.Model):
    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификати"


    photo = models.ImageField(upload_to='certificates', )
    uploader = models.ForeignKey(
        to='accounts.EmployeeBio',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='certificates',
    )

    def __str__(self):
        return f"Сертификат от: {self.uploader.user.username if self.uploader else 'Непознат'}"
