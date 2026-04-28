from django.urls import include, path
from rest_framework.routers import DefaultRouter

from e_signature.views import (
    SignatureAuditTrailViewSet,
    SignaturePartyViewSet,
    SignatureProviderPlaceholderView,
    SignatureRequestViewSet,
    SignedDocumentViewSet,
)


router = DefaultRouter()
router.register(r'requests', SignatureRequestViewSet, basename='signature-request')
router.register(r'parties', SignaturePartyViewSet, basename='signature-party')
router.register(r'signed-documents', SignedDocumentViewSet, basename='signed-document')
router.register(r'audit-trail', SignatureAuditTrailViewSet, basename='signature-audit-trail')

urlpatterns = [
    path('provider-status/', SignatureProviderPlaceholderView.as_view()),
    path('', include(router.urls)),
]

