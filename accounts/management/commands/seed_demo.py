from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from organizations.models import Organization
from law_cases.models import LawCase
from deadlines.models import Deadline
from documents.models import Document

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais de demonstração para JurisAI'

    def handle(self, *args, **options):
        organization, _ = Organization.objects.get_or_create(
            name='Escritorio Demo',
            defaults={'plan': 'free'}
        )

        admin, created = User.objects.get_or_create(
            email='admin@jurisai.local',
            defaults={
                'name': 'Administrador JurisAI',
                'organization': organization,
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('Admin12345!')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin criado: admin@jurisai.local'))
        else:
            self.stdout.write(self.style.WARNING('Admin já existe: admin@jurisai.local'))

        lawyers = []
        for i in range(1, 3):
            email = f'advogado{i}@jurisai.local'
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'name': f'Advogado {i}',
                    'organization': organization,
                    'role': 'advogado',
                }
            )
            if created:
                user.set_password('Advogado123!')
                user.save()
            lawyers.append(user)

        clients = []
        for i in range(1, 3):
            email = f'cliente{i}@jurisai.local'
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'name': f'Cliente {i}',
                    'organization': organization,
                    'role': 'cliente',
                }
            )
            if created:
                user.set_password('Cliente123!')
                user.save()
            clients.append(user)

        cases = []
        case_data = [
            ('Ação Trabalhista', 'Reclamação de horas extras e adicional.', clients[0], lawyers[0], 'open'),
            ('Cobrança de Honorários', 'Disputa sobre valores contratuais.', clients[1], lawyers[1], 'in_progress'),
            ('Revisão Contratual', 'Análise de cláusulas de contrato de prestação de serviços.', clients[0], lawyers[1], 'closed'),
        ]
        for title, description, client, lawyer, status in case_data:
            case, created = LawCase.objects.get_or_create(
                title=title,
                organization=organization,
                defaults={
                    'description': description,
                    'client': client,
                    'lawyer': lawyer,
                    'status': status,
                }
            )
            cases.append(case)
        self.stdout.write(self.style.SUCCESS(f'Criados {len(cases)} processos jurídicos'))

        deadlines = []
        offsets = [1, 2, 3, 5, 7]
        for i, offset in enumerate(offsets):
            case = cases[i % len(cases)]
            deadline, created = Deadline.objects.get_or_create(
                law_case=case,
                due_date=timezone.now() + timezone.timedelta(days=offset),
                organization=organization,
                defaults={'completed': i % 2 == 0},
            )
            deadlines.append(deadline)
        self.stdout.write(self.style.SUCCESS(f'Criados {len(deadlines)} prazos'))

        documents = []
        document_data = [
            (cases[0], 'petition', 'Petição inicial sobre horas extras'),
            (cases[1], 'contract', 'Contrato de honorários e condições de prestação'),
            (cases[2], 'internal', 'Parecer interno para revisão contratual'),
        ]
        for law_case, doc_type, content in document_data:
            document, created = Document.objects.get_or_create(
                law_case=law_case,
                type=doc_type,
                version=1,
                organization=organization,
                defaults={'content': content},
            )
            documents.append(document)
        self.stdout.write(self.style.SUCCESS(f'Criados {len(documents)} documentos'))

        self.stdout.write(self.style.SUCCESS('Dados iniciais de demonstração carregados com sucesso.'))
