import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError

from organizations.models import Organization

User = get_user_model()


def _is_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


class Command(BaseCommand):
    help = "Creates or updates an opt-in superuser from environment variables."

    def handle(self, *args, **options):
        if not _is_truthy(os.getenv("DJANGO_CREATE_SUPERUSER", "False")):
            self.stdout.write(
                self.style.WARNING(
                    "Skipping bootstrap_superuser because DJANGO_CREATE_SUPERUSER is not enabled."
                )
            )
            return

        admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
        admin_password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "")
        admin_name = os.getenv("DJANGO_SUPERUSER_NAME", "Render Administrator").strip()
        organization_name = os.getenv(
            "DJANGO_SUPERUSER_ORGANIZATION", "Render Bootstrap Organization"
        ).strip()

        if not admin_email or not admin_password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping bootstrap_superuser because DJANGO_SUPERUSER_EMAIL or DJANGO_SUPERUSER_PASSWORD is missing."
                )
            )
            return

        try:
            table_names = set(connection.introspection.table_names())
        except (OperationalError, ProgrammingError) as exc:
            self.stdout.write(
                self.style.WARNING(
                    f"Skipping bootstrap_superuser because database metadata is unavailable: {exc}"
                )
            )
            return

        required_tables = {"accounts_user", "organizations_organization"}
        if not required_tables.issubset(table_names):
            self.stdout.write(
                self.style.WARNING(
                    "Skipping bootstrap_superuser because required tables are not available yet."
                )
            )
            return

        organization, created_org = Organization.objects.get_or_create(
            name=organization_name,
            defaults={"plan": "enterprise"},
        )
        if created_org:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Bootstrap organization created: {organization.name}"
                )
            )

        user, created_user = User.objects.get_or_create(
            email=admin_email,
            defaults={
                "name": admin_name,
                "organization": organization,
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        changed_fields = set()
        if created_user:
            self.stdout.write(
                self.style.SUCCESS(f"Bootstrap superuser created: {user.email}")
            )
        if user.name != admin_name:
            user.name = admin_name
            changed_fields.add("name")
        if created_user and user.organization_id != organization.id:
            user.organization = organization
            changed_fields.add("organization")
        if user.role != "admin":
            user.role = "admin"
            changed_fields.add("role")
        if not user.is_staff:
            user.is_staff = True
            changed_fields.add("is_staff")
        if not user.is_superuser:
            user.is_superuser = True
            changed_fields.add("is_superuser")
        if not user.is_active:
            user.is_active = True
            changed_fields.add("is_active")
        if not user.check_password(admin_password):
            user.set_password(admin_password)
            changed_fields.add("password")

        if changed_fields:
            update_fields = [field for field in changed_fields if field != "password"]
            if "password" in changed_fields:
                update_fields.append("password")
            user.save(update_fields=update_fields or None)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Bootstrap superuser ensured with updates: {', '.join(sorted(changed_fields))}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Bootstrap superuser already configured: {user.email}"
                )
            )
