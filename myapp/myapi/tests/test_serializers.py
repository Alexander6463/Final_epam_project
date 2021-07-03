from django.test import TestCase
from django.contrib.auth.models import User
from ..serializers import UserSerializer, \
    WeatherCitiesSerializer, TopCitiesSerializer
from ..models import WeatherCity, TopCities


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_attributes = {
            'username': 'pavel',
            'password': 'nikolaev'
        }

        self.user = User.objects.create(**self.user_attributes)
        self.serializer = UserSerializer(instance=self.user)

    def test_serializer_keys(self):
        data = self.serializer.data
        self.assertEqual(data['username'], 'pavel')
        self.assertEqual(data['password'], 'nikolaev')
        self.assertEqual(set(data.keys()), {'username', 'password'})


class WeatherCitiesSerializerTest(TestCase):
    def setUp(self):
        self.weather_cities_attributes = {
            'city': 'Moscow',
            'date': '2021-06-25 18:00',
            'weather': 'some_weather'
        }
        self.weather = WeatherCity.objects.create(
            **self.weather_cities_attributes)
        self.serializer = WeatherCitiesSerializer(instance=self.weather)

    def test_serializer_keys(self):
        data = self.serializer.data
        self.assertEqual(data['city'], 'Moscow')
        self.assertEqual(data['date'], '2021-06-25 18:00')
        self.assertEqual(data['weather'], 'some_weather')
        self.assertEqual(set(data.keys()), {'city', 'date', 'weather'})


class TopCitiesSerializerTest(TestCase):
    def setUp(self):
        self.top_cities_attributes = {
            'city': 'Moscow',
        }
        self.top_cities = TopCities.objects.create(
            **self.top_cities_attributes)
        self.serializer = TopCitiesSerializer(instance=self.top_cities)

    def test_serializer_keys(self):
        data = self.serializer.data
        self.assertEqual(data['city'], 'Moscow')
        self.assertEqual(set(data.keys()), {'city'})
