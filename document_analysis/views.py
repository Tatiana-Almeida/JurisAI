from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from document_analysis.models import (
    DeadlineExtractionRun,
    DocumentComparison,
    DocumentDifference,
    ExtractedDeadlineSuggestion,
)
from document_analysis.serializers import (
    DeadlineExtractionRunSerializer,
    DocumentComparisonSerializer,
    DocumentDifferenceSerializer,
    ExtractedDeadlineSuggestionSerializer,
)
from jurisai.permissions import IsOrganizationMember


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class DocumentComparisonViewSet(OrganizationFilteredViewSet):
    queryset = DocumentComparison.objects.select_related('organization', 'left_document', 'right_document', 'requested_by').all()
    serializer_class = DocumentComparisonSerializer


class DocumentDifferenceViewSet(OrganizationFilteredViewSet):
    queryset = DocumentDifference.objects.select_related('organization', 'comparison').all()
    serializer_class = DocumentDifferenceSerializer


class DeadlineExtractionRunViewSet(OrganizationFilteredViewSet):
    queryset = DeadlineExtractionRun.objects.select_related('organization', 'document', 'requested_by').all()
    serializer_class = DeadlineExtractionRunSerializer


class ExtractedDeadlineSuggestionViewSet(OrganizationFilteredViewSet):
    queryset = ExtractedDeadlineSuggestion.objects.select_related('organization', 'extraction_run').all()
    serializer_class = ExtractedDeadlineSuggestionSerializer


class AnalysisPlaceholderView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response({'status': 'not_implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

