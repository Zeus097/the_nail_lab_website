from django.db import models
from staff.validators import ImageSizeValidator
from staff.choices import JobTypeChoice


class EmployeeBio(models.Model):
    name = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=50,
        choices=JobTypeChoice.choices
    )
    biography = models.CharField(max_length=500)
    telephone_number = models.CharField(max_length=20)
    services = models.ManyToManyField('services.BaseService', related_name='employees')
    # TODO: Да наследя тозиклас, като направя за всяка от 3те по един клас,
    #  който да води към услугите на ('services.МАНИКЮР/ ГРИМ/ etc..'--> също наследяване и така да се записват в необходимите бази)

    # TODO: След това ще трябва да оформя вече вютата и формите


    photo = models.ImageField(
        upload_to='staff_photos',
        validators=[
            ImageSizeValidator(5)
        ]
    )

    def __str__(self):
        return f"{self.name} ({self.job_type})"
