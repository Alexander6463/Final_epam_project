from django.http import HttpResponse
import csv
import requests
import json
from datetime import datetime
import time
from .models import WeatherCity, TopCities
from .serializers import WeatherCitiesSerializer, TopCitiesSerializer


class WorkWithDatabase:
    def __init__(self):
        ...

    @staticmethod
    def insert_weather_with_100_cities(weather_info, weather):
        """This func saves information into database"""
        for info in weather_info:
            try:
                weather(city=info['city'],
                        date=info['date'],
                        weather=info['weather']).save()
            except TypeError:
                print('Error with information', info)

    @staticmethod
    def export_to_csv_from_database(date_begin, date_end):
        """this function used for get information from
        database and write it into csv dict"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=['city',
                                                      'date',
                                                      'weather'])
        writer.writeheader()
        weathers = WeatherCity.objects.filter(date__gte=date_begin,
                                              date__lte=date_end)
        serializer = WeatherCitiesSerializer(weathers, many=True)
        for weather in serializer.data:
            writer.writerow({'city': weather['city'],
                             'date': weather['date'],
                             'weather': weather['weather']})
        return response

    @staticmethod
    def select_all(model):
        return model.objects.all()


class MyRequest:
    def __init__(self):
        self.api_key = 'd9cdda3d2e4342354008fd4dd59bd3ed'

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
        cities = WorkWithDatabase().select_all(TopCities)
        serializer = TopCitiesSerializer(cities, many=True)
        for index in serializer.data:
            city = index['city']
            response = requests.get(
                f'http://api.openweathermap.org/data/2.5/'
                f'weather?q={city}&units=metric&appid={self.api_key}')
            weather_100_cities.append({'city': city,
                                       'date': datetime.now(),
                                       'weather': json.loads(response.text)})
            time.sleep(1)  # free account only 60 calls per minute
        return weather_100_cities


class Validation:
    def __init__(self):
        ...

    @staticmethod
    def validate_date(datetime_string):
        """validate date, return true
        if date pattern is %Y-%m-%d %H:%M"""
        try:
            datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False
