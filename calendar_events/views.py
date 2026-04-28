from django.utils import timezone
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from calendar_events.models import CalendarEvent
from calendar_events.serializers import CalendarEventSerializer
from jurisai.permissions import IsOrganizationMember


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.select_related('organization', 'law_case', 'created_by', 'assigned_to').all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'status', 'assigned_to_id', 'law_case_id']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_at', 'end_at', 'created_at']

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        queryset = self.get_queryset().filter(start_at__gte=timezone.now()).order_by('start_at')
        return Response(CalendarEventSerializer(queryset, many=True).data)

    @action(detail=False, methods=['get'], url_path='month')
    def month(self, request):
        now = timezone.now()
        month = int(request.query_params.get('month', now.month))
        year = int(request.query_params.get('year', now.year))
        queryset = self.get_queryset().filter(start_at__year=year, start_at__month=month).order_by('start_at')
        return Response(CalendarEventSerializer(queryset, many=True).data)

