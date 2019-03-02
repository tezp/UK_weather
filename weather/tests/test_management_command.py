import json
import urllib.request

from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class TestCommands(TestCase):

    def setUp(self):
        print("Testing Management command in Weather App")

    def test_custom_command(self):
        """Test custom command."""
        try:
            out = StringIO()
            call_command('fetch_json_and_save', '-u',
                         'https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json',
                         stdout=out)
            response = urllib.request.urlopen(
                'https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json')
            response_data = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertEqual(len(response_data), 1296)
        except Exception as e:
            print("Something went wrong.\nReason:", str(e))
