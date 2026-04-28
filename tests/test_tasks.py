from datetime import timedelta

import pytest
from django.utils import timezone

from tasks.models import Task
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


@pytest.mark.django_db
def test_user_creates_task_only_in_own_organization():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        '/api/v1/tasks/',
        {
            'title': 'Preparar audiencia',
            'description': 'Tarefa do tenant B',
            'law_case_id': str(tenant['case_b'].id),
            'assigned_to_id': str(tenant['lawyer_b'].id),
            'priority': 'high',
            'due_date': (timezone.now() + timedelta(days=3)).isoformat(),
        },
        format='json',
    )

    assert response.status_code == 201
    task = Task.objects.get(title='Preparar audiencia')
    assert task.organization == tenant['org_b']
    assert task.law_case == tenant['case_b']


@pytest.mark.django_db
def test_user_does_not_list_tasks_from_other_organization():
    tenant = build_service_tenant_fixture()
    Task.objects.create(
        organization=tenant['org_a'],
        law_case=tenant['case_a'],
        title='Tarefa org A',
        created_by=tenant['admin_a'],
    )
    Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Tarefa org B',
        created_by=tenant['admin_b'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/tasks/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Tarefa org B'


@pytest.mark.django_db
def test_user_does_not_access_task_detail_from_other_organization():
    tenant = build_service_tenant_fixture()
    foreign_task = Task.objects.create(
        organization=tenant['org_a'],
        law_case=tenant['case_a'],
        title='Tarefa escondida',
        created_by=tenant['admin_a'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get(f'/api/v1/tasks/{foreign_task.id}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_comment_respects_organization():
    tenant = build_service_tenant_fixture()
    task = Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Tarefa comentavel',
        created_by=tenant['admin_b'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/tasks/{task.id}/comments/',
        {'message': 'Comentario interno'},
        format='json',
    )

    assert response.status_code == 201
    task.refresh_from_db()
    comment = task.comments.get()
    assert comment.organization == tenant['org_b']
    assert comment.author == tenant['admin_b']


@pytest.mark.django_db
def test_checklist_respects_organization():
    tenant = build_service_tenant_fixture()
    task = Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Tarefa checklist',
        created_by=tenant['admin_b'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/tasks/{task.id}/checklist/',
        {'title': 'Rever anexos'},
        format='json',
    )

    assert response.status_code == 201
    item = task.checklist_items.get()
    assert item.organization == tenant['org_b']
    assert item.title == 'Rever anexos'


@pytest.mark.django_db
def test_complete_task_updates_status_and_completed_at():
    tenant = build_service_tenant_fixture()
    task = Task.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Completar tarefa',
        created_by=tenant['admin_b'],
        status='pending',
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(f'/api/v1/tasks/{task.id}/complete/')

    assert response.status_code == 200
    task.refresh_from_db()
    assert task.status == 'completed'
    assert task.completed_at is not None
