from django.db.utils import IntegrityError
from parking_rates.apis.serializers import (ListParkingRatesSerializer,
                                            UpdateParkingPriceSerializer)
from parking_rates.models import ParkingRate
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, UpdateAPIView

class ListParkingRatesView(ListAPIView):
    queryset = ParkingRate.objects.all()
    serializer_class = ListParkingRatesSerializer


class UpdateParkingRatesView(UpdateAPIView):
    queryset = ParkingRate.objects.all()
    serializer_class = UpdateParkingPriceSerializer

    def get_object(self):
        return None

    def perform_update(self, serializer):
        try:
            for details in serializer.data['rates']:
                weekdays = details['days'].split(',')
                for weekday in weekdays:
                    ParkingRate.create_parking_rate(details, weekday)
        except IntegrityError:
            raise ValidationError('Time range overlap with existing entry')
