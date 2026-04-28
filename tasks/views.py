from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from jurisai.permissions import IsOrganizationMember
from tasks.models import Task
from tasks.serializers import TaskChecklistItemSerializer, TaskCommentSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('organization', 'law_case', 'assigned_to', 'created_by').filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['priority', 'status', 'assigned_to_id', 'law_case_id']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'updated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = getattr(self.request.user, 'organization', None)
        return queryset.filter(organization=organization) if organization else queryset.none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted', 'updated_at'])

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        task = self.get_object()
        if request.method.lower() == 'get':
            serializer = TaskCommentSerializer(task.comments.all(), many=True)
            return Response(serializer.data)

        serializer = TaskCommentSerializer(data=request.data, context={'request': request, 'task': task, 'organization': request.user.organization})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(TaskCommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], url_path='checklist')
    def checklist(self, request, pk=None):
        task = self.get_object()
        if request.method.lower() == 'get':
            serializer = TaskChecklistItemSerializer(task.checklist_items.all(), many=True)
            return Response(serializer.data)

        serializer = TaskChecklistItemSerializer(data=request.data, context={'request': request, 'task': task, 'organization': request.user.organization})
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(TaskChecklistItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save(update_fields=['status', 'completed_at', 'updated_at'])
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        task = self.get_object()
        task.status = 'cancelled'
        task.save(update_fields=['status', 'updated_at'])
        return Response(TaskSerializer(task).data)

