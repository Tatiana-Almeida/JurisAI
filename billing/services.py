import hashlib
import hmac
import json
from datetime import timezone as datetime_timezone
from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from billing.models import BillingWebhookEvent, Payment, Subscription
from organizations.models import Organization


def parse_stripe_signature_header(signature_header):
    if not signature_header:
        return None, []

    timestamp = None
    signatures = []
    for part in signature_header.split(','):
        key, _, value = part.strip().partition('=')
        if key == 't' and value:
            timestamp = value
        elif key == 'v1' and value:
            signatures.append(value)
    return timestamp, signatures


def compute_stripe_signature(payload_body, secret, timestamp):
    signed_payload = f'{timestamp}.{payload_body.decode("utf-8")}'.encode('utf-8')
    return hmac.new(
        secret.encode('utf-8'),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()


def verify_stripe_signature(payload_body, signature_header, secret):
    if not secret or not signature_header or not payload_body:
        return False

    timestamp, signatures = parse_stripe_signature_header(signature_header)
    if not timestamp or not signatures:
        return False

    expected_signature = compute_stripe_signature(payload_body, secret, timestamp)
    return any(hmac.compare_digest(expected_signature, candidate) for candidate in signatures)


def get_stripe_signature_timestamp(signature_header):
    timestamp, _ = parse_stripe_signature_header(signature_header)
    if not timestamp:
        return None
    try:
        return int(timestamp)
    except (TypeError, ValueError):
        return None


def validate_stripe_timestamp(signature_header, tolerance_seconds):
    timestamp = get_stripe_signature_timestamp(signature_header)
    if timestamp is None:
        return False, None

    now_ts = int(timezone.now().timestamp())
    if abs(now_ts - timestamp) > tolerance_seconds:
        return False, timestamp
    return True, timestamp


def parse_webhook_payload(payload_body):
    return json.loads(payload_body.decode('utf-8'))


def get_webhook_event_id(event):
    return event.get('id')


def get_webhook_event_type(event):
    return event.get('type')


def get_webhook_event_object(event):
    return event.get('data', {}).get('object', {})


def get_organization_id_from_webhook_object(event_object):
    metadata = event_object.get('metadata', {})
    return metadata.get('organization_id') or event_object.get('customer')


def resolve_webhook_organization(event_object):
    organization_id = get_organization_id_from_webhook_object(event_object)
    if not organization_id:
        return None
    return Organization.objects.filter(id=organization_id).first()


@dataclass
class BillingWebhookProcessResult:
    outcome: str
    event_type: str


def process_billing_webhook_event(
    *,
    event_id,
    event_type,
    payload,
    payload_body,
    signature_timestamp,
    organization,
    subscription_id=None,
    subscription_status=None,
):
    payload_hash = hashlib.sha256(payload_body).hexdigest()
    signature_datetime = timezone.datetime.fromtimestamp(signature_timestamp, tz=datetime_timezone.utc)

    try:
        with transaction.atomic():
            BillingWebhookEvent.objects.create(
                event_id=event_id,
                event_type=event_type,
                organization=organization,
                payload_hash=payload_hash,
                signature_timestamp=signature_datetime,
            )

            if event_type == 'invoice.payment_succeeded' and organization:
                amount = payload.get('amount_paid', 0) / 100
                Payment.objects.create(
                    organization=organization,
                    amount=amount,
                    status='paid',
                    method='credit_card',
                )
            elif event_type == 'invoice.payment_failed' and organization:
                Payment.objects.create(
                    organization=organization,
                    amount=payload.get('amount_due', 0) / 100,
                    status='failed',
                    method='credit_card',
                )
            elif event_type == 'customer.subscription.updated' and organization:
                plan = payload.get('items', {}).get('data', [{}])[0].get('plan', {}).get('nickname', '')
                current_period_start = payload.get('current_period_start')
                current_period_end = payload.get('current_period_end')
                Subscription.objects.update_or_create(
                    stripe_subscription_id=subscription_id,
                    organization=organization,
                    defaults={
                        'status': subscription_status,
                        'plan': plan,
                        'current_period_start': current_period_start and timezone.datetime.fromtimestamp(current_period_start, tz=datetime_timezone.utc),
                        'current_period_end': current_period_end and timezone.datetime.fromtimestamp(current_period_end, tz=datetime_timezone.utc),
                    },
                )
    except IntegrityError:
        return BillingWebhookProcessResult(outcome='duplicate', event_type=event_type)

    return BillingWebhookProcessResult(outcome='processed', event_type=event_type)
