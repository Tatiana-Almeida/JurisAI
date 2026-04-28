import pytest

from legal_templates.models import GeneratedDocument, LegalTemplate
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


@pytest.mark.django_db
def test_create_template():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        '/api/v1/legal-templates/',
        {
            'title': 'Peticao simples',
            'description': 'Template base',
            'document_type': 'petition',
            'body': 'Cliente: {{cliente_nome}}',
            'variables': [
                {
                    'name': 'cliente_nome',
                    'label': 'Nome do cliente',
                    'required': True,
                }
            ],
        },
        format='json',
    )

    assert response.status_code == 201
    assert LegalTemplate.objects.filter(title='Peticao simples', organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_generate_document_with_variables():
    tenant = build_service_tenant_fixture()
    template = LegalTemplate.objects.create(
        organization=tenant['org_b'],
        title='Contrato',
        document_type='contract',
        body='Cliente: {{cliente_nome}}',
        created_by=tenant['admin_b'],
    )
    template.variables.create(
        organization=tenant['org_b'],
        name='cliente_nome',
        label='Cliente',
        required=True,
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/legal-templates/{template.id}/generate/',
        {
            'variables_payload': {'cliente_nome': 'Empresa X'},
            'law_case_id': str(tenant['case_b'].id),
        },
        format='json',
    )

    assert response.status_code == 201
    generated = GeneratedDocument.objects.get(template=template)
    assert generated.organization == tenant['org_b']
    assert generated.rendered_content == 'Cliente: Empresa X'


@pytest.mark.django_db
def test_reject_generation_when_required_variable_is_missing():
    tenant = build_service_tenant_fixture()
    template = LegalTemplate.objects.create(
        organization=tenant['org_b'],
        title='Minuta',
        body='Parte: {{parte}}',
        created_by=tenant['admin_b'],
    )
    template.variables.create(
        organization=tenant['org_b'],
        name='parte',
        label='Parte',
        required=True,
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/legal-templates/{template.id}/generate/',
        {'variables_payload': {}},
        format='json',
    )

    assert response.status_code == 400
    assert not GeneratedDocument.objects.exists()


@pytest.mark.django_db
def test_user_does_not_access_template_from_other_tenant():
    tenant = build_service_tenant_fixture()
    foreign_template = LegalTemplate.objects.create(
        organization=tenant['org_a'],
        title='Template A',
        body='Texto',
        created_by=tenant['admin_a'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get(f'/api/v1/legal-templates/{foreign_template.id}/')

    assert response.status_code == 404

