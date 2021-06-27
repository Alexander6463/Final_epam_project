# Create your tasks here

from celery import shared_task
from .models import WeatherCity
from .services import WorkWithDatabase, MyRequest


@shared_task()
def add_information_about_weather():
    """celery task for get information
    about weather 100 the biggest cities"""
    req = MyRequest()
    db = WorkWithDatabase()
    db.insert_weather_with_100_cities(req.get_weather_100_cities(),
                                      WeatherCity)
    return 'Weather of 100 cities has been added'
