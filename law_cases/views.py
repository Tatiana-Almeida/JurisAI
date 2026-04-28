from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from law_cases.models import LawCase
from law_cases.serializers import LawCaseSerializer
from jurisai.permissions import IsOrganizationMember

class LawCaseViewSet(viewsets.ModelViewSet):
    queryset = LawCase.objects.select_related('organization', 'client', 'lawyer').filter(deleted=False)
    serializer_class = LawCaseSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'lawyer_id', 'client_id']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        base = super().get_queryset()
        if self.request.user.organization:
            return base.filter(organization=self.request.user.organization)
        return base.none()

    def perform_create(self, serializer):
        organization = getattr(self.request.user, 'organization', None)
        if organization and organization.cases.count() >= organization.max_cases():
            raise PermissionDenied('Limite de casos do plano atingido')
        serializer.save(organization=organization)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
