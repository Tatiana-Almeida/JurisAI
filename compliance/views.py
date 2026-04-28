from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from compliance.models import (
    AccessLog,
    DataConsent,
    DataDeletionRequest,
    DataExportRequest,
    DataRetentionPolicy,
    SensitiveDataFlag,
)
from compliance.serializers import (
    AccessLogSerializer,
    DataConsentSerializer,
    DataDeletionRequestSerializer,
    DataExportRequestSerializer,
    DataRetentionPolicySerializer,
    SensitiveDataFlagSerializer,
)
from jurisai.permissions import IsOrganizationMember


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class DataConsentViewSet(OrganizationFilteredViewSet):
    queryset = DataConsent.objects.select_related('organization', 'user').all()
    serializer_class = DataConsentSerializer


class DataRetentionPolicyViewSet(OrganizationFilteredViewSet):
    queryset = DataRetentionPolicy.objects.select_related('organization').all()
    serializer_class = DataRetentionPolicySerializer


class SensitiveDataFlagViewSet(OrganizationFilteredViewSet):
    queryset = SensitiveDataFlag.objects.select_related('organization').all()
    serializer_class = SensitiveDataFlagSerializer


class DataExportRequestViewSet(OrganizationFilteredViewSet):
    queryset = DataExportRequest.objects.select_related('organization', 'requested_by').all()
    serializer_class = DataExportRequestSerializer


class DataDeletionRequestViewSet(OrganizationFilteredViewSet):
    queryset = DataDeletionRequest.objects.select_related('organization', 'requested_by').all()
    serializer_class = DataDeletionRequestSerializer


class AccessLogViewSet(OrganizationFilteredViewSet):
    queryset = AccessLog.objects.select_related('organization', 'user').all()
    serializer_class = AccessLogSerializer

