# Create your tasks here

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import WeatherCity
from .services import insert_weather_with_100_cities, MyRequest


logger = get_task_logger(__name__)


@shared_task()
def add_information_about_weather():
    """celery task for get information
    about weather 100 the biggest cities"""
    req = MyRequest()
    weather = req.get_weather_100_cities()
    insert_weather_with_100_cities(weather, WeatherCity)
    return 'task add_information_about_weather is successful'
