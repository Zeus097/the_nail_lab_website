from django.db import models


class GalleryPhoto(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
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
