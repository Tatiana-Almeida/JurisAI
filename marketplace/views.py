from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from jurisai.permissions import IsOrganizationMember
from marketplace.models import MarketplaceTemplate, TemplatePublisher, TemplatePurchase, TemplateReview
from marketplace.serializers import (
    MarketplaceTemplateSerializer,
    TemplatePublisherSerializer,
    TemplatePurchaseSerializer,
    TemplateReviewSerializer,
)


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class TemplatePublisherViewSet(OrganizationFilteredViewSet):
    queryset = TemplatePublisher.objects.select_related('organization', 'user').all()
    serializer_class = TemplatePublisherSerializer


class MarketplaceTemplateViewSet(OrganizationFilteredViewSet):
    queryset = MarketplaceTemplate.objects.select_related('organization', 'publisher').all()
    serializer_class = MarketplaceTemplateSerializer


class TemplatePurchaseViewSet(OrganizationFilteredViewSet):
    queryset = TemplatePurchase.objects.select_related('organization', 'marketplace_template', 'purchased_by').all()
    serializer_class = TemplatePurchaseSerializer


class TemplateReviewViewSet(OrganizationFilteredViewSet):
    queryset = TemplateReview.objects.select_related('organization', 'marketplace_template', 'reviewer').all()
    serializer_class = TemplateReviewSerializer

