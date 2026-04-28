from rest_framework import serializers

from accounts.models import User
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from marketplace.models import MarketplaceTemplate, TemplatePublisher, TemplatePurchase, TemplateReview


class TemplatePublisherSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    user_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'user_id': User}

    class Meta:
        model = TemplatePublisher
        fields = ['id', 'organization', 'organization_id', 'user', 'user_id', 'display_name', 'created_at']
        read_only_fields = ['organization', 'user', 'created_at']

    def create(self, validated_data):
        return TemplatePublisher.objects.create(
            organization_id=validated_data['organization_id'],
            user_id=validated_data['user_id'],
            display_name=validated_data['display_name'],
        )


class MarketplaceTemplateSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    publisher_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'publisher_id': TemplatePublisher}

    class Meta:
        model = MarketplaceTemplate
        fields = ['id', 'organization', 'organization_id', 'publisher', 'publisher_id', 'title', 'description', 'price', 'is_active', 'created_at']
        read_only_fields = ['organization', 'publisher', 'created_at']

    def create(self, validated_data):
        return MarketplaceTemplate.objects.create(
            organization_id=validated_data['organization_id'],
            publisher_id=validated_data['publisher_id'],
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            price=validated_data.get('price', 0),
            is_active=validated_data.get('is_active', True),
        )


class TemplatePurchaseSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    marketplace_template_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'marketplace_template_id': MarketplaceTemplate}

    class Meta:
        model = TemplatePurchase
        fields = ['id', 'organization', 'organization_id', 'marketplace_template', 'marketplace_template_id', 'purchased_by', 'created_at']
        read_only_fields = ['organization', 'marketplace_template', 'purchased_by', 'created_at']

    def create(self, validated_data):
        return TemplatePurchase.objects.create(
            organization_id=validated_data['organization_id'],
            marketplace_template_id=validated_data['marketplace_template_id'],
            purchased_by=self.context['request'].user,
        )


class TemplateReviewSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    marketplace_template_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'marketplace_template_id': MarketplaceTemplate}

    class Meta:
        model = TemplateReview
        fields = [
            'id', 'organization', 'organization_id', 'marketplace_template', 'marketplace_template_id',
            'reviewer', 'rating', 'comment', 'created_at',
        ]
        read_only_fields = ['organization', 'marketplace_template', 'reviewer', 'created_at']

    def create(self, validated_data):
        return TemplateReview.objects.create(
            organization_id=validated_data['organization_id'],
            marketplace_template_id=validated_data['marketplace_template_id'],
            reviewer=self.context['request'].user,
            rating=validated_data.get('rating', 5),
            comment=validated_data.get('comment', ''),
        )
