from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ocr.views import (
    OCRAdvancedRunView,
    OCRAuditLogViewSet,
    OCRDocumentRunView,
    OCRJobViewSet,
    OCRKnowledgeBasePipelineRunViewSet,
    OCRPageResultViewSet,
    OCRResultViewSet,
    OrganizationOCRSettingsView,
)


router = DefaultRouter()
router.register(r'jobs', OCRJobViewSet, basename='ocr-job')
router.register(r'results', OCRResultViewSet, basename='ocr-result')
router.register(r'page-results', OCRPageResultViewSet, basename='ocr-page-result')
router.register(r'pipelines', OCRKnowledgeBasePipelineRunViewSet, basename='ocr-pipeline')
router.register(r'audit-logs', OCRAuditLogViewSet, basename='ocr-audit-log')

urlpatterns = [
    path('settings/', OrganizationOCRSettingsView.as_view(), name='ocr-settings'),
    path('documents/<uuid:document_id>/run/', OCRDocumentRunView.as_view(), name='ocr-document-run'),
    path('documents/<uuid:document_id>/advanced-run/', OCRAdvancedRunView.as_view(), name='ocr-document-advanced-run'),
    path('', include(router.urls)),
]
