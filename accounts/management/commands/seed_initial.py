from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from organizations.models import Organization

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria organização e usuário admin iniciais para o sistema JurisAI'

    def add_arguments(self, parser):
        parser.add_argument('--organization-name', type=str, default='Escritorio Demo')
        parser.add_argument('--plan', type=str, default='free')
        parser.add_argument('--admin-email', type=str, default='admin@jurisai.local')
        parser.add_argument('--admin-password', type=str, default='Admin12345!')
        parser.add_argument('--admin-name', type=str, default='Administrador JurisAI')

    def handle(self, *args, **options):
        organization, created_org = Organization.objects.get_or_create(
            name=options['organization_name'],
            defaults={'plan': options['plan']}
        )
        if created_org:
            self.stdout.write(self.style.SUCCESS(f'Organização criada: {organization.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Organização existente: {organization.name}'))

        admin, created_user = User.objects.get_or_create(
            email=options['admin_email'],
            defaults={
                'name': options['admin_name'],
                'organization': organization,
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created_user:
            admin.set_password(options['admin_password'])
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Usuário admin criado: {admin.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Usuário admin existente: {admin.email}'))

        self.stdout.write(self.style.SUCCESS('Seed inicial executada com sucesso.'))
