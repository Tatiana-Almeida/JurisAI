from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from jurisai.serializers import OrganizationScopedValidationMixin
from organizations.serializers import OrganizationSerializer


class UserSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'organization', 'organization_id', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}, 'role': {'required': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data, **kwargs):
        organization = kwargs.pop('organization', None) or self.context.get('organization')
        organization_id = validated_data.pop('organization_id', None)
        if organization is not None:
            validated_data['organization_id'] = organization.id
        elif organization_id is not None:
            validated_data['organization_id'] = organization_id
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
