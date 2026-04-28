from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from jurisai.permissions import IsOrganizationMember

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related('organization').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['channel', 'sent']
    ordering_fields = ['created_at', 'sent_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organization=self.request.user.organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)
