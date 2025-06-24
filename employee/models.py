from django.db import models
from employee.validators import ImageSizeValidator
from the_nail_lab_website import settings


class EmployeeBio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    biography = models.CharField(max_length=500)
    telephone_number = models.CharField(max_length=20)
    services = models.ManyToManyField('services.BaseService', related_name='employees')

    photo = models.ImageField(
        upload_to='staff_photos',
        validators=[
            ImageSizeValidator(5)
        ]
    )

    def __str__(self):
        return f"{self.name}"
