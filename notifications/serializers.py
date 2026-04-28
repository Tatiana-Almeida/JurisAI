from rest_framework import serializers
from notifications.models import Notification
from jurisai.serializers import OrganizationScopedValidationMixin


class NotificationSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Notification
        fields = ['id', 'organization', 'organization_id', 'channel', 'recipient', 'subject', 'body', 'sent', 'created_at', 'sent_at']
        read_only_fields = ['organization', 'sent', 'created_at', 'sent_at']

    def create(self, validated_data, **kwargs):
        return Notification.objects.create(
            organization_id=validated_data['organization_id'],
            channel=validated_data['channel'],
            recipient=validated_data['recipient'],
            subject=validated_data.get('subject', ''),
            body=validated_data['body'],
        )
