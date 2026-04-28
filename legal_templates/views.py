from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from jurisai.permissions import IsOrganizationMember
from legal_templates.models import GeneratedDocument, LegalTemplate, TemplateCategory
from legal_templates.serializers import (
    GeneratedDocumentSerializer,
    LegalTemplateSerializer,
    TemplateCategorySerializer,
    render_template_body,
)


class TemplateCategoryViewSet(viewsets.ModelViewSet):
    queryset = TemplateCategory.objects.select_related('organization').all()
    serializer_class = TemplateCategorySerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class LegalTemplateViewSet(viewsets.ModelViewSet):
    queryset = LegalTemplate.objects.select_related('organization', 'category', 'created_by').all()
    serializer_class = LegalTemplateSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['document_type', 'is_active', 'category_id']
    search_fields = ['title', 'description', 'body']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        template = self.get_object()
        variables_payload = request.data.get('variables_payload', {})
        law_case_id = request.data.get('law_case_id')
        rendered = render_template_body(template, variables_payload)
        generated = GeneratedDocument.objects.create(
            organization=request.user.organization,
            template=template,
            law_case_id=law_case_id,
            generated_by=request.user,
            rendered_content=rendered,
            variables_payload=variables_payload,
        )
        return Response(GeneratedDocumentSerializer(generated).data, status=status.HTTP_201_CREATED)


class GeneratedDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeneratedDocument.objects.select_related('organization', 'template', 'law_case', 'generated_by').all()
    serializer_class = GeneratedDocumentSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

