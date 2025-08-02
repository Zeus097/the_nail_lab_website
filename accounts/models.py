from the_nail_lab_website import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.validators import ImageSizeValidator, PhoneValidator
from accounts.managers import BaseUserManager


class BaseUser(AbstractUser):

    objects = BaseUserManager()


    email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    # is_employee = TRUE --> MANUALLY ENTERED ONLY BY ADMIN, THROUGH ADMIN PANEL

    telephone_number = models.CharField(
        max_length=20,
        validators=[PhoneValidator()],
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        # upload_to='user_photos',  --> Because Claudinary
        blank=True,
        null=True,
        # default='defaults/default_user.png',  --> Because Claudinary
        validators=[ImageSizeValidator(5)],
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
    biography = models.TextField(blank=True)
    services = models.ManyToManyField('services.BaseService', related_name='employees')
    # ManyToMany because it could have more employees in the future.

    def __str__(self):
        return self.user.get_full_name() or self.name or self.user.username


class ClientProfile(models.Model):
    class Meta:
        verbose_name = "Клиентски профил"
        verbose_name_plural = "Клиентски профили"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

    @property
    def email(self):
        return self.user.email

    @property
    def name(self):
        return self.user.username
