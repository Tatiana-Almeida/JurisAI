from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from documents.models import Document
from jurisai.permissions import IsOrganizationMember
from knowledge_base.models import KnowledgeBase
from ocr.models import OCRAuditLog, OCRJob, OCRKnowledgeBasePipelineRun, OCRPageResult, OCRResult
from ocr.serializers import (
    AdvancedOCRRunSerializer,
    ApplyOCRResultSerializer,
    OCRAuditLogSerializer,
    OCRJobSerializer,
    OCRKnowledgeBasePipelineRunSerializer,
    OCRPageResultSerializer,
    OCRResultSerializer,
    OCRSettingsSerializer,
    RunOCRKnowledgeBasePipelineSerializer,
    RunOCRSerializer,
)
from ocr.services import (
    get_ocr_settings,
    run_advanced_ocr,
    run_ocr_for_document,
    run_ocr_to_knowledge_base_pipeline,
    update_document_content_from_ocr,
)


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

    @action(detail=True, methods=['get'], url_path='pages')
    def pages(self, request, pk=None):
        result = self.get_object()
        queryset = OCRPageResult.objects.filter(
            organization=request.user.organization,
            ocr_result=result,
        ).order_by('page_number', 'created_at', 'id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OCRPageResultSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OCRPageResultSerializer(queryset, many=True)
        return Response(serializer.data)

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


class OCRKnowledgeBasePipelineRunViewSet(OrganizationFilteredReadOnlyViewSet):
    queryset = OCRKnowledgeBasePipelineRun.objects.select_related(
        'organization',
        'document',
        'knowledge_base',
        'ocr_job',
        'ocr_result',
        'knowledge_document',
        'indexing_job',
        'created_by',
    ).all()
    serializer_class = OCRKnowledgeBasePipelineRunSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_id', 'knowledge_base_id', 'status', 'step']
    ordering_fields = ['created_at', 'started_at', 'finished_at']

    @action(detail=False, methods=['post'], url_path='knowledge-base')
    def run_knowledge_base_pipeline(self, request):
        serializer = RunOCRKnowledgeBasePipelineSerializer(
            data=request.data,
            context={'request': request},
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

        knowledge_base = KnowledgeBase.objects.filter(
            pk=serializer.validated_data['knowledge_base_id'],
            organization=request.user.organization,
        ).select_related('organization').first()
        if knowledge_base is None:
            return Response(
                {'knowledge_base_id': ['Este recurso nao pertence a organizacao atual.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pipeline_run = run_ocr_to_knowledge_base_pipeline(
            document=document,
            knowledge_base=knowledge_base,
            user=request.user,
            update_document_content=serializer.validated_data['update_document_content'],
        )
        response_status = status.HTTP_200_OK if pipeline_run.status == 'completed' else status.HTTP_400_BAD_REQUEST
        return Response(OCRKnowledgeBasePipelineRunSerializer(pipeline_run).data, status=response_status)


class OrganizationOCRSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = OCRSettingsSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_object(self):
        organization = getattr(self.request.user, 'organization', None)
        return get_ocr_settings(organization)

    def update(self, request, *args, **kwargs):
        if getattr(request.user, 'role', None) != 'admin':
            return Response(
                {'detail': 'Apenas administradores podem atualizar as configuracoes de OCR.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


class OCRAuditLogViewSet(OrganizationFilteredReadOnlyViewSet):
    queryset = OCRAuditLog.objects.select_related(
        'organization',
        'document',
        'ocr_job',
        'created_by',
    ).all()
    serializer_class = OCRAuditLogSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_id', 'ocr_job_id', 'action', 'status', 'reason', 'provider', 'mode']
    ordering_fields = ['created_at']


class OCRPageResultViewSet(OrganizationFilteredReadOnlyViewSet):
    queryset = OCRPageResult.objects.select_related(
        'organization',
        'ocr_result',
        'ocr_job',
        'document',
    ).all()
    serializer_class = OCRPageResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_id', 'ocr_job_id', 'ocr_result_id', 'status', 'page_number']
    ordering_fields = ['created_at', 'page_number']


class OCRAdvancedRunView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    serializer_class = AdvancedOCRRunSerializer

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

        result = run_advanced_ocr(
            document=document,
            user=request.user,
            mode=serializer.validated_data['mode'],
        )
        return Response(
            {
                'status': result['status'],
                'reason': result['reason'],
                'job': OCRJobSerializer(result['job']).data,
                'audit_log': OCRAuditLogSerializer(result['audit_log']).data,
                'result': OCRResultSerializer(result['result']).data if result.get('result') else None,
            },
            status=status.HTTP_200_OK,
        )
