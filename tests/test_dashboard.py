from datetime import timedelta

import pytest
from django.utils import timezone

from deadlines.models import Deadline
from documents.models import Document
from legal_finance.models import ClientInvoice
from tasks.models import Task
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


@pytest.mark.django_db
def test_dashboard_summary_counts_are_correct_for_current_tenant():
    tenant = build_service_tenant_fixture()
    now = timezone.now()
    Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Pendente B',
        created_by=tenant['admin_b'],
        status='pending',
    )
    Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Concluida B',
        created_by=tenant['admin_b'],
        status='completed',
        completed_at=now,
    )
    Deadline.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        due_date=now + timedelta(days=2),
        completed=False,
    )
    Deadline.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        due_date=now - timedelta(days=2),
        completed=False,
    )
    Document.objects.create(
        law_case=tenant['case_b'],
        organization=tenant['org_b'],
        type='internal',
        content='Doc B',
        version=1,
    )
    ClientInvoice.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        client=tenant['client_b'],
        invoice_number='INV-B-001',
        amount='1000.00',
        status='open',
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/dashboard/summary/')

    assert response.status_code == 200
    assert response.data['total_cases'] == 1
    assert response.data['active_cases'] == 1
    assert response.data['total_documents'] == 1
    assert response.data['upcoming_deadlines'] == 1
    assert response.data['overdue_deadlines'] == 1
    assert response.data['pending_tasks'] == 1
    assert response.data['completed_tasks'] == 1
    assert response.data['pending_invoices'] == 1


@pytest.mark.django_db
def test_dashboard_does_not_mix_data_between_organizations():
    tenant = build_service_tenant_fixture()
    Task.objects.create(
        organization=tenant['org_a'],
        law_case=tenant['case_a'],
        title='Tarefa A',
        created_by=tenant['admin_a'],
        status='pending',
    )
    Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Tarefa B',
        created_by=tenant['admin_b'],
        status='pending',
    )
    client = authenticated_client(tenant['admin_b'])

    summary_response = client.get('/api/v1/dashboard/summary/')
    tasks_response = client.get('/api/v1/dashboard/tasks/')

    assert summary_response.status_code == 200
    assert summary_response.data['pending_tasks'] == 1
    assert tasks_response.status_code == 200
    assert len(tasks_response.data) == 1
    assert tasks_response.data[0]['title'] == 'Tarefa B'

