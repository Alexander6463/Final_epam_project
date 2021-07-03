
import csv
import requests
import json
import time

from datetime import datetime
from django.http import StreamingHttpResponse

from .models import WeatherCity, TopCities
from .serializers import WeatherCitiesSerializer, TopCitiesSerializer
from myapp.settings import MY_API_KEY


class MyRequest:
    def __init__(self):
        self.api_key = MY_API_KEY

    def get_weather_city(self, city, units='metric'):
        """get information about weather in the city
        use units = metric if you want to get temperature in Celsius
        and use units = imperial if you want
        to get temperature in Fahrenheits"""

        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/'
            f'weather?q={city}&units={units}&appid={self.api_key}')
        if response.ok:
            return json.loads(response.text)

    def get_weather_100_cities(self):
        """get information about weather in
         the biggest 100 cities in the world"""
        weather_100_cities = list()
        cities = select_all(TopCities)
        serializer = TopCitiesSerializer(cities, many=True)
        for index in serializer.data:
            city = index['city']
            response = requests.get(
                f'http://api.openweathermap.org/'
                f'data/2.5/weather?q={city}'
                f'&units=metric&appid={self.api_key}')
            weather_100_cities.append({'city': city,
                                       'date': datetime.now(),
                                       'weather': json.loads(response.text)})
            time.sleep(1)  # free account only 60 calls per minute
        return weather_100_cities


def insert_weather_with_100_cities(weather_info, weather):
    """This func saves information into database"""
    for info in weather_info:
        try:
            weather(city=info['city'],
                    date=info['date'],
                    weather=info['weather']).save()
        except TypeError:
            print('Error with information', info)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_to_csv_from_database(date_begin, date_end):
    """this function used for get information from
    database and write it into csv dict"""
    weathers = WeatherCity.objects.filter(date__gte=date_begin,
                                          date__lte=date_end)
    serializer = WeatherCitiesSerializer(weathers, many=True)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow([weather['city'],
                          weather['date'],
                          weather['weather']])
         for weather in serializer.data), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response


def select_all(model):
    return model.objects.all()
