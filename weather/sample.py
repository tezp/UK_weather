import json
import urllib.request

#
# response = urllib.request.urlopen(
#     'https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json')
# response1 = json.loads(response.read())
# print((response1[0]['year']))
#
#
# def setUp(self):
#     print("Testing Views in Weather App")
#
#
# def test_request_status(self):
#     response = urllib.request.urlopen(
#         'https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json')
#     response1 = json.loads(response.read())
#     self.assertEqual(response1[0]['value'], 82.9, 'Working fine')


url = 'http://127.0.0.1:8000/getjsondata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall'
# response = client.get(
#     'http://127.0.0.1:8000/getjsondata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall')
# # {'start_date': '2010-01', 'end_date': '2010-12', 'location': 'England', 'metric': 'Rainfall'})

# response = urllib.request.urlopen(url)
# json_data = json.loads(response.read())
#
# # response1 = json.loads(response.read())
# print(json_data)
# for data in json_data:
#     n = float(data['value'])
#     print(n)
# di = {'2010-01': '67.5', '2010-02': '73.8', '2010-03': '58.7', '2010-04': '24.5', '2010-05': '29.5', '2010-06': '36.6',
#       '2010-07': '61.1', '2010-08': '97.3', '2010-09': '78.6', '2010-10': '73.2', '2010-11': '91.4', '2010-12': '35.1'}
# tp = next(iter(di.items()))[1]
# print(tp)



from datetime import datetime
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from weather.models import Weather
import json
import urllib.request
import time
import re


class Command(BaseCommand):
    """
    Usage of command :
    python3 manage.py fetch_json_and_save -u https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json
    """
    help = 'Saves Json data'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--url', type=str,
                            help="""URL which will fetch json files for all 
                            locations and metrics, parse and store them in the Django models.""")

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        is_saved = save(str(url))
        if is_saved:
            self.stdout.write(self.style.SUCCESS('Successfully saved data into database.'))


def save(url):
    """
    Saves Json data into database
    :param url:
    :return:
    """
    try:
        metric, location, json_data = get_data_from_url(url)
        print("[+] Saving JSON into database")
        start = time.time()
        for data in json_data:
            weather = Weather()
            weather.value = data['value']
            my_date = str(data['year']) + "-" + str(data['month'])
            weather.date = str(datetime.strptime(my_date, '%Y-%m').date())
            weather.location = location
            weather.metrics = metric
            print("[+] Saving : " + weather.metrics + " for date " + str(weather.date))
            weather.save()
        print("[+] JSON data saved into database")
        print("Time required to save data : ", time.time() - start, " Seconds")
        return True

    except IntegrityError as e:
        print("Exception while saving data into database: ")
        print("Reason : " + "Data already available")
        return False
    except Exception as e:
        return False


def get_data_from_url(url):
    """
    Returns Json data from URL and parsed location, metric from URL
    :param url:
    :return: metric, location, json_data
    """
    split_url = re.findall(r"[\w']+", url)
    metric = split_url[-3]
    location = split_url[-2]
    try:
        start = time.time()
        print("[+] Fetching JSON from url : " + url)
        response = urllib.request.urlopen(url)
        json_data = json.loads(response.read())
        print("[+] JSON fetched from url : " + url)
        print("Time required to fetch data : ", time.time() - start, " Seconds")
        return metric, location, json_data
    except urllib.request.HTTPError  as exception:
        print("Exception while fetching data from url : " + url)
        print("Reason : " + str(exception))
    except Exception  as exception:
        print("Exception while fetching data from url : " + url)
        print("Reason : " + str(exception))

