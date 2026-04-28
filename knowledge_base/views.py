from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from jurisai.permissions import IsOrganizationMember
from knowledge_base.models import DocumentChunk, KnowledgeBase, KnowledgeDocument, RetrievalQuery
from knowledge_base.serializers import (
    DocumentChunkSerializer,
    KnowledgeBaseSerializer,
    KnowledgeDocumentSerializer,
    RetrievalQuerySerializer,
)


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class KnowledgeBaseViewSet(OrganizationFilteredViewSet):
    queryset = KnowledgeBase.objects.select_related('organization', 'created_by').all()
    serializer_class = KnowledgeBaseSerializer


class KnowledgeDocumentViewSet(OrganizationFilteredViewSet):
    queryset = KnowledgeDocument.objects.select_related('organization', 'knowledge_base', 'document').all()
    serializer_class = KnowledgeDocumentSerializer


class DocumentChunkViewSet(OrganizationFilteredViewSet):
    queryset = DocumentChunk.objects.select_related('organization', 'knowledge_document').all()
    serializer_class = DocumentChunkSerializer


class RetrievalQueryViewSet(OrganizationFilteredViewSet):
    queryset = RetrievalQuery.objects.select_related('organization', 'knowledge_base', 'user').all()
    serializer_class = RetrievalQuerySerializer


class KnowledgeBaseSearchPlaceholderView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response({'status': 'not_implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

