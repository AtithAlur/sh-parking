import json
import os

from parking_rates.models import ParkingRate
from django.conf import settings


def run():
    print('############## Deleting ParkingRate #############')
    ParkingRate.objects.all().delete()
    print('############## Creating ParkingRate ###############')
    data = open(os.path.join(settings.BASE_DIR, 'data', 'parking_rates.json'))
    parking_rates = json.load(data)
    for details in parking_rates["rates"]:
        weekdays = details['days'].split(',')
        for weekday in weekdays:
            ParkingRate.create_parking_rate(details, weekday)
