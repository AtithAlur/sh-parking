from django.utils.http import urlencode
from parking_rates.models import ParkingRate
from parking_rates.utils import (convert_to_reference_datetime,
                                 create_reference_start_and_end_datetime)
from psycopg2.extras import DateTimeTZRange
from rest_framework import status
from rest_framework.test import APITestCase


class RetrieveParkingPriceTestCase(APITestCase):
    def setUp(self):
        start_date, end_date = create_reference_start_and_end_datetime(
            'mon', '0200-0300', 'America/Chicago')
        ParkingRate.objects.create(
            time_range=DateTimeTZRange(convert_to_reference_datetime(
                start_date), convert_to_reference_datetime(end_date)),
            price='20.00')

    def test_parking_price(self):
        params = {
            'start_at': '2015-07-06T02:00:00-05:00',
            'end_at': '2015-07-06T02:30:00-05:00'
        }
        response = self.client.get('/apis/price?' + urlencode(params))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data, {'price': '20.00'})

    def test_timezone_parking_prices(self):
        params = {
            'start_at': '2015-07-06T13:30:00+06:30',
            'end_at': '2015-07-06T14:00:00+06:30'
        }
        response = self.client.get('/apis/price?' + urlencode(params))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data, {'price': '20.00'})

    def test_boundary_parking_price(self):
        start_at = '2015-07-06T02:00:00-05:00'
        end_at = '2015-07-06T03:00:00-05:00'
        response = self.client.get(
            f'/apis/price?start_at={start_at}&end_at={end_at}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data, {'price': '20.00'})

    def test_overlapping_time_range(self):
        start_date, end_date = create_reference_start_and_end_datetime(
            'mon', '0300-0600', 'America/Chicago')
        ParkingRate.objects.create(
            time_range=DateTimeTZRange(convert_to_reference_datetime(
                start_date), convert_to_reference_datetime(end_date)),
            price='22.00')
        start_at = '2015-07-06T02:00:00-05:00'
        end_at = '2015-07-06T04:00:00-05:00'
        response = self.client.get(
            f'/apis/price?start_at={start_at}&end_at={end_at}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.data
        self.assertEqual(data, {
            'statusCode': 404,
            'statusMessage': 'Not Found',
            'errorMessages': ['Unavailable']
        })

    def test_missing_parking_rate(self):
        start_at = '2015-07-06T02:00:00-05:00'
        end_at = '2015-07-06T04:00:00-05:00'
        response = self.client.get(
            f'/apis/price?start_at={start_at}&end_at={end_at}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.data
        self.assertEqual(data, {
            'statusCode': 404,
            'statusMessage': 'Not Found',
            'errorMessages': ['Unavailable']
        })

        start_at = '2015-07-06T01:00:00-05:00'
        end_at = '2015-07-06T03:00:00-05:00'
        response = self.client.get(
            f'/apis/price?start_at={start_at}&end_at={end_at}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.data
        self.assertEqual(data, {
            'statusCode': 404,
            'statusMessage': 'Not Found',
            'errorMessages': ['Unavailable']
        })

    def test_missing_start_at(self):
        response = self.client.get(
            '/apis/price?end_at=2015-07-01T07:30:00-05:00')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'statusCode': 400,
            'statusMessage': 'Bad Request',
            'errorMessages': ['Missing query parameter: start_at'],
        })

    def test_missing_end_at(self):
        response = self.client.get(
            '/apis/price?start_at=2015-07-01T07:30:00-05:00')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'statusCode': 400,
            'statusMessage': 'Bad Request',
            'errorMessages': ['Missing query parameter: end_at'],
        })

    def test_invalid_date_range(self):
        response = self.client.get(
            '/apis/price?start_at=2015-07-01T07:00:00-05:00&end_at=2015-07-02T07:30:00-05:00')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'statusCode': 400,
            'statusMessage': 'Bad Request',
            'errorMessages': ['Invalid date range'],
        })

    def test_invalid_date(self):
        response = self.client.get(
            '/apis/price?start_at=2015-07-017:00:00-05:00&end_at=2015-07-01T07:30:00-05:00')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'statusCode': 400,
            'statusMessage': 'Bad Request',
            'errorMessages': ["Invalid isoformat string: '2015-07-017:00:00-05:00'"],
        })
