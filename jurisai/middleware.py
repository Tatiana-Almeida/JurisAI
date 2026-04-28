import threading
from django.utils.deprecation import MiddlewareMixin

_thread_local = threading.local()

def get_current_request():
    return getattr(_thread_local, 'request', None)

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.organization = getattr(request.user, 'organization', None)
        _thread_local.request = request

    def process_response(self, request, response):
        if hasattr(_thread_local, 'request'):
            del _thread_local.request
        return response
