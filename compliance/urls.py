from django.urls import include, path
from rest_framework.routers import DefaultRouter

from compliance.views import (
    AccessLogViewSet,
    DataConsentViewSet,
    DataDeletionRequestViewSet,
    DataExportRequestViewSet,
    DataRetentionPolicyViewSet,
    SensitiveDataFlagViewSet,
)


router = DefaultRouter()
router.register(r'consents', DataConsentViewSet, basename='compliance-consent')
router.register(r'retention-policies', DataRetentionPolicyViewSet, basename='compliance-retention-policy')
router.register(r'sensitive-data-flags', SensitiveDataFlagViewSet, basename='compliance-sensitive-data-flag')
router.register(r'export-requests', DataExportRequestViewSet, basename='compliance-export-request')
router.register(r'deletion-requests', DataDeletionRequestViewSet, basename='compliance-deletion-request')
router.register(r'access-logs', AccessLogViewSet, basename='compliance-access-log')

urlpatterns = [
    path('', include(router.urls)),
]

