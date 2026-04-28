from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from audit_logs.models import AuditLog
from audit_logs.serializers import AuditLogSerializer
from jurisai.permissions import IsAdmin

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user', 'organization').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'entity', 'user']
    search_fields = ['entity', 'before', 'after']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = getattr(self.request.user, 'organization', None)
        if organization is None:
            return queryset.none()
        return queryset.filter(organization=organization)
