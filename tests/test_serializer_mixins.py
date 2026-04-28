from types import SimpleNamespace

import pytest

from accounts.models import User
from accounts.serializers import UserSerializer
from billing.serializers import PaymentSerializer
from organizations.models import Organization


@pytest.mark.django_db
def test_user_serializer_uses_context_organization_for_organization_id():
    organization = Organization.objects.create(name='Org Serializer Context', plan='free')

    serializer = UserSerializer(
        data={
            'name': 'Novo Usuario',
            'email': 'novo@example.com',
            'password': 'strongpass123',
            'role': 'admin',
        },
        context={'organization': organization},
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['organization_id'] == str(organization.id)


@pytest.mark.django_db
def test_payment_serializer_uses_authenticated_request_organization_for_organization_id():
    organization = Organization.objects.create(name='Org Serializer Request', plan='free')
    user = User.objects.create_user(
        email='billing@example.com',
        password='strongpass123',
        name='Billing User',
        organization=organization,
        role='admin',
    )

    serializer = PaymentSerializer(
        data={'amount': '10.00', 'method': 'pix'},
        context={'request': SimpleNamespace(user=user)},
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['organization_id'] == str(organization.id)
