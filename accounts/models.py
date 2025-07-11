from the_nail_lab_website import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.validators import ImageSizeValidator, PhoneValidator


class BaseUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    telephone_number = models.CharField(
        max_length=20,
        validators=[PhoneValidator()],
    )

    def __str__(self):
        return self.username


class EmployeeBio(models.Model):
    # Using signal to attach this model to the employee profile, created through Admin interface

    class Meta:
        verbose_name = "Служебен профил"
        verbose_name_plural = "Служебни профили"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    biography = models.CharField(max_length=500, blank=True)
    services = models.ManyToManyField('services.BaseService', related_name='employees')

    photo = models.ImageField(
        upload_to='staff_photos',
        default='defaults/default_user.png',
        validators=[ImageSizeValidator(5)],
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}"


class ClientProfile(models.Model):
    class Meta:
        verbose_name = "Клиентски профил"
        verbose_name_plural = "Клиентски профили"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.FileField(
        upload_to='user_photos',
        default='defaults/default_user.png',
        validators=[ImageSizeValidator(5)],
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}"

    @property
    def email(self):
        return self.user.email

    @property
    def name(self):
        return self.user.username
