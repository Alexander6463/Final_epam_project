from rest_framework import serializers

from .models import WeatherCity, TopCities
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class WeatherCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ['city', 'date', 'weather']


class TopCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopCities
        fields = ['city']
