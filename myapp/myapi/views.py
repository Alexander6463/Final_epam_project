from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherCity
from .services import MyRequest, export_to_csv_from_database
from .serializers import WeatherCitiesSerializer, \
    UserSerializer, DateTimeSerializer, CityWeatherSerializer


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class WeatherView(APIView):
    """This view automatically generate information
    about city."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """Give information about weather in the city.
        Use units=metric for Celsius and units=imperial for Fahrenheit
        example request: weather?city=Moscow&units=metric"""
        if 'city' in request.GET and 'units' in request.GET:
            serializer = CityWeatherSerializer(
                data={'city': request.GET['city'],
                      'units': request.GET['units']})
            if serializer.is_valid():
                weather = MyRequest().get_weather_city(
                    serializer.data['city'],
                    serializer.data['units'])
                if weather:
                    return Response(weather, status=status.HTTP_200_OK)
        return Response('BadRequest', status=status.HTTP_400_BAD_REQUEST)


class WeatherViewCities(APIView):
    """This view automatically generate information
    about 100 cities in json ordered by population"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """Give information about 100 top cities weather
        between date_first and date_last in json format.
        Use date_first and date_last in format 'YYYY-MM-DD'
        example request:
        export_to_json?date_first=2021-06-15&date_last=2021-06-29"""
        if 'date_first' in request.GET and 'date_last' in request.GET:
            serializer = DateTimeSerializer(
                data={'date_first': request.GET['date_first'],
                      'date_last': request.GET['date_last']})
            if serializer.is_valid():
                weathers = WeatherCity.objects.filter(
                    date__gte=serializer.data['date_first'],
                    date__lte=serializer.data['date_last'])
                serializer = WeatherCitiesSerializer(weathers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('BadRequest', status=status.HTTP_400_BAD_REQUEST)


class WeatherViewCitiesCSV(APIView):
    """This view automatically generate information
        about 100 cities in csv file ordered by population"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """"Give information about 100 top cities weather
        between date_first and date_last in csv file format.
        Use date_first and date_last in format 'YYYY-MM-DD
        example request:
        export_to_csv?date_first=2021-06-15&date_last=2021-06-29'"""
        if 'date_first' in request.GET and 'date_last' in request.GET:
            serializer = DateTimeSerializer(
                data={'date_first': request.GET['date_first'],
                      'date_last': request.GET['date_last']})
            if serializer.is_valid():
                return export_to_csv_from_database(
                    serializer.data['date_first'],
                    serializer.data['date_last'])
        return Response('BadRequest', status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    """For registration use username and password"""

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Root(APIView):
    """My API ROOT"""
    def get(self, request, format=None):
        return Response({'docs': 'http://0.0.0.0:8000/api/docs',
                         'login': 'http://0.0.0.0:8000/api-auth/login'})
