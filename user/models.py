from django.db import models
from django.conf import settings
from user.validators import FileSizeValidator


class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    photo = models.FileField(
        validators=[
            FileSizeValidator(5),
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

