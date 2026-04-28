import hashlib
import hmac
import json
import time

import pytest
from django.db import connection
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from billing.models import Payment, Subscription
from organizations.models import Organization


def build_client():
    client = APIClient()
    client.raise_request_exception = False
    return client


def subscription_table_exists():
    return Subscription._meta.db_table in connection.introspection.table_names()


def build_payment_succeeded_payload(organization_id, event_id='evt_test_paid_001'):
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


def build_subscription_updated_payload(organization_id, event_id='evt_test_sub_001'):
    return {
        'id': event_id,
        'type': 'customer.subscription.updated',
        'data': {
            'object': {
                'id': 'sub_test_001',
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
    return json.dumps(payload, separators=(',', ':'))


def build_stripe_like_signature(payload_body, secret='test-secret', timestamp=None):
    timestamp = str(timestamp or int(time.time()))
    signed_payload = f'{timestamp}.{payload_body}'.encode('utf-8')
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()
    return f't={timestamp},v1={expected_signature}'


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_webhook_without_signature_should_be_rejected_and_not_create_payment():
    organization = Organization.objects.create(name='Org Billing A', plan='free')
    client = build_client()
    payload = build_payment_succeeded_payload(organization.id)

    response = client.post(
        reverse('billing_webhook'),
        serialize_payload(payload),
        content_type='application/json',
    )

    assert response.status_code in (400, 403)
    assert Payment.objects.count() == 0


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_webhook_with_invalid_signature_should_be_rejected_and_not_create_payment():
    organization = Organization.objects.create(name='Org Billing B', plan='free')
    client = build_client()
    payload = build_payment_succeeded_payload(organization.id, event_id='evt_invalid_sig')

    response = client.post(
        reverse('billing_webhook'),
        serialize_payload(payload),
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE='invalid-signature',
    )

    assert response.status_code in (400, 403)
    assert Payment.objects.count() == 0


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_invalid_payload_should_not_change_financial_state():
    organization = Organization.objects.create(name='Org Billing C', plan='free')
    client = build_client()
    payload = {
        'id': 'evt_invalid_payload',
        'type': 'invoice.payment_succeeded',
        'data': {'object': {'metadata': {'organization_id': str(organization.id)}}},
    }
    payload_body = serialize_payload(payload)

    response = client.post(
        reverse('billing_webhook'),
        payload_body,
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE=build_stripe_like_signature(payload_body),
    )

    assert response.status_code == 400
    assert Payment.objects.count() == 0
    if subscription_table_exists():
        assert Subscription.objects.count() == 0


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_unknown_event_should_not_change_financial_state():
    organization = Organization.objects.create(name='Org Billing D', plan='free')
    client = build_client()
    payload = {
        'id': 'evt_unknown_001',
        'type': 'billing.unknown',
        'data': {
            'object': {
                'metadata': {'organization_id': str(organization.id)},
                'amount_paid': 2000,
            }
        },
    }
    payload_body = serialize_payload(payload)

    response = client.post(
        reverse('billing_webhook'),
        payload_body,
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE=build_stripe_like_signature(payload_body),
    )

    assert response.status_code == 200
    assert response.data['received'] is True
    assert Payment.objects.count() == 0
    if subscription_table_exists():
        assert Subscription.objects.count() == 0


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_valid_signed_payment_success_event_should_be_accepted_after_correction():
    organization = Organization.objects.create(name='Org Billing E', plan='free')
    payload = build_payment_succeeded_payload(organization.id, event_id='evt_signed_valid')
    client = build_client()
    payload_body = serialize_payload(payload)

    response = client.post(
        reverse('billing_webhook'),
        payload_body,
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE=build_stripe_like_signature(payload_body),
    )

    assert response.status_code == 200
    assert Payment.objects.count() == 1
    payment = Payment.objects.get()
    assert payment.organization == organization
    assert str(payment.amount) == '15.00'
    assert payment.status == 'paid'


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_repeated_event_id_should_be_idempotent_after_correction():
    organization = Organization.objects.create(name='Org Billing F', plan='free')
    payload = build_payment_succeeded_payload(organization.id, event_id='evt_repeat_001')
    client = build_client()
    payload_body = serialize_payload(payload)
    signature = build_stripe_like_signature(payload_body)

    first_response = client.post(
        reverse('billing_webhook'),
        payload_body,
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE=signature,
    )
    second_response = client.post(
        reverse('billing_webhook'),
        payload_body,
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE=signature,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert Payment.objects.count() == 1


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret', STRIPE_WEBHOOK_TOLERANCE_SECONDS=300)
def test_webhook_with_old_timestamp_should_be_rejected_and_not_create_payment():
    organization = Organization.objects.create(name='Org Billing H', plan='free')
    payload = build_payment_succeeded_payload(organization.id, event_id='evt_old_timestamp')
    client = build_client()
    payload_body = serialize_payload(payload)

    response = client.post(
        reverse('billing_webhook'),
        payload_body,
        content_type='application/json',
        HTTP_STRIPE_SIGNATURE=build_stripe_like_signature(payload_body, timestamp='1700000000'),
    )

    assert response.status_code == 400
    assert Payment.objects.count() == 0


@pytest.mark.django_db
@override_settings(STRIPE_WEBHOOK_SECRET='test-secret')
def test_unsigned_subscription_update_should_be_rejected_and_not_change_subscription():
    organization = Organization.objects.create(name='Org Billing G', plan='free')
    client = build_client()

    response = client.post(
        reverse('billing_webhook'),
        build_subscription_updated_payload(organization.id, event_id='evt_sub_unsigned'),
        format='json',
    )

    assert response.status_code in (400, 403)
    if subscription_table_exists():
        assert Subscription.objects.count() == 0
