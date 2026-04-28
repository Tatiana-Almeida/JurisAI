from rest_framework import serializers


class OrganizationScopedValidationMixin:
    organization_context_key = 'organization'
    organization_field_name = 'organization_id'
    organization_required_message = 'Este campo é obrigatório.'

    def resolve_organization_id(self, data):
        organization = self.context.get(self.organization_context_key)
        if organization is not None:
            data[self.organization_field_name] = str(organization.id)
            return data

        request = self.context.get('request')
        user = getattr(request, 'user', None) if request is not None else None
        if getattr(user, 'is_authenticated', False) and getattr(user, 'organization', None):
            data[self.organization_field_name] = str(user.organization_id)

        return data

    def validate(self, data):
        data = self.resolve_organization_id(data)
        if self.organization_field_name not in data:
            raise serializers.ValidationError(
                {self.organization_field_name: self.organization_required_message}
            )
        return data


class TenantRelationValidationMixin:
    tenant_relation_fields = {}
    tenant_relation_error_message = 'Este recurso não pertence à organização atual.'

    def validate_tenant_relations(self, data):
        organization_id = data.get('organization_id')
        if organization_id is None:
            return data

        for field_name, related_model in self.tenant_relation_fields.items():
            related_id = data.get(field_name)
            if related_id is None:
                continue

            related_organization_id = related_model.objects.filter(
                pk=related_id
            ).values_list('organization_id', flat=True).first()

            if related_organization_id is None:
                continue

            if str(related_organization_id) != str(organization_id):
                raise serializers.ValidationError(
                    {field_name: self.tenant_relation_error_message}
                )

        return data

    def validate(self, data):
        data = super().validate(data)
        return self.validate_tenant_relations(data)
