import json
import csv

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from django.test import override_settings

from ..models import WeatherCity
from ..serializers import WeatherCitiesSerializer


cache_params = {"default": {"BACKEND":
                            "django.core.cache.backends.dummy.DummyCache"}}


def mocked_requests_get(*args, **kwargs):
    """function for mock requests lib"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.ok = status_code

        def json(self):
            return self.text
    if args[0] == 'Bad request':
        return MockResponse(None, False)
    return MockResponse(args[0], True)


class UserTests(APITestCase):
    def setUp(self) -> None:
        """set up initial params"""
        self.url = 'http://0.0.0.0:8000/api/user/'
        self.data = {'username': 'Test', 'password': 'Test'}

    def test_create_account(self):
        """Ensure we can create a new User object"""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Test')


class CityWeatherTests(APITestCase):
    def setUp(self) -> None:
        """set up initial params"""
        self.city = 'Moscow'
        self.user = User.objects.create_user(username='Test', password='Test')
        self.units = 'metric'
        self.url = f'http://0.0.0.0:8000/api/weather?city={self.city}' \
                   f'&units={self.units}'

    def test_get_weather_city_unauth(self):
        """Ensure that we cant get weather city without auth"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(CACHES=cache_params)
    def test_get_weather_city_with_auth(self):
        """Ensure that we can get weather city with auth"""
        data = json.dumps({'city': 'Moscow',
                           'date': 'some_date',
                           'weather': 'some_weather'})
        self.client.force_authenticate(user=self.user)
        with patch('requests.get') as fake_get:
            fake_get.return_value = mocked_requests_get(data)
            response = self.client.get(self.url)
            self.assertEqual(response.data, json.loads(data))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, json.loads(data))

    @override_settings(CACHES=cache_params)
    def test_get_weather_city_with_bad_name_city(self):
        """Ensure that name of variables city and units must be correct"""
        self.url = 'http://0.0.0.0:8000/api/weather?cit=Moscow&unis=metric'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'BadRequest')


class WeatherViewCitiesTest(APITestCase):
    def setUp(self) -> None:
        """set up initial params"""
        self.date_first = '2021-06-24'
        self.date_last = '2021-06-25'
        self.user = User.objects.create_user(username='Test', password='Test')
        self.url = f'http://0.0.0.0:8000/api/' \
                   f'export_to_json?date_first={self.date_first}' \
                   f'&date_last={self.date_last}'
        WeatherCity.objects.create(city='Moscow',
                                   date='2021-06-24',
                                   weather='test')
        WeatherCity.objects.create(city='New York',
                                   date='2021-06-24',
                                   weather='test')

    def test_get_weather_cities_unauth(self):
        """Ensure that we cant get cities weather without auth"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(CACHES=cache_params)
    def test_get_weather_cities_auth(self):
        """"Ensure that we can get cities weather with auth"""
        weathers = WeatherCity.objects.filter(date__gte=self.date_first,
                                              date__lte=self.date_last)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         WeatherCitiesSerializer(weathers, many=True).data)

    @override_settings(CACHES=cache_params)
    def test_validation_date_error(self):
        """Ensure that we get bad request in case validation error"""
        self.date_first = 'some_date'
        self.url = f'http://0.0.0.0:8000/api/' \
                   f'export_to_json?date_begin={self.date_first}' \
                   f'&date_end={self.date_last}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'BadRequest')


class WeatherViewCitiesCSVTest(APITestCase):

    def setUp(self) -> None:
        """set up initial params"""
        self.date_first = '2021-06-24'
        self.date_last = '2021-06-25'
        self.user = User.objects.create_user(username='Test',
                                             password='Test')
        self.url = f'http://0.0.0.0:8000/api/' \
                   f'export_to_csv?date_begin={self.date_first}' \
                   f'&date_end={self.date_last}/'
        WeatherCity.objects.create(city='Moscow',
                                   date='2021-06-24',
                                   weather='test')
        WeatherCity.objects.create(city='New York',
                                   date='2021-06-24',
                                   weather='test')

    def test_get_weather_cities_unauth(self):
        """Ensure that we cant get cities weather without auth"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(CACHES=cache_params)
    def test_validation_date_error(self):
        """Ensure that we get validation error in case bad format date"""
        self.date_first = 'not date'
        self.url = f'http://0.0.0.0:8000/api/' \
                   f'export_to_csv?date_begin={self.date_first}' \
                   f'&date_end={self.date_last}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'BadRequest')

    @override_settings(CACHES=cache_params)
    def test_get_weather_cities_csv(self):
        """Ensure that we get information in case auth"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        weathers = WeatherCity.objects.filter(date__gte=self.date_first,
                                              date__lte=self.date_last)
        serializer = WeatherCitiesSerializer(weathers, many=True)
        data_from_csv = csv.DictReader(
            response.content.decode('utf-8').split('\r\n')[1:],
            fieldnames=['city', 'date', 'weather'])
        for data_ser, data_csv in zip(serializer.data, data_from_csv):
            self.assertEqual({"city": data_ser['city'],
                              "date": data_ser['date'],
                              'weather': data_ser['weather']}, data_csv)


class RootViewTest(APITestCase):
    def setUp(self) -> None:
        """initial set up"""
        self.url = 'http://0.0.0.0:8000/api/'
        self.data = {'docs': 'http://0.0.0.0:8000/api/docs',
                     'login': 'http://0.0.0.0:8000/api-auth/login'}

    def test_get_api_root(self):
        """ensure that we get right response"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.data)
