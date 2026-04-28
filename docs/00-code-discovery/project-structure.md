# Project Structure

## Estrutura de alto nível

```text
JurisAI/
  accounts/
  ai_assistant/
  audit_logs/
  billing/
  deadlines/
  documents/
  jurisai/
  law_cases/
  notifications/
  organizations/
  tests/
  manage.py
  README.md
  requirements.txt
  docker-compose.yml
  Dockerfile
  pytest.ini
```

## Pastas e responsabilidades

| Caminho | Responsabilidade | Estado |
|---|---|---|
| `accounts/` | Usuários, serializers, views, URLs e comandos de seed/setup | [CONFIRMADO_NO_CÓDIGO] |
| `organizations/` | Organização e limites de plano | [CONFIRMADO_NO_CÓDIGO] |
| `law_cases/` | Casos jurídicos | [CONFIRMADO_NO_CÓDIGO] |
| `deadlines/` | Prazos e task de lembrete | [CONFIRMADO_NO_CÓDIGO] |
| `documents/` | Documentos, upload path e versionamento | [CONFIRMADO_NO_CÓDIGO] |
| `ai_assistant/` | Endpoints de IA, histórico e serviços | [CONFIRMADO_NO_CÓDIGO] |
| `billing/` | Cobrança, invoices, subscriptions e webhook | [CONFIRMADO_NO_CÓDIGO] |
| `notifications/` | Entidade de notificação, serviço de envio e task assíncrona | [CONFIRMADO_NO_CÓDIGO] |
| `audit_logs/` | Modelo, serializer, view read-only e signals globais de auditoria | [CONFIRMADO_NO_CÓDIGO] |
| `jurisai/` | Configuração do projeto, middleware, permissões, health e Celery | [CONFIRMADO_NO_CÓDIGO] |
| `tests/` | Testes API com pytest + DRF APIClient | [CONFIRMADO_NO_CÓDIGO] |

## Convenções observadas

- [CONFIRMADO_NO_CÓDIGO] Cada app principal possui `models.py`, `serializers.py`, `views.py`, `urls.py` e `migrations/`.
- [CONFIRMADO_NO_CÓDIGO] Não existe uma pasta separada de `repositories/`.
- [CONFIRMADO_NO_CÓDIGO] Há uso de `services/` apenas em `ai_assistant/` e `notifications/`.
- [CONFIRMADO_NO_CÓDIGO] Há `tasks.py` em `deadlines`, `notifications` e `billing`.
- [NÃO_ENCONTRADO] Não foram encontrados módulos explícitos de cache, observabilidade estruturada, feature flags ou policies separadas.

## Pontos de entrada

- [CONFIRMADO_NO_CÓDIGO] `manage.py` para comandos Django.
- [CONFIRMADO_NO_CÓDIGO] `jurisai/wsgi.py` para Gunicorn.
- [CONFIRMADO_NO_CÓDIGO] `jurisai/asgi.py` existe no projeto.
- [CONFIRMADO_NO_CÓDIGO] `jurisai/urls.py` agrega as rotas HTTP.
- [CONFIRMADO_NO_CÓDIGO] `jurisai/celery.py` inicializa o Celery.

## Artefatos de suporte

- [CONFIRMADO_NO_CÓDIGO] `docker-compose.yml` descreve `web`, `db`, `redis`, `worker` e `flower`.
- [CONFIRMADO_NO_CÓDIGO] `Dockerfile` instala dependências e roda `collectstatic`.
- [CONFIRMADO_NO_CÓDIGO] `pytest.ini` configura `pytest-django`.
- [CONFIRMADO_NO_CÓDIGO] Existem comandos de seed em `accounts/management/commands/`.

