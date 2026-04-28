from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from crm.models import Consultation, Lead, LeadActivity
from crm.serializers import ConsultationSerializer, LeadActivitySerializer, LeadSerializer
from jurisai.permissions import IsOrganizationMember


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class LeadViewSet(OrganizationFilteredViewSet):
    queryset = Lead.objects.select_related('organization', 'owner').all()
    serializer_class = LeadSerializer


class LeadActivityViewSet(OrganizationFilteredViewSet):
    queryset = LeadActivity.objects.select_related('organization', 'lead', 'author').all()
    serializer_class = LeadActivitySerializer


class ConsultationViewSet(OrganizationFilteredViewSet):
    queryset = Consultation.objects.select_related('organization', 'lead', 'assigned_to').all()
    serializer_class = ConsultationSerializer

