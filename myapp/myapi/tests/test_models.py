import datetime
from django.test import TestCase

from myapi.models import WeatherCity, TopCities


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        WeatherCity.objects.create(city='Moscow',
                                   date=datetime.datetime.now(),
                                   weather='test')

    def test_city_label(self):
        weather = WeatherCity.objects.get(id=1)
        field_label = weather._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_city_max_length(self):
        weather = WeatherCity.objects.get(id=1)
        max_length = weather._meta.get_field('city').max_length
        self.assertEquals(max_length, 50)

    def test_date_label(self):
        weather = WeatherCity.objects.get(id=1)
        field_label = weather._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

    def test_weather_label(self):
        weather = WeatherCity.objects.get(id=1)
        field_label = weather._meta.get_field('weather').verbose_name
        self.assertEquals(field_label, 'weather')

    def test_object_name(self):
        weather = WeatherCity.objects.get(id=1)
        expected_object_name = f'city {weather.city}, ' \
                               f'date {weather.date}, ' \
                               f'weather {weather.weather}'
        self.assertEquals(expected_object_name, str(weather))


class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        TopCities.objects.create(city='Moscow')

    def test_city_label(self):
        top_city = TopCities.objects.get(id=1)
        field_label = top_city._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_object_name(self):
        top_city = TopCities.objects.get(id=1)
        expected_object_name = f'city {top_city.city}'
        self.assertEquals(expected_object_name, str(top_city))
