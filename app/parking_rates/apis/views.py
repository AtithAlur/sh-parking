from datetime import datetime

from parking_rates.apis.serializers import RetrieveParkingPriceSerializer
from parking_rates.models import ParkingRate
from parking_rates.utils import convert_to_reference_datetime
from psycopg2.extras import DateTimeTZRange
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import RetrieveAPIView


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

@method_decorator(
    name="get", # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_at",
                openapi.IN_QUERY,
                description="ISO-8601 Time stamp",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_at",
                openapi.IN_QUERY,
                description="ISO-8601 Time stamp",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class RetrieveParkingPrice(RetrieveAPIView):
    serializer_class = RetrieveParkingPriceSerializer

    def get_object(self):
        start_at_dt, end_at_dt = self.__fetch_and_validate_dates(self.request)
        if start_at_dt and end_at_dt:
            time_range = DateTimeTZRange(start_at_dt, end_at_dt)
            queryset = ParkingRate.objects.filter(
                time_range__contains=time_range)
            if len(queryset) == 1:
                return queryset.first()
            else:
                raise NotFound(detail=['Unavailable'])

    def __fetch_and_validate_dates(self, request):
        try:
            start_at = request.query_params.get('start_at')
            if not start_at:
                raise ValidationError('Missing query parameter: start_at')

            end_at = self.request.query_params.get('end_at')
            if not end_at:
                raise ValidationError('Missing query parameter: end_at')

            start_at_dt = datetime.fromisoformat(start_at)
            end_at_dt = datetime.fromisoformat(end_at)
            if start_at_dt.date() != end_at_dt.date():
                raise ValidationError('Invalid date range')
        except ValueError as e:
            raise ValidationError(e)
        return convert_to_reference_datetime(start_at_dt), convert_to_reference_datetime(end_at_dt)
