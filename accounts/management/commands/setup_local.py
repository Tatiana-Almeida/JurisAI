from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Executa migrações e popula dados iniciais para desenvolvimento local'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Executando migrações...'))
        call_command('migrate', '--noinput')

        self.stdout.write(self.style.NOTICE('Gerando dados iniciais de demonstração...'))
        call_command('seed_demo')

        self.stdout.write(self.style.SUCCESS('Configuração local concluída.'))
