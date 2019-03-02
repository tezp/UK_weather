from django.db import models


# Create your models here.


class Weather(models.Model):
    class Meta:
        unique_together = (('location', 'metrics', 'date'),)

    # columns in database
    location = models.CharField(max_length=20)
    metrics = models.CharField(max_length=20)
    value = models.FloatField(default=0)
    date = models.DateField(max_length=10)
