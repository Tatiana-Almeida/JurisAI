from django.utils import timezone
from rest_framework import serializers

from accounts.models import User
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from law_cases.models import LawCase
from tasks.models import Task, TaskChecklistItem, TaskComment


class TaskSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    assigned_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    created_by_id = serializers.UUIDField(source='created_by.id', read_only=True)

    tenant_relation_fields = {
        'law_case_id': LawCase,
        'assigned_to_id': User,
    }

    class Meta:
        model = Task
        fields = [
            'id', 'organization', 'organization_id', 'law_case', 'law_case_id', 'title',
            'description', 'assigned_to', 'assigned_to_id', 'created_by', 'created_by_id',
            'priority', 'status', 'due_date', 'completed_at', 'created_at', 'updated_at',
            'is_deleted',
        ]
        read_only_fields = ['organization', 'law_case', 'assigned_to', 'created_by', 'completed_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Task.objects.create(
            organization_id=validated_data['organization_id'],
            law_case_id=validated_data.get('law_case_id'),
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            assigned_to_id=validated_data.get('assigned_to_id'),
            created_by=self.context['request'].user,
            priority=validated_data.get('priority', 'medium'),
            status=validated_data.get('status', 'pending'),
            due_date=validated_data.get('due_date'),
        )

    def update(self, instance, validated_data):
        instance.law_case_id = validated_data.get('law_case_id', instance.law_case_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.assigned_to_id = validated_data.get('assigned_to_id', instance.assigned_to_id)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        if instance.status == 'completed' and instance.completed_at is None:
            instance.completed_at = timezone.now()
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        data['assigned_to_id'] = str(instance.assigned_to_id) if instance.assigned_to_id else None
        data['created_by_id'] = str(instance.created_by_id)
        return data


class TaskCommentSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    task_id = serializers.UUIDField(write_only=True, required=False)
    author_id = serializers.UUIDField(source='author.id', read_only=True)

    tenant_relation_fields = {
        'task_id': Task,
    }

    class Meta:
        model = TaskComment
        fields = ['id', 'organization', 'organization_id', 'task', 'task_id', 'author', 'author_id', 'message', 'created_at']
        read_only_fields = ['organization', 'task', 'author', 'created_at']

    def create(self, validated_data):
        task_id = validated_data.get('task_id') or self.context['task'].id
        return TaskComment.objects.create(
            organization_id=validated_data['organization_id'],
            task_id=task_id,
            author=self.context['request'].user,
            message=validated_data['message'],
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['task_id'] = str(instance.task_id)
        data['author_id'] = str(instance.author_id)
        return data


class TaskChecklistItemSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    task_id = serializers.UUIDField(write_only=True, required=False)

    tenant_relation_fields = {
        'task_id': Task,
    }

    class Meta:
        model = TaskChecklistItem
        fields = ['id', 'organization', 'organization_id', 'task', 'task_id', 'title', 'is_completed', 'completed_at', 'created_at']
        read_only_fields = ['organization', 'task', 'completed_at', 'created_at']

    def create(self, validated_data):
        task_id = validated_data.get('task_id') or self.context['task'].id
        return TaskChecklistItem.objects.create(
            organization_id=validated_data['organization_id'],
            task_id=task_id,
            title=validated_data['title'],
            is_completed=validated_data.get('is_completed', False),
            completed_at=timezone.now() if validated_data.get('is_completed') else None,
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.completed_at = timezone.now() if instance.is_completed else None
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['task_id'] = str(instance.task_id)
        return data
