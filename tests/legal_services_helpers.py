from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from deadlines.models import Deadline
from documents.models import Document
from law_cases.models import LawCase
from organizations.models import Organization


def authenticate(client, email, password='strongpass123'):
    token_response = client.post(
        reverse('token_obtain_pair'),
        {'email': email, 'password': password},
        format='json',
    )
    assert token_response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")


def build_service_tenant_fixture():
    org_a = Organization.objects.create(name='Org A Expanded Services', plan='free')
    org_b = Organization.objects.create(name='Org B Expanded Services', plan='growth')

    admin_a = User.objects.create_user(
        email='admin-a-services@example.com',
        password='strongpass123',
        name='Admin A Services',
        organization=org_a,
        role='admin',
        is_staff=True,
    )
    admin_b = User.objects.create_user(
        email='admin-b-services@example.com',
        password='strongpass123',
        name='Admin B Services',
        organization=org_b,
        role='admin',
        is_staff=True,
    )
    lawyer_a = User.objects.create_user(
        email='lawyer-a-services@example.com',
        password='strongpass123',
        name='Lawyer A Services',
        organization=org_a,
        role='advogado',
    )
    lawyer_b = User.objects.create_user(
        email='lawyer-b-services@example.com',
        password='strongpass123',
        name='Lawyer B Services',
        organization=org_b,
        role='advogado',
    )
    client_a = User.objects.create_user(
        email='client-a-services@example.com',
        password='strongpass123',
        name='Client A Services',
        organization=org_a,
        role='cliente',
    )
    client_b = User.objects.create_user(
        email='client-b-services@example.com',
        password='strongpass123',
        name='Client B Services',
        organization=org_b,
        role='cliente',
    )

    case_a = LawCase.objects.create(
        title='Caso A Expanded',
        description='Caso tenant A',
        client=client_a,
        lawyer=lawyer_a,
        organization=org_a,
        status='open',
    )
    case_b = LawCase.objects.create(
        title='Caso B Expanded',
        description='Caso tenant B',
        client=client_b,
        lawyer=lawyer_b,
        organization=org_b,
        status='open',
    )

    return {
        'org_a': org_a,
        'org_b': org_b,
        'admin_a': admin_a,
        'admin_b': admin_b,
        'lawyer_a': lawyer_a,
        'lawyer_b': lawyer_b,
        'client_a': client_a,
        'client_b': client_b,
        'case_a': case_a,
        'case_b': case_b,
    }


def authenticated_client(user):
    client = APIClient()
    authenticate(client, user.email)
    return client


def seed_dashboard_records(tenant):
    Deadline.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        due_date='2030-01-10T10:00:00Z',
        completed=False,
    )
    Deadline.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        due_date='2020-01-10T10:00:00Z',
        completed=False,
    )
    Document.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        type='internal',
        content='Documento dashboard B',
        version=1,
    )
