from django.test import TestCase
from parking_rates.models import ParkingRate
from psycopg2.extras import DateTimeTZRange
from datetime import datetime, timedelta
from zoneinfo._common import ZoneInfoNotFoundError
from django.db.utils import DataError, IntegrityError


class ParkingRateTestCase(TestCase):
    def setUp(self):
        current_datetime = datetime.now()
        time_range = DateTimeTZRange(
            current_datetime, (current_datetime + timedelta(hours=3)))
        ParkingRate.objects.create(price='30.00', time_range=time_range)

    def test_creates_parking_rates(self):
        parking_rates = ParkingRate.objects.all()
        self.assertEquals(len(parking_rates), 1)

        rate = parking_rates.first()
        self.assertAlmostEqual(rate.price, 30.00)
        self.assertIsNotNone(rate.uuid)
        self.assertIsNotNone(rate.created_at)
        self.assertIsNotNone(rate.updated_at)

    def test_limits_price_to_10_digits(self):
        current_datetime = datetime.now()
        time_range = DateTimeTZRange(
            current_datetime, (current_datetime + timedelta(hours=3)))
        with self.assertRaises(DataError):
            ParkingRate.objects.create(
                price=123456789.00, time_range=time_range)

    def test_time_range_overlap(self):
        current_datetime = datetime.now()
        time_range = DateTimeTZRange(
            current_datetime, (current_datetime + timedelta(hours=3)))
        with self.assertRaises(IntegrityError):
            ParkingRate.objects.create(price=789.00, time_range=time_range)
            ParkingRate.objects.create(price=9.00, time_range=time_range)

    def test_create_parking_rate(self):
        weekday = 'mon'
        details = {
            'times': '0100-0200',
            'tz': 'America/Chicago',
            'price': 200
        }
        rate = ParkingRate.create_parking_rate(details, weekday)
        self.assertEquals(rate.time_range.lower.isoformat(),
                          '2021-04-19T06:00:00+00:00')
        self.assertEquals(rate.time_range.upper.isoformat(),
                          '2021-04-19T07:00:00+00:00')

    def test_time_end_date_crossover(self):
        weekday = 'sun'
        details = {
            'times': '0100-2200',
            'tz': 'America/Chicago',
            'price': 200
        }
        rate = ParkingRate.create_parking_rate(details, weekday)
        self.assertEquals(rate.time_range.lower.isoformat(),
                          '2021-04-25T06:00:00+00:00')
        self.assertEquals(rate.time_range.upper.isoformat(),
                          '2021-04-26T03:00:00+00:00')

    def test_time_start_date_crossover(self):
        weekday = 'mon'
        details = {
            'times': '0100-2200',
            'tz': 'Asia/Calcutta',
            'price': 200
        }
        rate = ParkingRate.create_parking_rate(details, weekday)
        self.assertEquals(rate.time_range.lower.isoformat(),
                          '2021-04-18T19:30:00+00:00')
        self.assertEquals(rate.time_range.upper.isoformat(),
                          '2021-04-19T16:30:00+00:00')

    def test_invalid_timezone(self):
        weekday = 'mon'
        details = {
            'times': '0100-2200',
            'tz': 'Asia/invalid',
            'price': 200
        }
        with self.assertRaises(ZoneInfoNotFoundError):
            ParkingRate.create_parking_rate(details, weekday)

    def test_invalid_weekday(self):
        weekday = 'abcd'
        details = {
            'times': '0100-2200',
            'tz': 'Asia/invalid',
            'price': 200
        }
        with self.assertRaises(KeyError):
            ParkingRate.create_parking_rate(details, weekday)
