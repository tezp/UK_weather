import json
import urllib.request

from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from django.test import TestCase
from django.test import Client


class TestWeatherView(TestCase):

    def setUp(self):
        print("Testing Views in Weather App")

    def test_json_data_status(self):
        """ Test json response"""
        url = 'http://127.0.0.1:8000/getjsondata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall'
        response = urllib.request.urlopen(url)
        # we get response like : {"2010-01":"67.5","2010-02":"73.8","2010-03":"58.7","2010-04":"24.5",...}
        json_data_or_dict = json.loads(response.read())
        # Get the first element : {"2010-01":"67.5"}
        first_element = next(iter(json_data_or_dict.items()))
        # Get the value
        value = first_element[1]
        self.assertEqual(response.status, 200)
        self.assertEqual(float(value), 67.5)

    def test_serialised_data_status(self):
        """Test serialised response"""
        url = 'http://127.0.0.1:8000/getserialiseddata/?start_date=2010-01&end_date=2010-12&location=' \
              'England&metric=Rainfall'
        response = urllib.request.urlopen(url)
        # We get response like : [{"2010-01":"67.5"},{"2010-02":"73.8"},{"2010-03":"58.7"},{"2010-04":"24.5"}]
        list_of_dict = json.loads(response.read())
        # Get the first element : {"2010-01":"67.5"}
        first_element = next(iter(list_of_dict[0].items()))
        # Get the value
        value = first_element[1]
        self.assertEqual(response.status, 200)
        self.assertEqual(float(value), 67.5)
