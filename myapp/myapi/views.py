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
from .services import MyRequest, Validation, WorkWithDatabase
from .serializers import WeatherCitiesSerializer, UserSerializer


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class WeatherView(APIView):
    """This view automatically generate information
    about city."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """Give information about weather in the city.
        Use units=metric for Celsius and units=imperial for Fahrenheit"""
        city = self.kwargs.get('city_name')
        units = self.kwargs.get('units_name')
        weather = MyRequest().get_weather_city(city, units)
        if weather:
            return Response({"weather": weather}, status=status.HTTP_200_OK)
        else:
            return Response('Bad request', status=status.HTTP_400_BAD_REQUEST)


class WeatherViewCities(APIView):
    """This view automatically generate information
    about 100 cities in json ordered by population"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """Give information about 100 top cities weather
        between date_first and date_last in json format.
        Use date_first and date_last in format 'YYYY-MM-DD H:M:'"""
        date_begin = self.kwargs.get('date_first')
        date_end = self.kwargs.get('date_last')
        if Validation().validate_date(date_begin) \
                and Validation().validate_date(date_end):
            weathers = WeatherCity.objects.\
                filter(date__gte=date_begin, date__lte=date_end)
            serializer = WeatherCitiesSerializer(weathers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = 'ValidationError, Use date_first ' \
                         'and date_last in format YYYY-MM-DD H:M'
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)


class WeatherViewCitiesCSV(APIView):
    """This view automatically generate information
        about 100 cities in csv file ordered by population"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """"Give information about 100 top cities weather
        between date_first and date_last in csv file format.
        Use date_first and date_last in format 'YYYY-MM-DD H:M:'"""
        date_begin = self.kwargs.get('date_first')
        date_end = self.kwargs.get('date_last')
        valid = Validation()
        db = WorkWithDatabase()
        if valid.validate_date(date_begin) \
                and valid.validate_date(date_end):
            return db.export_to_csv_from_database(date_begin, date_end)
        else:
            serializer = 'ValidationError, Use date_first ' \
                         'and date_last in format YYYY-MM-DD H:M'
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)


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
