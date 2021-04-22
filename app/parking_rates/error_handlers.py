from parking_rates.utils import error_message
from rest_framework.views import exception_handler


def apis_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        error_details = {
            'status_code': response.status_code,
            'status_message': response.status_text,
            'error_messages': exc.detail
        }
        response.data = error_message(error_details)
    return response
