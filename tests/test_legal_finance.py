import pytest

from legal_finance.models import Expense
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


@pytest.mark.django_db
def test_invoices_are_filtered_by_organization():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    client.post(
        '/api/v1/legal-finance/invoices/',
        {
            'law_case_id': str(tenant['case_b'].id),
            'client_id': str(tenant['client_b'].id),
            'invoice_number': 'INV-B-100',
            'amount': '2500.00',
            'status': 'open',
        },
        format='json',
    )
    other_client = authenticated_client(tenant['admin_a'])
    other_client.post(
        '/api/v1/legal-finance/invoices/',
        {
            'law_case_id': str(tenant['case_a'].id),
            'client_id': str(tenant['client_a'].id),
            'invoice_number': 'INV-A-100',
            'amount': '1000.00',
            'status': 'open',
        },
        format='json',
    )

    response = client.get('/api/v1/legal-finance/invoices/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['invoice_number'] == 'INV-B-100'


@pytest.mark.django_db
def test_payments_are_filtered_by_organization():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])
    invoice_response = client.post(
        '/api/v1/legal-finance/invoices/',
        {
            'law_case_id': str(tenant['case_b'].id),
            'client_id': str(tenant['client_b'].id),
            'invoice_number': 'INV-B-200',
            'amount': '500.00',
            'status': 'open',
        },
        format='json',
    )
    invoice_id = invoice_response.data['id']
    client.post(
        '/api/v1/legal-finance/payments/',
        {
            'invoice_id': invoice_id,
            'law_case_id': str(tenant['case_b'].id),
            'amount': '500.00',
            'payment_method': 'cash',
            'paid_at': '2030-01-10T10:00:00Z',
        },
        format='json',
    )
    other_client = authenticated_client(tenant['admin_a'])
    foreign_invoice = other_client.post(
        '/api/v1/legal-finance/invoices/',
        {
            'law_case_id': str(tenant['case_a'].id),
            'client_id': str(tenant['client_a'].id),
            'invoice_number': 'INV-A-200',
            'amount': '600.00',
            'status': 'open',
        },
        format='json',
    )
    other_client.post(
        '/api/v1/legal-finance/payments/',
        {
            'invoice_id': foreign_invoice.data['id'],
            'law_case_id': str(tenant['case_a'].id),
            'amount': '600.00',
            'payment_method': 'cash',
            'paid_at': '2030-01-10T10:00:00Z',
        },
        format='json',
    )

    response = client.get('/api/v1/legal-finance/payments/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['amount'] == '500.00'


@pytest.mark.django_db
def test_summary_does_not_mix_tenants():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])
    client.post(
        '/api/v1/legal-finance/invoices/',
        {
            'law_case_id': str(tenant['case_b'].id),
            'client_id': str(tenant['client_b'].id),
            'invoice_number': 'INV-B-300',
            'amount': '900.00',
            'status': 'open',
        },
        format='json',
    )
    other_client = authenticated_client(tenant['admin_a'])
    other_client.post(
        '/api/v1/legal-finance/invoices/',
        {
            'law_case_id': str(tenant['case_a'].id),
            'client_id': str(tenant['client_a'].id),
            'invoice_number': 'INV-A-300',
            'amount': '1500.00',
            'status': 'paid',
        },
        format='json',
    )

    response = client.get('/api/v1/legal-finance/summary/')

    assert response.status_code == 200
    assert response.data['total_invoices'] == 1
    assert response.data['open_invoices'] == 1
    assert response.data['paid_invoices'] == 0


@pytest.mark.django_db
def test_create_expense_linked_to_same_tenant_case():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        '/api/v1/legal-finance/expenses/',
        {
            'law_case_id': str(tenant['case_b'].id),
            'description': 'Taxa judicial',
            'amount': '120.00',
            'expense_date': '2030-01-05T09:00:00Z',
            'reimbursable': True,
        },
        format='json',
    )

    assert response.status_code == 201
    assert Expense.objects.filter(organization=tenant['org_b'], law_case=tenant['case_b']).count() == 1


@pytest.mark.django_db
def test_reject_case_from_other_tenant_when_creating_expense():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        '/api/v1/legal-finance/expenses/',
        {
            'law_case_id': str(tenant['case_a'].id),
            'description': 'Despesa indevida',
            'amount': '120.00',
            'expense_date': '2030-01-05T09:00:00Z',
            'reimbursable': False,
        },
        format='json',
    )

    assert response.status_code == 400
    assert Expense.objects.count() == 0
