# Runtime And Scripts

## Comandos e pontos de execução

| Comando/arquivo | Finalidade | Estado |
|---|---|---|
| `python manage.py ...` | Administração Django | [CONFIRMADO_NO_CÓDIGO] |
| `gunicorn jurisai.wsgi:application --bind 0.0.0.0:8000 --workers 3` | Servir a aplicação web | [CONFIRMADO_NO_CÓDIGO] |
| `celery -A jurisai worker --loglevel=info` | Processar tarefas assíncronas | [CONFIRMADO_NO_CÓDIGO] |
| `celery -A jurisai flower --port=5555` | Interface de monitorização Celery | [CONFIRMADO_NO_CÓDIGO] |
| `python manage.py setup_local` | Rodar migrações e seed demo | [CONFIRMADO_NO_CÓDIGO] |
| `python manage.py seed_initial` | Criar organização/admin iniciais | [CONFIRMADO_NO_CÓDIGO] |
| `python manage.py seed_demo` | Criar dados de demonstração | [CONFIRMADO_NO_CÓDIGO] |

## Variáveis de ambiente esperadas

| Variável | Uso observado | Estado |
|---|---|---|
| `DJANGO_SECRET_KEY` | Secret key Django | [CONFIRMADO_NO_CÓDIGO] |
| `DJANGO_DEBUG` | Liga/desliga debug | [CONFIRMADO_NO_CÓDIGO] |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos | [CONFIRMADO_NO_CÓDIGO] |
| `DJANGO_USE_SQLITE` | Forçar SQLite | [CONFIRMADO_NO_CÓDIGO] |
| `POSTGRES_DB` | Nome do banco | [CONFIRMADO_NO_CÓDIGO] |
| `POSTGRES_USER` | Usuário do banco | [CONFIRMADO_NO_CÓDIGO] |
| `POSTGRES_PASSWORD` | Password do banco | [CONFIRMADO_NO_CÓDIGO] |
| `POSTGRES_HOST` | Host do banco | [CONFIRMADO_NO_CÓDIGO] |
| `POSTGRES_PORT` | Porta do banco | [CONFIRMADO_NO_CÓDIGO] |
| `EMAIL_HOST` | SMTP host | [CONFIRMADO_NO_CÓDIGO] |
| `EMAIL_PORT` | SMTP port | [CONFIRMADO_NO_CÓDIGO] |
| `EMAIL_HOST_USER` | SMTP user | [CONFIRMADO_NO_CÓDIGO] |
| `EMAIL_HOST_PASSWORD` | SMTP password | [CONFIRMADO_NO_CÓDIGO] |
| `EMAIL_USE_TLS` | TLS SMTP | [CONFIRMADO_NO_CÓDIGO] |
| `DEFAULT_FROM_EMAIL` | Remetente padrão | [CONFIRMADO_NO_CÓDIGO] |
| `REDIS_URL` | Broker/result backend Celery | [CONFIRMADO_NO_CÓDIGO] |
| `OPENAI_API_KEY` | Chave OpenAI | [CONFIRMADO_NO_CÓDIGO] |

## Configuração de runtime

- [CONFIRMADO_NO_CÓDIGO] O timezone do Django está definido como `America/Sao_Paulo`.
- [CONFIRMADO_NO_CÓDIGO] O idioma padrão é `pt-br`.
- [CONFIRMADO_NO_CÓDIGO] A paginação padrão usa `jurisai.pagination.StandardPagination`.
- [CONFIRMADO_NO_CÓDIGO] O backend grava arquivos em `MEDIA_ROOT` e serve estáticos a partir de `STATIC_ROOT`.

## Seeds e dados iniciais

- [CONFIRMADO_NO_CÓDIGO] `setup_local` executa `migrate` seguido de `seed_demo`.
- [CONFIRMADO_NO_CÓDIGO] `seed_demo` cria organização demo, admin, advogados, clientes, casos, prazos e documentos.
- [CONFIRMADO_NO_CÓDIGO] `seed_initial` e `seed_demo` usam o plano `starter`.
- [CONFIRMADO_NO_CÓDIGO] O model atual `Organization` não define `starter` como plano válido.

## Execução de testes

- [CONFIRMADO_NO_CÓDIGO] O repositório usa `pytest`.
- [PRECISA_VALIDAR] Neste ambiente de análise, não foi possível rodar os testes porque `python`, `py` e `pytest` não estavam disponíveis no PATH local.

