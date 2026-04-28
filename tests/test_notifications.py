import pytest

from notifications.models import Notification
from notifications.services import NotificationService
from notifications.tasks import send_pending_notifications
from organizations.models import Organization


@pytest.mark.django_db
def test_send_whatsapp_without_notification_keeps_legacy_mock_behavior():
    organization = Organization.objects.create(name='Org Notifications Legacy', plan='free')

    NotificationService().send_whatsapp(
        organization_id=organization.id,
        recipient='5511999999999',
        body='Mensagem mock',
    )

    notifications = Notification.objects.filter(organization=organization)
    assert notifications.count() == 1
    notification = notifications.get()
    assert notification.channel == 'whatsapp'
    assert notification.sent is True
    assert notification.subject == 'WhatsApp'


@pytest.mark.django_db
def test_send_pending_notifications_marks_existing_whatsapp_without_duplication():
    organization = Organization.objects.create(name='Org Notifications Task', plan='free')
    original = Notification.objects.create(
        organization=organization,
        channel='whatsapp',
        recipient='5511888888888',
        subject='WhatsApp',
        body='Mensagem pendente',
        sent=False,
    )

    send_pending_notifications()

    notifications = Notification.objects.filter(organization=organization)
    assert notifications.count() == 1

    original.refresh_from_db()
    assert original.sent is True
    assert original.sent_at is not None


@pytest.mark.django_db
def test_send_pending_notifications_keeps_email_path_behavior(monkeypatch):
    organization = Organization.objects.create(name='Org Notifications Email', plan='free')
    original = Notification.objects.create(
        organization=organization,
        channel='email',
        recipient='email@example.com',
        subject='Assunto',
        body='Mensagem email',
        sent=False,
    )

    captured = {}

    def fake_send_email(self, subject, message, recipient_list):
        captured['subject'] = subject
        captured['message'] = message
        captured['recipient_list'] = recipient_list

    monkeypatch.setattr(NotificationService, 'send_email', fake_send_email)

    send_pending_notifications()

    notifications = Notification.objects.filter(organization=organization)
    assert notifications.count() == 1

    original.refresh_from_db()
    assert original.sent is True
    assert original.sent_at is not None
    assert captured == {
        'subject': 'Assunto',
        'message': 'Mensagem email',
        'recipient_list': ['email@example.com'],
    }
