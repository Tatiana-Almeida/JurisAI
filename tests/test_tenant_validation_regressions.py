import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from deadlines.models import Deadline
from documents.models import Document
from law_cases.models import LawCase
from organizations.models import Organization


def authenticate(client, email, password):
    token_response = client.post(
        reverse('token_obtain_pair'),
        {'email': email, 'password': password},
        format='json',
    )
    assert token_response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")


def build_tenant_fixture():
    org_a = Organization.objects.create(name='Org A Tenant Validation', plan='free')
    org_b = Organization.objects.create(name='Org B Tenant Validation', plan='free')

    admin_b = User.objects.create_user(
        email='admin-b-tenant@example.com',
        password='strongpass123',
        name='Admin B',
        organization=org_b,
        role='admin',
        is_staff=True,
    )
    lawyer_a = User.objects.create_user(
        email='lawyer-a-tenant@example.com',
        password='strongpass123',
        name='Lawyer A',
        organization=org_a,
        role='advogado',
    )
    client_a = User.objects.create_user(
        email='client-a-tenant@example.com',
        password='strongpass123',
        name='Client A',
        organization=org_a,
        role='cliente',
    )
    lawyer_b = User.objects.create_user(
        email='lawyer-b-tenant@example.com',
        password='strongpass123',
        name='Lawyer B',
        organization=org_b,
        role='advogado',
    )
    client_b = User.objects.create_user(
        email='client-b-tenant@example.com',
        password='strongpass123',
        name='Client B',
        organization=org_b,
        role='cliente',
    )

    return {
        'org_a': org_a,
        'org_b': org_b,
        'admin_b': admin_b,
        'lawyer_a': lawyer_a,
        'client_a': client_a,
        'lawyer_b': lawyer_b,
        'client_b': client_b,
    }


@pytest.mark.django_db
def test_reject_case_creation_with_client_from_other_organization():
    tenant = build_tenant_fixture()
    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.post(
        '/api/v1/cases/',
        {
            'title': 'Caso com cliente externo',
            'description': 'Nao deveria aceitar client_id cross-tenant',
            'client_id': str(tenant['client_a'].id),
            'lawyer_id': str(tenant['lawyer_b'].id),
            'status': 'open',
        },
        format='json',
    )

    assert response.status_code in (400, 403)
    assert not LawCase.objects.filter(title='Caso com cliente externo').exists()


@pytest.mark.django_db
def test_reject_case_creation_with_lawyer_from_other_organization():
    tenant = build_tenant_fixture()
    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.post(
        '/api/v1/cases/',
        {
            'title': 'Caso com advogado externo',
            'description': 'Nao deveria aceitar lawyer_id cross-tenant',
            'client_id': str(tenant['client_b'].id),
            'lawyer_id': str(tenant['lawyer_a'].id),
            'status': 'open',
        },
        format='json',
    )

    assert response.status_code in (400, 403)
    assert not LawCase.objects.filter(title='Caso com advogado externo').exists()


@pytest.mark.django_db
def test_reject_deadline_creation_with_law_case_from_other_organization():
    tenant = build_tenant_fixture()
    foreign_case = LawCase.objects.create(
        title='Caso da organizacao A',
        description='Caso base para prazo cross-tenant',
        client=tenant['client_a'],
        lawyer=tenant['lawyer_a'],
        organization=tenant['org_a'],
        status='open',
    )

    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.post(
        '/api/v1/deadlines/',
        {
            'law_case_id': str(foreign_case.id),
            'due_date': '2030-01-01T12:00:00Z',
            'completed': False,
        },
        format='json',
    )

    assert response.status_code in (400, 403)
    assert not Deadline.objects.filter(law_case=foreign_case).exists()


@pytest.mark.django_db
def test_allow_deadline_creation_with_law_case_from_same_organization():
    tenant = build_tenant_fixture()
    local_case = LawCase.objects.create(
        title='Caso da organizacao B',
        description='Caso base para prazo valido',
        client=tenant['client_b'],
        lawyer=tenant['lawyer_b'],
        organization=tenant['org_b'],
        status='open',
    )

    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.post(
        '/api/v1/deadlines/',
        {
            'law_case_id': str(local_case.id),
            'due_date': '2030-01-01T12:00:00Z',
            'completed': False,
        },
        format='json',
    )

    assert response.status_code == 201
    assert Deadline.objects.filter(law_case=local_case, organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_reject_deadline_update_with_law_case_from_other_organization():
    tenant = build_tenant_fixture()
    local_case = LawCase.objects.create(
        title='Caso local para update de prazo',
        description='Caso local',
        client=tenant['client_b'],
        lawyer=tenant['lawyer_b'],
        organization=tenant['org_b'],
        status='open',
    )
    foreign_case = LawCase.objects.create(
        title='Caso externo para update de prazo',
        description='Caso externo',
        client=tenant['client_a'],
        lawyer=tenant['lawyer_a'],
        organization=tenant['org_a'],
        status='open',
    )
    deadline = Deadline.objects.create(
        law_case=local_case,
        due_date='2030-01-01T12:00:00Z',
        completed=False,
        organization=tenant['org_b'],
    )

    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.patch(
        f'/api/v1/deadlines/{deadline.id}/',
        {'law_case_id': str(foreign_case.id)},
        format='json',
    )

    assert response.status_code in (400, 403)
    deadline.refresh_from_db()
    assert deadline.law_case_id == local_case.id


@pytest.mark.django_db
def test_reject_document_creation_with_law_case_from_other_organization():
    tenant = build_tenant_fixture()
    foreign_case = LawCase.objects.create(
        title='Caso externo para documento',
        description='Caso base para documento cross-tenant',
        client=tenant['client_a'],
        lawyer=tenant['lawyer_a'],
        organization=tenant['org_a'],
        status='open',
    )

    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.post(
        '/api/v1/documents/',
        {
            'law_case_id': str(foreign_case.id),
            'type': 'internal',
            'content': 'Documento nao deveria ser aceite entre tenants',
        },
        format='json',
    )

    assert response.status_code in (400, 403)
    assert not Document.objects.filter(law_case=foreign_case).exists()


@pytest.mark.django_db
def test_allow_document_creation_with_law_case_from_same_organization():
    tenant = build_tenant_fixture()
    local_case = LawCase.objects.create(
        title='Caso da organizacao B para documento',
        description='Caso base para documento valido',
        client=tenant['client_b'],
        lawyer=tenant['lawyer_b'],
        organization=tenant['org_b'],
        status='open',
    )

    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.post(
        '/api/v1/documents/',
        {
            'law_case_id': str(local_case.id),
            'type': 'internal',
            'content': 'Documento valido no mesmo tenant',
        },
        format='json',
    )

    assert response.status_code == 201
    assert Document.objects.filter(law_case=local_case, organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_reject_document_update_with_law_case_from_other_organization():
    tenant = build_tenant_fixture()
    local_case = LawCase.objects.create(
        title='Caso local para update de documento',
        description='Caso local',
        client=tenant['client_b'],
        lawyer=tenant['lawyer_b'],
        organization=tenant['org_b'],
        status='open',
    )
    foreign_case = LawCase.objects.create(
        title='Caso externo para update de documento',
        description='Caso externo',
        client=tenant['client_a'],
        lawyer=tenant['lawyer_a'],
        organization=tenant['org_a'],
        status='open',
    )
    document = Document.objects.create(
        law_case=local_case,
        type='internal',
        content='Documento local',
        version=1,
        organization=tenant['org_b'],
    )

    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')

    response = client.patch(
        f'/api/v1/documents/{document.id}/',
        {'law_case_id': str(foreign_case.id)},
        format='json',
    )

    assert response.status_code in (400, 403)
    document.refresh_from_db()
    assert document.law_case_id == local_case.id
