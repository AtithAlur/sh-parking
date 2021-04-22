from parking_rates.models import ParkingRate
from rest_framework import serializers


class ListParkingRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRate
        fields = ['price', 'uuid', 'time_range']


class RetrieveParkingPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRate
        fields = ['price']


class ParkingRateField(serializers.Serializer):
    days = serializers.CharField()
    times = serializers.CharField()
    tz = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class UpdateParkingPriceSerializer(serializers.Serializer):
    rates = ParkingRateField(many=True)
