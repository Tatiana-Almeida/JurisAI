import re

from rest_framework import serializers

from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from law_cases.models import LawCase
from legal_templates.models import GeneratedDocument, LegalTemplate, TemplateCategory, TemplateVariable


class TemplateVariableSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    template_id = serializers.UUIDField(write_only=True, required=False)
    tenant_relation_fields = {'template_id': LegalTemplate}

    class Meta:
        model = TemplateVariable
        fields = ['id', 'organization', 'organization_id', 'template', 'template_id', 'name', 'label', 'required', 'default_value']
        read_only_fields = ['organization', 'template']

    def create(self, validated_data):
        template_id = validated_data.get('template_id') or self.context['template'].id
        return TemplateVariable.objects.create(
            organization_id=validated_data['organization_id'],
            template_id=template_id,
            name=validated_data['name'],
            label=validated_data['label'],
            required=validated_data.get('required', False),
            default_value=validated_data.get('default_value', ''),
        )


class TemplateCategorySerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = TemplateCategory
        fields = ['id', 'organization', 'organization_id', 'name', 'description', 'created_at']
        read_only_fields = ['organization', 'created_at']

    def create(self, validated_data):
        return TemplateCategory.objects.create(
            organization_id=validated_data['organization_id'],
            name=validated_data['name'],
            description=validated_data.get('description', ''),
        )


class LegalTemplateSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    variables = TemplateVariableSerializer(many=True, required=False)

    class Meta:
        model = LegalTemplate
        fields = [
            'id', 'organization', 'organization_id', 'category', 'category_id', 'title', 'description',
            'document_type', 'body', 'is_active', 'created_by', 'created_at', 'updated_at', 'variables',
        ]
        read_only_fields = ['organization', 'category', 'created_by', 'created_at', 'updated_at']

    def validate(self, data):
        data = super().validate(data)
        category_id = data.get('category_id')
        organization_id = data.get('organization_id')
        if category_id and not TemplateCategory.objects.filter(id=category_id, organization_id=organization_id).exists():
            raise serializers.ValidationError({'category_id': 'Este recurso nao pertence a organizacao atual.'})
        return data

    def create(self, validated_data):
        variables = validated_data.pop('variables', [])
        template = LegalTemplate.objects.create(
            organization_id=validated_data['organization_id'],
            category_id=validated_data.get('category_id'),
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            document_type=validated_data.get('document_type', 'other'),
            body=validated_data['body'],
            is_active=validated_data.get('is_active', True),
            created_by=self.context['request'].user,
        )
        for variable in variables:
            TemplateVariable.objects.create(
                organization=template.organization,
                template=template,
                name=variable['name'],
                label=variable['label'],
                required=variable.get('required', False),
                default_value=variable.get('default_value', ''),
            )
        return template

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['category_id'] = str(instance.category_id) if instance.category_id else None
        data['variables'] = TemplateVariableSerializer(instance.variables.all(), many=True).data
        return data


class GeneratedDocumentSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    template_id = serializers.UUIDField(write_only=True)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    generated_by_id = serializers.UUIDField(source='generated_by.id', read_only=True)
    tenant_relation_fields = {
        'template_id': LegalTemplate,
        'law_case_id': LawCase,
    }

    class Meta:
        model = GeneratedDocument
        fields = [
            'id', 'organization', 'organization_id', 'template', 'template_id', 'law_case', 'law_case_id',
            'generated_by', 'generated_by_id', 'rendered_content', 'variables_payload', 'created_at',
        ]
        read_only_fields = ['organization', 'template', 'law_case', 'generated_by', 'rendered_content', 'created_at']


def render_template_body(template, payload):
    rendered = template.body
    for variable in template.variables.all():
        value = payload.get(variable.name, variable.default_value)
        if variable.required and value in (None, ''):
            raise serializers.ValidationError({'variables_payload': f'Variavel obrigatoria ausente: {variable.name}'})
        rendered = rendered.replace(f'{{{{{variable.name}}}}}', str(value or ''))
    rendered = re.sub(r'{{[^{}]+}}', '', rendered)
    return rendered
