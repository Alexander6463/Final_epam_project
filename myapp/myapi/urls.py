from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from .views import WeatherView, WeatherViewCities, \
    WeatherViewCitiesCSV, UserRegistration, Root

schema_view = get_schema_view(title='Weather API')
descr = 'A web API that viewing weather in cities'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', Root.as_view()),
    path('docs/', include_docs_urls(title='Weather API', description=descr)),
    path('schema/', schema_view),
    path('user/', UserRegistration.as_view()),
    path('weather', WeatherView.as_view()),
    path('export_to_json', WeatherViewCities.as_view()),
    path('export_to_csv', WeatherViewCitiesCSV.as_view()),
]
