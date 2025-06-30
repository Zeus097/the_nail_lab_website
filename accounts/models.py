from the_nail_lab_website import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.validators import ImageSizeValidator


class BaseUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.username


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
        return f"{self.name} ({self.user.username})"


class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    photo = models.FileField(
        validators=[
            ImageSizeValidator(5),
        ],
        upload_to='files',
    )

    def __str__(self):
        return f"{self.user.username} ({self.phone})"

    @property
    def email(self):
        return self.user.email

    @property
    def name(self):
        return self.user.username