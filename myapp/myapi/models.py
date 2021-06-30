from django.db import models
# Create your models here.


class WeatherCity(models.Model):
    """Model for save information about weather in 100 cities"""
    city = models.CharField(max_length=30)
    date = models.DateTimeField()
    weather = models.TextField(default=None)

    def __str__(self):
        return f'city {self.city}, date {self.date}, ' \
               f'weather {self.weather}'


class TopCities(models.Model):
    """Model for save names top 100 cities"""
    city = models.CharField(max_length=30)

    def __str__(self):
        return f'city {self.city}'
