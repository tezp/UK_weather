from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from weather.models import Weather


class TestWeatherModel(TestCase):

    def setUp(self):
        print("Testing Model in Weather App")
        Weather.objects.create(location='India', metrics='Rainfall', value=23.3, date='2018-06-01')
        Weather.objects.create(location='India', metrics='Rainfall', value=19.7, date='2018-07-01')

    def test_weather(self):
        weather1 = Weather.objects.get(location="India", metrics='Rainfall', date='2018-06-01')
        weather2 = Weather.objects.get(location="India", metrics='Rainfall', date='2018-07-01')
        self.assertEqual(weather1.value, 23.3)
        self.assertEqual(weather2.value, 19.7)
