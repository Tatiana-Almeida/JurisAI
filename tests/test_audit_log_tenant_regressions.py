import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from audit_logs.models import AuditLog
from organizations.models import Organization


def authenticate(client, email, password):
    token_response = client.post(
        reverse('token_obtain_pair'),
        {'email': email, 'password': password},
        format='json',
    )
    assert token_response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")


def build_audit_fixture():
    org_a = Organization.objects.create(name='Org Audit A', plan='free')
    org_b = Organization.objects.create(name='Org Audit B', plan='free')

    admin_a = User.objects.create_user(
        email='admin-a-audit@example.com',
        password='strongpass123',
        name='Admin Audit A',
        organization=org_a,
        role='admin',
        is_staff=True,
    )
    admin_b = User.objects.create_user(
        email='admin-b-audit@example.com',
        password='strongpass123',
        name='Admin Audit B',
        organization=org_b,
        role='admin',
        is_staff=True,
    )
    lawyer_b = User.objects.create_user(
        email='lawyer-b-audit@example.com',
        password='strongpass123',
        name='Lawyer Audit B',
        organization=org_b,
        role='advogado',
    )

    log_a = AuditLog.objects.create(
        user=admin_a,
        action='update',
        entity='law_cases.lawcase',
        before={'status': 'open'},
        after={'status': 'closed'},
        ip='10.0.0.1',
    )
    log_b = AuditLog.objects.create(
        user=admin_b,
        action='create',
        entity='documents.document',
        before=None,
        after={'type': 'internal'},
        ip='10.0.0.2',
    )
    log_without_organization = AuditLog.objects.create(
        user=None,
        action='delete',
        entity='notifications.notification',
        before={'id': 'ghost-log'},
        after=None,
        ip='10.0.0.3',
    )

    return {
        'org_a': org_a,
        'org_b': org_b,
        'admin_a': admin_a,
        'admin_b': admin_b,
        'lawyer_b': lawyer_b,
        'log_a': log_a,
        'log_b': log_b,
        'log_without_organization': log_without_organization,
    }


@pytest.mark.django_db
def test_admin_should_not_list_audit_logs_from_other_organizations():
    fixture = build_audit_fixture()
    client = APIClient()
    authenticate(client, fixture['admin_b'].email, 'strongpass123')

    response = client.get('/api/v1/audit-logs/')

    assert response.status_code == 200
    result_ids = {item['id'] for item in response.data['results']}
    assert str(fixture['log_b'].id) in result_ids
    assert str(fixture['log_a'].id) not in result_ids
    assert str(fixture['log_without_organization'].id) not in result_ids


@pytest.mark.django_db
def test_admin_should_not_retrieve_audit_log_from_other_organization():
    fixture = build_audit_fixture()
    client = APIClient()
    authenticate(client, fixture['admin_b'].email, 'strongpass123')

    response = client.get(f"/api/v1/audit-logs/{fixture['log_a'].id}/")

    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_non_admin_cannot_list_audit_logs():
    fixture = build_audit_fixture()
    client = APIClient()
    authenticate(client, fixture['lawyer_b'].email, 'strongpass123')

    response = client.get('/api/v1/audit-logs/')

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_should_not_list_audit_logs_without_organization():
    fixture = build_audit_fixture()
    client = APIClient()
    authenticate(client, fixture['admin_b'].email, 'strongpass123')

    response = client.get('/api/v1/audit-logs/')

    assert response.status_code == 200
    result_ids = {item['id'] for item in response.data['results']}
    assert str(fixture['log_without_organization'].id) not in result_ids
