from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from jurisai.permissions import IsOrganizationMember
from ocr.models import OCRJob, OCRResult
from ocr.serializers import OCRJobSerializer, OCRResultSerializer


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class OCRJobViewSet(OrganizationFilteredViewSet):
    queryset = OCRJob.objects.select_related('organization', 'document', 'requested_by').all()
    serializer_class = OCRJobSerializer


class OCRResultViewSet(OrganizationFilteredViewSet):
    queryset = OCRResult.objects.select_related('organization', 'job').all()
    serializer_class = OCRResultSerializer


class OCRRunPlaceholderView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        return Response({'status': 'not_implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

