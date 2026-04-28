from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from e_signature.models import SignatureAuditTrail, SignatureParty, SignatureRequest, SignedDocument
from e_signature.serializers import (
    SignatureAuditTrailSerializer,
    SignaturePartySerializer,
    SignatureRequestSerializer,
    SignedDocumentSerializer,
)
from jurisai.permissions import IsOrganizationMember


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class SignatureRequestViewSet(OrganizationFilteredViewSet):
    queryset = SignatureRequest.objects.select_related('organization', 'document', 'requested_by').all()
    serializer_class = SignatureRequestSerializer


class SignaturePartyViewSet(OrganizationFilteredViewSet):
    queryset = SignatureParty.objects.select_related('organization', 'signature_request', 'user').all()
    serializer_class = SignaturePartySerializer


class SignedDocumentViewSet(OrganizationFilteredViewSet):
    queryset = SignedDocument.objects.select_related('organization', 'signature_request').all()
    serializer_class = SignedDocumentSerializer


class SignatureAuditTrailViewSet(OrganizationFilteredViewSet):
    queryset = SignatureAuditTrail.objects.select_related('organization', 'signature_request', 'actor').all()
    serializer_class = SignatureAuditTrailSerializer


class SignatureProviderPlaceholderView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response({'status': 'not_implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

