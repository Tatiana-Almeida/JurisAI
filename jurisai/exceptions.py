from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            response.data = {
                'error': 'validation_error',
                'details': response.data,
            }
        elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
            response.data = {
                'error': 'authentication_failed',
                'details': response.data,
            }
        elif isinstance(exc, PermissionDenied):
            response.data = {
                'error': 'permission_denied',
                'details': response.data,
            }
        else:
            response.data = {
                'error': 'server_error',
                'details': response.data,
            }
    else:
        response = Response(
            {'error': 'server_error', 'details': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
