from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from documents.models import Document
from jurisai.permissions import IsOrganizationMember
from ocr.models import OCRJob, OCRResult
from ocr.serializers import (
    ApplyOCRResultSerializer,
    OCRJobSerializer,
    OCRResultSerializer,
    RunOCRSerializer,
)
from ocr.services import run_ocr_for_document, update_document_content_from_ocr


class OrganizationFilteredReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        queryset = super().get_queryset()
        return queryset.filter(organization=organization) if organization else queryset.none()


class OCRJobViewSet(OrganizationFilteredReadOnlyViewSet):
    queryset = OCRJob.objects.select_related('organization', 'document', 'requested_by').all()
    serializer_class = OCRJobSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_id', 'status', 'extraction_method']
    ordering_fields = ['created_at', 'started_at', 'finished_at']


class OCRResultViewSet(OrganizationFilteredReadOnlyViewSet):
    queryset = OCRResult.objects.select_related('organization', 'job', 'document').all()
    serializer_class = OCRResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_id', 'job_id']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'], url_path='apply-to-document')
    def apply_to_document(self, request, pk=None):
        result = self.get_object()
        serializer = ApplyOCRResultSerializer(
            data=request.data,
            context={'request': request, 'result_id': str(result.id)},
        )
        serializer.is_valid(raise_exception=True)

        update_document_content_from_ocr(result.document, result.extracted_text, user=request.user)
        result.metadata['content_updated'] = True
        result.save(update_fields=['metadata'])

        return Response(
            {
                'status': 'applied',
                'document_id': str(result.document.id),
                'result_id': str(result.id),
                'char_count': result.char_count,
            },
            status=status.HTTP_200_OK,
        )


class OCRDocumentRunView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    serializer_class = RunOCRSerializer

    def post(self, request, document_id):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'document_id': document_id},
        )
        serializer.is_valid(raise_exception=True)

        document = Document.objects.filter(
            pk=serializer.validated_data['document_id'],
            organization=request.user.organization,
        ).select_related('organization').first()
        if document is None:
            return Response(
                {'document_id': ['Este recurso nao pertence a organizacao atual.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job, result = run_ocr_for_document(
            document=document,
            user=request.user,
            update_document_content=serializer.validated_data['update_document_content'],
        )
        payload = {
            'job': OCRJobSerializer(job).data,
            'result': OCRResultSerializer(result).data if result else None,
        }
        return Response(payload, status=status.HTTP_200_OK)
