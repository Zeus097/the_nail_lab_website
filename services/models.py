from django.db import models

from cloudinary_storage.storage import MediaCloudinaryStorage


class BaseService(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    duration = models.IntegerField()
    service_photo = models.ImageField(
        storage=MediaCloudinaryStorage(),
    )

    def __str__(self):
        return f"{self.name}"
