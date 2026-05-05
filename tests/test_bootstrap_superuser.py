import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from organizations.models import Organization

User = get_user_model()


@pytest.mark.django_db
def test_bootstrap_superuser_skips_when_flag_is_disabled(monkeypatch):
    monkeypatch.setenv("DJANGO_CREATE_SUPERUSER", "False")
    monkeypatch.delenv("DJANGO_SUPERUSER_EMAIL", raising=False)
    monkeypatch.delenv("DJANGO_SUPERUSER_PASSWORD", raising=False)

    call_command("bootstrap_superuser")

    assert User.objects.count() == 0
    assert Organization.objects.count() == 0


@pytest.mark.django_db
def test_bootstrap_superuser_creates_org_and_admin(monkeypatch):
    monkeypatch.setenv("DJANGO_CREATE_SUPERUSER", "True")
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "render-admin@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("DJANGO_SUPERUSER_NAME", "Render Admin")
    monkeypatch.setenv("DJANGO_SUPERUSER_ORGANIZATION", "Render Bootstrap Org")

    call_command("bootstrap_superuser")

    user = User.objects.get(email="render-admin@example.com")
    organization = Organization.objects.get(name="Render Bootstrap Org")

    assert user.organization == organization
    assert user.name == "Render Admin"
    assert user.role == "admin"
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.check_password("StrongPass123!")
    assert organization.plan == "enterprise"


@pytest.mark.django_db
def test_bootstrap_superuser_is_idempotent_and_repairs_flags(monkeypatch):
    organization = Organization.objects.create(name="Existing Org", plan="free")
    user = User.objects.create_user(
        email="render-admin@example.com",
        password="old-password",
        name="Legacy Admin",
        organization=organization,
        role="cliente",
        is_staff=False,
        is_superuser=False,
    )

    monkeypatch.setenv("DJANGO_CREATE_SUPERUSER", "True")
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "render-admin@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "NewStrongPass123!")
    monkeypatch.setenv("DJANGO_SUPERUSER_NAME", "Render Admin")

    call_command("bootstrap_superuser")

    user.refresh_from_db()

    assert User.objects.count() == 1
    assert user.name == "Render Admin"
    assert user.role == "admin"
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_active is True
    assert user.organization == organization
    assert user.check_password("NewStrongPass123!")
