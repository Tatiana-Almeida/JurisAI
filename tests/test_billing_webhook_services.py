import json
from unittest.mock import patch

import pytest
from django.db import connection

from billing.models import BillingWebhookEvent, Payment, Subscription
from billing.services import process_billing_webhook_event
from organizations.models import Organization


def build_payment_succeeded_payload(organization_id, event_id='evt_service_paid_001'):
    return {
        'id': event_id,
        'type': 'invoice.payment_succeeded',
        'data': {
            'object': {
                'metadata': {'organization_id': str(organization_id)},
                'amount_paid': 1500,
            }
        },
    }


def build_subscription_updated_payload(organization_id, event_id='evt_service_sub_001'):
    return {
        'id': event_id,
        'type': 'customer.subscription.updated',
        'data': {
            'object': {
                'id': 'sub_service_001',
                'customer': str(organization_id),
                'status': 'active',
                'items': {
                    'data': [
                        {
                            'plan': {
                                'nickname': 'growth',
                            }
                        }
                    ]
                },
                'current_period_start': 1704067200,
                'current_period_end': 1706745600,
            }
        },
    }


def serialize_payload(payload):
    return json.dumps(payload, separators=(',', ':')).encode('utf-8')


def subscription_table_exists():
    return Subscription._meta.db_table in connection.introspection.table_names()


@pytest.mark.django_db
def test_process_billing_webhook_event_processes_new_payment_event():
    organization = Organization.objects.create(name='Org Service A', plan='free')
    event = build_payment_succeeded_payload(organization.id, event_id='evt_service_new_001')
    payload = event['data']['object']

    result = process_billing_webhook_event(
        event_id=event['id'],
        event_type=event['type'],
        payload=payload,
        payload_body=serialize_payload(event),
        signature_timestamp=1704067200,
        organization=organization,
    )

    assert result.outcome == 'processed'
    assert result.event_type == 'invoice.payment_succeeded'
    assert BillingWebhookEvent.objects.count() == 1
    assert BillingWebhookEvent.objects.get().event_id == 'evt_service_new_001'
    assert Payment.objects.count() == 1


@pytest.mark.django_db
def test_process_billing_webhook_event_treats_duplicate_as_idempotent():
    organization = Organization.objects.create(name='Org Service B', plan='free')
    event = build_payment_succeeded_payload(organization.id, event_id='evt_service_dup_001')
    payload_body = serialize_payload(event)
    payload = event['data']['object']

    first_result = process_billing_webhook_event(
        event_id=event['id'],
        event_type=event['type'],
        payload=payload,
        payload_body=payload_body,
        signature_timestamp=1704067200,
        organization=organization,
    )
    second_result = process_billing_webhook_event(
        event_id=event['id'],
        event_type=event['type'],
        payload=payload,
        payload_body=payload_body,
        signature_timestamp=1704067200,
        organization=organization,
    )

    assert first_result.outcome == 'processed'
    assert second_result.outcome == 'duplicate'
    assert BillingWebhookEvent.objects.count() == 1
    assert Payment.objects.count() == 1


@pytest.mark.django_db
def test_process_billing_webhook_event_rolls_back_on_side_effect_error():
    organization = Organization.objects.create(name='Org Service C', plan='free')
    event = build_payment_succeeded_payload(organization.id, event_id='evt_service_rollback_001')
    payload = event['data']['object']

    with patch('billing.services.Payment.objects.create', side_effect=RuntimeError('boom')):
        with pytest.raises(RuntimeError, match='boom'):
            process_billing_webhook_event(
                event_id=event['id'],
                event_type=event['type'],
                payload=payload,
                payload_body=serialize_payload(event),
                signature_timestamp=1704067200,
                organization=organization,
            )

    assert BillingWebhookEvent.objects.count() == 0
    assert Payment.objects.count() == 0


@pytest.mark.django_db
def test_process_billing_webhook_event_keeps_unknown_event_without_side_effects():
    organization = Organization.objects.create(name='Org Service D', plan='free')
    event = {
        'id': 'evt_service_unknown_001',
        'type': 'billing.unknown',
        'data': {
            'object': {
                'metadata': {'organization_id': str(organization.id)},
                'amount_paid': 2000,
            }
        },
    }

    result = process_billing_webhook_event(
        event_id=event['id'],
        event_type=event['type'],
        payload=event['data']['object'],
        payload_body=serialize_payload(event),
        signature_timestamp=1704067200,
        organization=organization,
    )

    assert result.outcome == 'processed'
    assert BillingWebhookEvent.objects.count() == 1
    assert Payment.objects.count() == 0
    if subscription_table_exists():
        assert Subscription.objects.count() == 0


@pytest.mark.django_db
def test_process_billing_webhook_event_updates_subscription_event():
    organization = Organization.objects.create(name='Org Service E', plan='free')
    event = build_subscription_updated_payload(organization.id, event_id='evt_service_sub_002')
    payload = event['data']['object']

    result = process_billing_webhook_event(
        event_id=event['id'],
        event_type=event['type'],
        payload=payload,
        payload_body=serialize_payload(event),
        signature_timestamp=1704067200,
        organization=organization,
        subscription_id=payload['id'],
        subscription_status=payload['status'],
    )

    assert result.outcome == 'processed'
    assert BillingWebhookEvent.objects.count() == 1
    assert Subscription.objects.count() == 1
    subscription = Subscription.objects.get()
    assert subscription.organization == organization
    assert subscription.stripe_subscription_id == 'sub_service_001'
    assert subscription.status == 'active'
