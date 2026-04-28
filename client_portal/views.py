from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from client_portal.models import ClientCaseVisibility, ClientDocumentShare, ClientMessage
from client_portal.serializers import ClientCaseVisibilitySerializer, ClientDocumentShareSerializer, ClientMessageSerializer
from documents.serializers import DocumentSerializer
from jurisai.permissions import IsOrganizationMember
from law_cases.serializers import LawCaseSerializer


class ClientPortalCasesView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        visibility_qs = ClientCaseVisibility.objects.filter(
            organization=request.user.organization,
            client=request.user,
            can_view=True,
        ).select_related('law_case')
        cases = [item.law_case for item in visibility_qs]
        return Response(LawCaseSerializer(cases, many=True).data)


class ClientPortalDocumentsView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        now = timezone.now()
        shares = ClientDocumentShare.objects.filter(
            organization=request.user.organization,
            client=request.user,
        ).select_related('document').filter(
            expires_at__isnull=True,
        ) | ClientDocumentShare.objects.filter(
            organization=request.user.organization,
            client=request.user,
            expires_at__gte=now,
        ).select_related('document')
        documents = [share.document for share in shares]
        return Response(DocumentSerializer(documents, many=True).data)


class ClientPortalMessagesView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        queryset = ClientMessage.objects.filter(
            organization=request.user.organization,
        ).filter(sender=request.user) | ClientMessage.objects.filter(
            organization=request.user.organization,
            recipient=request.user,
        )
        return Response(ClientMessageSerializer(queryset.order_by('-created_at'), many=True).data)

    def post(self, request):
        serializer = ClientMessageSerializer(data=request.data, context={'request': request, 'organization': request.user.organization})
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(ClientMessageSerializer(message).data, status=status.HTTP_201_CREATED)


class ClientCaseVisibilityViewSet(viewsets.ModelViewSet):
    queryset = ClientCaseVisibility.objects.select_related('organization', 'client', 'law_case').all()
    serializer_class = ClientCaseVisibilitySerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class ClientDocumentShareViewSet(viewsets.ModelViewSet):
    queryset = ClientDocumentShare.objects.select_related('organization', 'client', 'document', 'shared_by').all()
    serializer_class = ClientDocumentShareSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

