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

            # Find values foe each element

            weather.value = data['value']
            # Get date in yyyy-dd format
            my_date = str(data['year']) + "-" + str(data['month'])
            # Convert date into yyyy-mm-dd to find range between two dates
            weather.date = str(datetime.strptime(my_date, '%Y-%m').date())
            weather.location = location
            weather.metrics = metric
            print("[+] Saving : " + weather.metrics + " for date " + str(weather.date))
            weather.save()

            # ============Or we can use=============
            # obj, created = Weather.objects.get_or_create(value=data['value'], location=location, metrics=metric,
            #                                              date=str(datetime.strptime(my_date, '%Y-%m').date()))

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
