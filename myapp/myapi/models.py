from django.db import models
# Create your models here.


class WeatherCity(models.Model):
    """Model for save information about weather in 100 cities"""
    city = models.CharField(max_length=50, null=False)
    date = models.DateTimeField(null=False, db_index=True)
    weather = models.TextField(null=False)

    def __str__(self):
        return f'city {self.city}, date {self.date}, ' \
               f'weather {self.weather}'


class TopCities(models.Model):
    """Model for save names top 100 cities"""
    city = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return f'city {self.city}'
