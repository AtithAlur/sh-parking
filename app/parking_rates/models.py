import uuid

from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models
from parking_rates.utils import create_reference_start_and_end_datetime
from psycopg2.extras import DateTimeTZRange


class ParkingRate(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time_range = DateTimeRangeField(unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_parking_rate(cls, details, weekday):
        start_date, end_date = create_reference_start_and_end_datetime(
            weekday, details["times"], details["tz"])
        time_range = DateTimeTZRange(start_date, end_date)
        return ParkingRate.objects.create(price=details["price"], time_range=time_range)
