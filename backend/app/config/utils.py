from rest_framework.views import exception_handler
from rest_framework.response import Response as DRF_response
from rest_framework import status
from django.core import exceptions


def custom_exception_handler(exc, context):
    original_response = exception_handler(exc, context)
    if isinstance(exc, exceptions.ValidationError):
        data = exc.error_list
        return DRF_response(data=data, status=status.HTTP_400_BAD_REQUEST)
    return original_response
