from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from business_intelligence.models import MetricSnapshot, ReportDefinition, SavedReport
from business_intelligence.serializers import MetricSnapshotSerializer, ReportDefinitionSerializer, SavedReportSerializer
from jurisai.permissions import IsOrganizationMember


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class ReportDefinitionViewSet(OrganizationFilteredViewSet):
    queryset = ReportDefinition.objects.select_related('organization').all()
    serializer_class = ReportDefinitionSerializer


class SavedReportViewSet(OrganizationFilteredViewSet):
    queryset = SavedReport.objects.select_related('organization', 'report_definition', 'saved_by').all()
    serializer_class = SavedReportSerializer


class MetricSnapshotViewSet(OrganizationFilteredViewSet):
    queryset = MetricSnapshot.objects.select_related('organization').all()
    serializer_class = MetricSnapshotSerializer

