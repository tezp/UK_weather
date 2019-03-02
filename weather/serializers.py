from rest_framework import serializers
from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('date', 'value')

    def to_representation(self, instance):
        """
        Change default representation of serialised data
        :param instance:
        :return:
        """
        identifiers = dict()
        identifiers['date'] = instance.date
        identifiers['value'] = instance.value
        year_month_date = str(identifiers['date'])
        year_month = year_month_date.split("-")
        identifiers['date'] = "-".join(year_month[:-1])
        representation = {
            str(identifiers['date']): str(identifiers['value'])
        }
        return representation
