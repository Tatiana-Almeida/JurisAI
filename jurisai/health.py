from django.http import JsonResponse


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'jurisai', 'version': 'v0.11.0'})
