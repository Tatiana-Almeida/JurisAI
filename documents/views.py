from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from documents.models import Document
from documents.serializers import DocumentSerializer
from jurisai.permissions import IsOrganizationMember

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('law_case', 'organization').all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'law_case_id']
    search_fields = ['content', 'law_case__title']
    ordering_fields = ['created_at', 'version']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            return queryset.filter(organization=self.request.user.organization)
        return queryset.none()

    def perform_create(self, serializer):
        organization = getattr(self.request.user, 'organization', None)
        if organization and organization.documents.count() >= organization.max_documents():
            raise PermissionDenied('Limite de documentos do plano atingido')
        serializer.save(organization=organization)
