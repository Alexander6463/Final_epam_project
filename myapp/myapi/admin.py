from django.contrib import admin

# Register your models here.
from .models import WeatherCity

admin.site.register(WeatherCity)
