import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from requests import ConnectionError


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, Exception):

        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        return JsonResponse({'message': str(exc)}, status=503)
        # returns a JsonResponse
        # return JsonResponse(err_data, safe=False, status=503)

    if response is not None:
        response.data['status_code'] = response.status_code

    # returns response as handled normally by the framework
    return response