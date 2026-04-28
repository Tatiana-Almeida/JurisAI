from datetime import timedelta

import pytest
from django.utils import timezone

from calendar_events.models import CalendarEvent
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


@pytest.mark.django_db
def test_events_are_filtered_by_organization():
    tenant = build_service_tenant_fixture()
    now = timezone.now()
    CalendarEvent.objects.create(
        organization=tenant['org_a'],
        law_case=tenant['case_a'],
        title='Evento A',
        created_by=tenant['admin_a'],
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )
    CalendarEvent.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Evento B',
        created_by=tenant['admin_b'],
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/calendar/events/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Evento B'


@pytest.mark.django_db
def test_upcoming_returns_only_future_events_for_tenant():
    tenant = build_service_tenant_fixture()
    now = timezone.now()
    CalendarEvent.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Passado',
        created_by=tenant['admin_b'],
        start_at=now - timedelta(days=1),
        end_at=now - timedelta(days=1, hours=-1),
    )
    CalendarEvent.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Futuro',
        created_by=tenant['admin_b'],
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/calendar/events/upcoming/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Futuro'


@pytest.mark.django_db
def test_month_returns_only_month_events_for_tenant():
    tenant = build_service_tenant_fixture()
    now = timezone.now()
    CalendarEvent.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Mes atual',
        created_by=tenant['admin_b'],
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )
    CalendarEvent.objects.create(
        organization=tenant['org_b'],
        law_case=tenant['case_b'],
        title='Outro mes',
        created_by=tenant['admin_b'],
        start_at=(now + timedelta(days=40)),
        end_at=(now + timedelta(days=40, hours=1)),
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get(f'/api/v1/calendar/events/month/?month={now.month}&year={now.year}')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Mes atual'


@pytest.mark.django_db
def test_user_does_not_access_other_tenant_event():
    tenant = build_service_tenant_fixture()
    now = timezone.now()
    foreign_event = CalendarEvent.objects.create(
        organization=tenant['org_a'],
        law_case=tenant['case_a'],
        title='Evento privado',
        created_by=tenant['admin_a'],
        start_at=now + timedelta(days=2),
        end_at=now + timedelta(days=2, hours=1),
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get(f'/api/v1/calendar/events/{foreign_event.id}/')

    assert response.status_code == 404

