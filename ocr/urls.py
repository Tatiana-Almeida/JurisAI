from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ocr.views import OCRDocumentRunView, OCRJobViewSet, OCRResultViewSet


router = DefaultRouter()
router.register(r'jobs', OCRJobViewSet, basename='ocr-job')
router.register(r'results', OCRResultViewSet, basename='ocr-result')

urlpatterns = [
    path('documents/<uuid:document_id>/run/', OCRDocumentRunView.as_view(), name='ocr-document-run'),
    path('', include(router.urls)),
]
