from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone

from parking_rates.constants import WEEKDAYS_MAPPING

# This is a reference datetime we use to compare and store in the DB
REFERENCE_DATE = datetime.fromisoformat('2021-04-19T00:00:00-00:00')

"""
  Description: Converts the input date information to the reference UTC datetime
  Args:
    weekday_str: Short weekday string. Ex: 'mon', 'tue'
    hours_str: Start and end hours. Formate 'HHMM-HHMM'
    tzone: TZ Database name. Ex: 'America/Chicago'
  Retruns: start_date and end_date datetime
"""


def create_reference_start_and_end_datetime(weekday_str, hours_str, tzone):
    weekday = WEEKDAYS_MAPPING[weekday_str]
    start_hour, end_hour = hours_str.split('-')
    tzinfo = ZoneInfo(tzone)
    if weekday is not None and start_hour is not None and end_hour is not None and tzinfo is not None:
        start_date = (REFERENCE_DATE + timedelta(days=weekday)).replace(hour=int(start_hour[0:2]),
                                                                        minute=int(start_hour[2:4]), second=0, microsecond=0, tzinfo=tzinfo).astimezone(timezone.utc)
        end_date = (REFERENCE_DATE + timedelta(days=weekday)).replace(hour=int(end_hour[0:2]),
                                                                      minute=int(end_hour[2:4]), second=0, microsecond=0, tzinfo=tzinfo).astimezone(timezone.utc)
        return start_date, end_date


"""
  Description: Converts the input datetime to reference datetime in UTC
  Args:
    date: datetime to be converted
  Returns: Converted reference datetime in UTC
"""


def convert_to_reference_datetime(date):
    if date is not None:
        reference_date = (REFERENCE_DATE + timedelta(days=date.weekday())).replace(hour=date.hour,
                                                                                   minute=date.minute, second=date.second, microsecond=0, tzinfo=date.tzinfo).astimezone(timezone.utc)
        return reference_date


def error_message(error_details):
    return {
        'statusCode': error_details['status_code'],
        'statusMessage': error_details['status_message'],
        'errorMessages': error_details['error_messages'],
    }
