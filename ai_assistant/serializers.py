from rest_framework import serializers
from ai_assistant.models import AIRequest


class AIRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRequest
        fields = ['id', 'user', 'organization', 'prompt', 'response', 'tokens_used', 'cost', 'created_at']
        read_only_fields = ['id', 'user', 'response', 'tokens_used', 'cost', 'created_at']
