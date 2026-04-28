from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ocr.views import OCRJobViewSet, OCRResultViewSet, OCRRunPlaceholderView


router = DefaultRouter()
router.register(r'jobs', OCRJobViewSet, basename='ocr-job')
router.register(r'results', OCRResultViewSet, basename='ocr-result')

urlpatterns = [
    path('run/', OCRRunPlaceholderView.as_view()),
    path('', include(router.urls)),
]

