from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from documents.models import Document
from jurisai.permissions import IsOrganizationMember
from knowledge_base.models import DocumentChunk, KnowledgeBase, KnowledgeDocument, RetrievalQuery
from knowledge_base.serializers import (
    DocumentChunkSerializer,
    IndexDocumentSerializer,
    KnowledgeAskSerializer,
    KnowledgeBaseSerializer,
    KnowledgeDocumentSerializer,
    KnowledgeSearchSerializer,
    RetrievalQuerySerializer,
)
from knowledge_base.services import build_grounded_answer, index_document_for_knowledge_base, search_chunks


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


class KnowledgeBaseViewSet(OrganizationScopedViewSet):
    queryset = KnowledgeBase.objects.select_related('organization', 'created_by').all()
    serializer_class = KnowledgeBaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']

    @action(detail=True, methods=['post'], url_path='index-document')
    def index_document(self, request, pk=None):
        knowledge_base = self.get_object()
        serializer = IndexDocumentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        document = Document.objects.filter(
            pk=serializer.validated_data['document_id'],
            organization=request.user.organization,
        ).select_related('law_case', 'organization').first()
        if document is None:
            return Response(
                {'document_id': ['Este recurso nao pertence a organizacao atual.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        knowledge_document, chunk_count = index_document_for_knowledge_base(
            document=document,
            knowledge_base=knowledge_base,
            user=request.user,
        )
        response_payload = KnowledgeDocumentSerializer(knowledge_document).data
        response_payload['chunks_created'] = chunk_count
        return Response(response_payload, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def search(self, request, pk=None):
        knowledge_base = self.get_object()
        serializer = KnowledgeSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        results = search_chunks(
            organization=request.user.organization,
            query=serializer.validated_data['query'],
            knowledge_base=knowledge_base,
            limit=serializer.validated_data['limit'],
        )
        sources = build_grounded_answer(serializer.validated_data['query'], results)['sources']
        status_value = 'completed' if sources else 'no_sources'
        return Response(
            {
                'query': serializer.validated_data['query'],
                'status': status_value,
                'sources': sources,
            }
        )

    @action(detail=True, methods=['post'])
    def ask(self, request, pk=None):
        knowledge_base = self.get_object()
        serializer = KnowledgeAskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = build_grounded_answer(
            serializer.validated_data['query'],
            search_chunks(
                organization=request.user.organization,
                query=serializer.validated_data['query'],
                knowledge_base=knowledge_base,
                limit=serializer.validated_data['limit'],
            ),
        )

        RetrievalQuery.objects.create(
            organization=request.user.organization,
            knowledge_base=knowledge_base,
            created_by=request.user,
            query=result['query'],
            answer=result['answer'],
            status=result['status'],
            sources_payload=result['sources'],
        )
        return Response(result)


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
    queryset = DocumentChunk.objects.select_related('organization', 'knowledge_document', 'document').all()
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
