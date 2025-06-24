from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.username

