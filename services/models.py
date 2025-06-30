from django.db import models


class BaseService(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.name} – {self.price}лв"
