from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer
from jurisai.permissions import IsOrganizationMember, IsAdmin

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'plan']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        if self.request.user.organization:
            return Organization.objects.filter(id=self.request.user.organization.id)
        return Organization.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def plans(self, request):
        plans = [
            {'key': 'free', 'name': 'Free', 'users': 1, 'cases': 10, 'documents': 50, 'ia_requests': 20, 'price': 0},
            {'key': 'solo', 'name': 'Solo', 'users': 1, 'cases': 100, 'documents': 500, 'ia_requests': 100, 'price': 297},
            {'key': 'growth', 'name': 'Escritório', 'users': 10, 'cases': 'Ilimitado', 'documents': 'Ilimitado', 'ia_requests': 500, 'price': 597},
            {'key': 'enterprise', 'name': 'Enterprise', 'users': 'Ilimitado', 'cases': 'Ilimitado', 'documents': 'Ilimitado', 'ia_requests': 2000, 'price': 897},
        ]
        return Response(plans)
