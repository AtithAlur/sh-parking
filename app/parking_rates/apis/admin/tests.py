from parking_rates.models import ParkingRate
from parking_rates.utils import (convert_to_reference_datetime,
                                 create_reference_start_and_end_datetime)
from psycopg2.extras import DateTimeTZRange
from rest_framework import status
from rest_framework.test import APITestCase


class ListParkingRatesViewTestCase(APITestCase):
    def setUp(self):
        start_date, end_date = create_reference_start_and_end_datetime(
            'mon', '0200-0300', 'America/Chicago')
        ParkingRate.objects.create(
            time_range=DateTimeTZRange(convert_to_reference_datetime(
                start_date), convert_to_reference_datetime(end_date)),
            price='20.00')

    def test_list_parking_rates(self):
        response = self.client.get('/apis/admin/rates')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateParkingRatesViewTestCase(APITestCase):
    def setUp(self):
        start_date, end_date = create_reference_start_and_end_datetime(
            'mon', '0200-0300', 'America/Chicago')
        ParkingRate.objects.create(
            time_range=DateTimeTZRange(convert_to_reference_datetime(
                start_date), convert_to_reference_datetime(end_date)),
            price='20.00')

    def test_update_parking_price(self):
        data = {
            "rates": [
                {
                    "days": "mon,tues,thurs",
                    "times": "0900-2100",
                    "tz": "America/Chicago",
                    "price": 1500
                }
            ]
        }
        response = self.client.put(
            '/apis/admin/rates/update', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        weekdays = "mon,tues,thurs".split(',')
        for weekday in weekdays:
            start_date, end_date = create_reference_start_and_end_datetime(
                weekday, '0900-2100', 'America/Chicago')
            rates = ParkingRate.objects.filter(
                time_range=DateTimeTZRange(start_date, end_date))
            self.assertEquals(len(rates), 1)

    def test_update_parking_price_overlap(self):
        data = {
            "rates": [
                {
                    "days": "mon,tues,thurs",
                    "times": "0900-2100",
                    "tz": "America/Chicago",
                    "price": 1500
                }
            ]
        }
        self.client.put('/apis/admin/rates/update', data, format='json')
        response = self.client.put(
            '/apis/admin/rates/update', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.data
        self.assertEqual(data, {
            'statusCode': 400,
            'statusMessage': 'Bad Request',
            'errorMessages': ['Time range overlap with existing entry']
        })
