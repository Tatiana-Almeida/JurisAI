from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import UserSerializer
from jurisai.permissions import IsOrganizationMember
from organizations.models import Organization


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('organization').all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'role']
    ordering_fields = ['created_at', 'name']
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            return queryset.filter(organization=self.request.user.organization)
        return queryset.none()

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied('Apenas administradores podem criar usuários')
        organization = getattr(self.request.user, 'organization', None)
        if organization and not organization.can_add_user():
            raise PermissionDenied('Limite de usuários do plano atingido')
        serializer.save(organization=organization)

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user
        if request.method == 'GET':
            return Response(UserSerializer(user).data)
        partial = request.method == 'PATCH'
        data = request.data.copy()
        data.pop('role', None)
        data.pop('organization_id', None)
        serializer = UserSerializer(user, data=data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        organization_name = request.data.get('organization_name')
        plan = request.data.get('plan', 'free')

        if not organization_name:
            return Response({'organization_name': 'O nome da organização é obrigatório para cadastro.'}, status=status.HTTP_400_BAD_REQUEST)

        organization = Organization.objects.create(name=organization_name, plan=plan)
        serializer = UserSerializer(data=request.data, context={'request': request, 'organization': organization})
        serializer.is_valid(raise_exception=True)
        user = serializer.save(organization=organization)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not request.user.check_password(old_password):
            return Response({'detail': 'Senha antiga incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()
        return Response({'detail': 'Senha alterada com sucesso.'})
