import pytest

from client_portal.models import ClientCaseVisibility, ClientDocumentShare
from documents.models import Document
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


@pytest.mark.django_db
def test_client_does_not_see_case_without_visibility():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['client_b'])

    response = client.get('/api/v1/client-portal/cases/')

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_client_sees_case_with_visibility():
    tenant = build_service_tenant_fixture()
    ClientCaseVisibility.objects.create(
        organization=tenant['org_b'],
        client=tenant['client_b'],
        law_case=tenant['case_b'],
        can_view=True,
    )
    client = authenticated_client(tenant['client_b'])

    response = client.get('/api/v1/client-portal/cases/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == str(tenant['case_b'].id)


@pytest.mark.django_db
def test_client_does_not_see_document_not_shared():
    tenant = build_service_tenant_fixture()
    Document.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        type='internal',
        content='Nao partilhado',
        version=1,
    )
    client = authenticated_client(tenant['client_b'])

    response = client.get('/api/v1/client-portal/documents/')

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_client_sees_document_when_shared():
    tenant = build_service_tenant_fixture()
    document = Document.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        type='internal',
        content='Partilhado',
        version=1,
    )
    ClientDocumentShare.objects.create(
        organization=tenant['org_b'],
        client=tenant['client_b'],
        document=document,
        shared_by=tenant['admin_b'],
        can_download=True,
    )
    client = authenticated_client(tenant['client_b'])

    response = client.get('/api/v1/client-portal/documents/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == str(document.id)


@pytest.mark.django_db
def test_client_does_not_access_data_from_other_organization():
    tenant = build_service_tenant_fixture()
    ClientCaseVisibility.objects.create(
        organization=tenant['org_a'],
        client=tenant['client_a'],
        law_case=tenant['case_a'],
        can_view=True,
    )
    client = authenticated_client(tenant['client_b'])

    response = client.get('/api/v1/client-portal/cases/')

    assert response.status_code == 200
    assert response.data == []

