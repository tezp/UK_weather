import sqlite3
from _datetime import datetime

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from weather.models import Weather
from weather.serializers import WeatherSerializer


class NormalWeatherListAPI(APIView):
    """
    This class is used to create REST API for UK_Weather. It does not used django rest framework.
    """
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        """
        HTTP GET method to fetch requested data.
        It uses arguments - start_date, end_date, metric, location
        Request Format:
        http://127.0.0.1:8000/getjsondata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall
        or
        curl -X GET -i 'http://127.0.0.1:8000/getjsondata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall'
        :param request:
        :return: Json data
        """
        if self.request.GET:
            try:
                # Get the query parameters
                start_date = self.request.GET.get("start_date")
                end_date = self.request.GET.get("end_date")
                metric = self.request.GET.get("metric")
                location = self.request.GET.get("location")
                start_date = str(datetime.strptime(start_date, '%Y-%m').date())
                end_date = str(datetime.strptime(end_date, '%Y-%m').date())

                # Check the query parameters
                if (start_date or end_date or metric or location) is not None:
                    weather = Weather.objects.filter(location=location, metrics=metric,
                                                     date__range=[start_date, end_date]
                                                     )
                    return_data = {}
                    for w in weather:
                        # We have data with yyyy-mm-dd format. Convert it into yyyy-dd format by splitting
                        year_month_date = str(w.date)
                        year_month = year_month_date.split("-")
                        year_month = "-".join(year_month[:-1])
                        return_data[str(year_month)] = str(w.value)
                    return Response(return_data)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            except sqlite3.Error as exception:
                print("Exception while fetching data")
                return status.HTTP_400_BAD_REQUEST


class WeatherListAPI(ListAPIView):
    """
    This class is used to create REST API for UK_Weather. It extends  django rest_framework's ListAPIView
    """
    serializer_class = WeatherSerializer

    def get_queryset(self):
        """
        HTTP GET method to fetch requested data.
        It uses arguments - start_date, end_date, metric, location
        Request Format:
        http://127.0.0.1:8000/getserialiseddata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall
        or
        curl -X GET -i 'http://127.0.0.1:8000/getserialiseddata/?start_date=2010-01&end_date=2010-12&location=England&metric=Rainfall'
        :return: Serialized data

        """
        if self.request.GET:
            try:
                # fetch all data from databse

                start_date = self.request.GET.get("start_date")
                end_date = self.request.GET.get("end_date")
                metric = self.request.GET.get("metric")
                location = self.request.GET.get("location")
                start_date = str(datetime.strptime(start_date, '%Y-%m').date())
                end_date = str(datetime.strptime(end_date, '%Y-%m').date())
                if (start_date or end_date or metric or location) is not None:
                    weather = Weather.objects.filter(location=location, metrics=metric,
                                                     date__range=[start_date, end_date]
                                                     )
                    return weather
                else:
                    return status.HTTP_400_BAD_REQUEST
            except sqlite3.Error as exception:
                print("Exception while fetching data")
                return status.HTTP_400_BAD_REQUEST
