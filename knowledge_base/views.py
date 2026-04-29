from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max

from documents.models import Document
from jurisai.permissions import IsOrganizationMember
from knowledge_base.models import (
    DocumentChunk,
    EmbeddingAuditLog,
    IndexingJob,
    KnowledgeBase,
    KnowledgeDocument,
    RAGSettings,
    RetrievalQuery,
)
from knowledge_base.serializers import (
    DocumentChunkSerializer,
    EmbeddingAuditLogSerializer,
    IndexDocumentSerializer,
    IndexingJobSerializer,
    KnowledgeAskSerializer,
    KnowledgeBaseSerializer,
    KnowledgeDocumentSerializer,
    KnowledgeSearchSerializer,
    PrepareEmbeddingsSerializer,
    RAGSettingsSerializer,
    ReindexDocumentSerializer,
    RetrievalQuerySerializer,
)
from knowledge_base.services import (
    build_grounded_answer,
    generate_embeddings_placeholder,
    get_rag_settings,
    index_document_for_knowledge_base,
    resolve_retrieval_behavior,
    search_chunks,
)


class OrganizationScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_organization(self):
        return getattr(self.request.user, 'organization', None)

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(organization=organization) if organization else queryset.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['organization'] = self.get_organization()
        return context

    def perform_create(self, serializer):
        serializer.save(organization=self.get_organization(), created_by=self.request.user)


class OrganizationRAGSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = RAGSettingsSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_object(self):
        organization = getattr(self.request.user, 'organization', None)
        return get_rag_settings(organization)

    def update(self, request, *args, **kwargs):
        if getattr(request.user, 'role', None) != 'admin':
            return Response(
                {'detail': 'Apenas administradores podem atualizar as configuracoes de RAG.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


class KnowledgeBaseViewSet(OrganizationScopedViewSet):
    queryset = KnowledgeBase.objects.select_related('organization', 'created_by').all()
    serializer_class = KnowledgeBaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']

    def _resolve_document(self, request, serializer):
        document = Document.objects.filter(
            pk=serializer.validated_data['document_id'],
            organization=request.user.organization,
        ).select_related('law_case', 'organization').first()
        if document is None:
            return None, Response(
                {'document_id': ['Este recurso nao pertence a organizacao atual.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return document, None

    def _run_index_operation(self, request, knowledge_base, *, reindex=False):
        serializer_class = ReindexDocumentSerializer if reindex else IndexDocumentSerializer
        serializer = serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        document, error_response = self._resolve_document(request, serializer)
        if error_response is not None:
            return error_response

        try:
            knowledge_document, chunk_count, chunks_deleted, job = index_document_for_knowledge_base(
                document=document,
                knowledge_base=knowledge_base,
                user=request.user,
                reindex=reindex,
            )
        except Exception:
            failed_job = IndexingJob.objects.filter(
                organization=request.user.organization,
                knowledge_base=knowledge_base,
                document=document,
            ).order_by('-created_at').first()
            payload = {
                'status': 'failed',
                'message': 'Falha controlada durante a indexacao do documento.',
            }
            if failed_job is not None:
                payload['indexing_job_id'] = str(failed_job.id)
                payload['error_message'] = failed_job.error_message
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_payload = KnowledgeDocumentSerializer(knowledge_document).data
        response_payload.update(
            {
                'chunks_created': chunk_count,
                'chunks_deleted': chunks_deleted,
                'indexing_job_id': str(job.id),
            }
        )
        return Response(response_payload, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='index-document')
    def index_document(self, request, pk=None):
        return self._run_index_operation(request, self.get_object(), reindex=False)

    @action(detail=True, methods=['post'], url_path='reindex-document')
    def reindex_document(self, request, pk=None):
        return self._run_index_operation(request, self.get_object(), reindex=True)

    @action(detail=True, methods=['post'])
    def search(self, request, pk=None):
        knowledge_base = self.get_object()
        settings = get_rag_settings(request.user.organization)
        serializer = KnowledgeSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        results = search_chunks(
            organization=request.user.organization,
            query=serializer.validated_data['query'],
            knowledge_base=knowledge_base,
            limit=min(serializer.validated_data['limit'], settings.max_sources_per_answer),
        )
        grounded = build_grounded_answer(
            serializer.validated_data['query'],
            results,
            settings=settings,
        )
        retrieval_behavior = resolve_retrieval_behavior(settings)
        return Response(
            {
                'query': grounded['query'],
                'status': grounded['status'],
                'retrieval_method': grounded['retrieval_method'],
                'effective_retrieval_mode': retrieval_behavior['effective_retrieval_mode'],
                'fallback_used': retrieval_behavior['fallback_used'],
                'fallback_reason': retrieval_behavior['fallback_reason'],
                'sources_count': grounded['sources_count'],
                'confidence': grounded['confidence'],
                'sources': grounded['sources'],
            }
        )

    @action(detail=True, methods=['post'])
    def ask(self, request, pk=None):
        knowledge_base = self.get_object()
        settings = get_rag_settings(request.user.organization)
        serializer = KnowledgeAskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        effective_limit = min(serializer.validated_data['limit'], settings.max_sources_per_answer)
        result = build_grounded_answer(
            serializer.validated_data['query'],
            search_chunks(
                organization=request.user.organization,
                query=serializer.validated_data['query'],
                knowledge_base=knowledge_base,
                limit=effective_limit,
            ),
            settings=settings,
        )
        retrieval_behavior = resolve_retrieval_behavior(settings)
        result['effective_retrieval_mode'] = retrieval_behavior['effective_retrieval_mode']
        result['fallback_used'] = retrieval_behavior['fallback_used']
        result['fallback_reason'] = retrieval_behavior['fallback_reason']

        RetrievalQuery.objects.create(
            organization=request.user.organization,
            knowledge_base=knowledge_base,
            created_by=request.user,
            query=result['query'],
            answer=result['answer'],
            status=result['status'],
            retrieval_method=result['retrieval_method'],
            confidence=result['confidence'],
            sources_count=result['sources_count'],
            sources_payload={
                'retrieval_method': result['retrieval_method'],
                'effective_retrieval_mode': result['effective_retrieval_mode'],
                'fallback_used': result['fallback_used'],
                'fallback_reason': result['fallback_reason'],
                'sources_count': result['sources_count'],
                'confidence': result['confidence'],
                'sources': result['sources'],
            },
        )
        return Response(result)

    @action(detail=True, methods=['post'], url_path='prepare-embeddings')
    def prepare_embeddings(self, request, pk=None):
        knowledge_base = self.get_object()
        settings = get_rag_settings(request.user.organization)
        serializer = PrepareEmbeddingsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        knowledge_document = None
        knowledge_document_id = serializer.validated_data.get('knowledge_document_id')
        if knowledge_document_id:
            knowledge_document = KnowledgeDocument.objects.filter(
                pk=knowledge_document_id,
                organization=request.user.organization,
                knowledge_base=knowledge_base,
            ).first()
            if knowledge_document is None:
                return Response(
                    {'knowledge_document_id': ['Este recurso nao pertence a organizacao atual.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        result = generate_embeddings_placeholder(
            organization=request.user.organization,
            settings=settings,
            knowledge_document=knowledge_document,
            created_by=request.user,
        )
        return Response(
            {
                'status': result['status'],
                'reason': result['reason'],
                'audit_log_id': result['audit_log_id'],
                'effective_retrieval_mode': resolve_retrieval_behavior(settings)['effective_retrieval_mode'],
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        knowledge_base = self.get_object()
        documents_queryset = knowledge_base.documents.filter(organization=request.user.organization)
        queries_queryset = knowledge_base.queries.filter(organization=request.user.organization)
        stats_payload = {
            'total_documents': documents_queryset.count(),
            'indexed_documents': documents_queryset.filter(status='indexed').count(),
            'failed_documents': documents_queryset.filter(status='failed').count(),
            'total_chunks': DocumentChunk.objects.filter(
                organization=request.user.organization,
                knowledge_document__knowledge_base=knowledge_base,
            ).count(),
            'last_indexed_at': documents_queryset.aggregate(last_indexed_at=Max('indexed_at'))['last_indexed_at'],
            'total_queries': queries_queryset.count(),
            'last_query_at': queries_queryset.aggregate(last_query_at=Max('created_at'))['last_query_at'],
        }
        return Response(stats_payload)


class KnowledgeDocumentViewSet(OrganizationScopedViewSet):
    queryset = KnowledgeDocument.objects.select_related(
        'organization',
        'knowledge_base',
        'document',
        'created_by',
    ).all()
    serializer_class = KnowledgeDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['knowledge_base_id', 'source_type', 'status']
    search_fields = ['title', 'error_message']
    ordering_fields = ['created_at', 'updated_at', 'indexed_at']


class DocumentChunkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentChunk.objects.select_related(
        'organization',
        'knowledge_document',
        'document',
        'embedding',
    ).all()
    serializer_class = DocumentChunkSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['knowledge_document_id', 'document_id']
    search_fields = ['content']
    ordering_fields = ['chunk_index', 'created_at']

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        queryset = super().get_queryset()
        return queryset.filter(organization=organization) if organization else queryset.none()


class RetrievalQueryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RetrievalQuery.objects.select_related('organization', 'knowledge_base', 'created_by').all()
    serializer_class = RetrievalQuerySerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['knowledge_base_id', 'status']
    search_fields = ['query', 'answer']
    ordering_fields = ['created_at']

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        queryset = super().get_queryset()
        return queryset.filter(organization=organization) if organization else queryset.none()


class IndexingJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndexingJob.objects.select_related(
        'organization',
        'knowledge_base',
        'knowledge_document',
        'document',
        'created_by',
    ).all()
    serializer_class = IndexingJobSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['knowledge_base_id', 'knowledge_document_id', 'document_id', 'status']
    ordering_fields = ['created_at', 'started_at', 'finished_at']

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        queryset = super().get_queryset()
        return queryset.filter(organization=organization) if organization else queryset.none()


class EmbeddingAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmbeddingAuditLog.objects.select_related(
        'organization',
        'knowledge_document',
        'chunk',
        'created_by',
    ).all()
    serializer_class = EmbeddingAuditLogSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['knowledge_document_id', 'chunk_id', 'action', 'status', 'reason']
    ordering_fields = ['created_at']

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        queryset = super().get_queryset()
        return queryset.filter(organization=organization) if organization else queryset.none()
