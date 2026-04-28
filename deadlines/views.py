from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from deadlines.models import Deadline
from deadlines.serializers import DeadlineSerializer
from jurisai.permissions import IsOrganizationMember

class DeadlineViewSet(viewsets.ModelViewSet):
    queryset = Deadline.objects.select_related('law_case', 'organization').all()
    serializer_class = DeadlineSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['completed', 'law_case_id']
    search_fields = ['law_case__title']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            queryset = queryset.filter(organization=self.request.user.organization)
        else:
            return queryset.none()

        upcoming_days = self.request.query_params.get('upcoming_days')
        if upcoming_days is not None:
            try:
                days = int(upcoming_days)
                end = timezone.now() + timezone.timedelta(days=days)
                queryset = queryset.filter(due_date__lte=end, completed=False)
            except (TypeError, ValueError):
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        deadline = self.get_object()
        deadline.completed = True
        deadline.save()
        return Response(DeadlineSerializer(deadline).data)
