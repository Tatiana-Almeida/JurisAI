# Technology Stack

## Linguagem e framework

| Item | Valor | Estado |
|---|---|---|
| Linguagem | Python | [CONFIRMADO_NO_CÓDIGO] |
| Framework web | Django 4.2.x | [CONFIRMADO_NO_CÓDIGO] |
| API framework | Django REST Framework | [CONFIRMADO_NO_CÓDIGO] |
| Autenticação | JWT via `djangorestframework-simplejwt` | [CONFIRMADO_NO_CÓDIGO] |
| Filtros | `django-filter` + `SearchFilter` + `OrderingFilter` | [CONFIRMADO_NO_CÓDIGO] |
| Documentação da API | `drf-yasg` | [CONFIRMADO_NO_CÓDIGO] |
| Fila assíncrona | Celery | [CONFIRMADO_NO_CÓDIGO] |
| Broker/backend | Redis | [CONFIRMADO_NO_CÓDIGO] |
| Testes | pytest + pytest-django | [CONFIRMADO_NO_CÓDIGO] |

## Banco de dados

- [CONFIRMADO_NO_CÓDIGO] Em runtime normal, a configuração padrão é PostgreSQL.
- [CONFIRMADO_NO_CÓDIGO] Em testes ou quando `DJANGO_USE_SQLITE` está ativo, o backend usa SQLite.
- [INFERIDO_DO_CÓDIGO] O SQLite é usado como simplificação para desenvolvimento/testes locais.

## Infraestrutura e runtime

- [CONFIRMADO_NO_CÓDIGO] O container web usa Gunicorn com 3 workers.
- [CONFIRMADO_NO_CÓDIGO] Há serviço `worker` Celery e interface Flower em `docker-compose.yml`.
- [CONFIRMADO_NO_CÓDIGO] Não existe serviço `beat` declarado no `docker-compose.yml`.
- [PRECISA_VALIDAR] O projeto lista `django_celery_beat` em `INSTALLED_APPS`, mas essa dependência não aparece em `requirements.txt`.

## Integrações externas

| Integração | Evidência | Estado |
|---|---|---|
| OpenAI | `openai>=1.0` e `ai_assistant/services/ai_service.py` | [CONFIRMADO_NO_CÓDIGO] |
| SMTP email | Configurações `EMAIL_*` e `send_mail` | [CONFIRMADO_NO_CÓDIGO] |
| Stripe webhook | `billing/views.py` | [CONFIRMADO_NO_CÓDIGO] |
| WhatsApp | Implementação mock em `notifications/services.py` | [CONFIRMADO_NO_CÓDIGO] |

## Limitações observadas

- [CONFIRMADO_NO_CÓDIGO] A integração OpenAI usa interface `ChatCompletion.create`, que pode não estar alinhada com a versão moderna declarada da SDK.
- [CONFIRMADO_NO_CÓDIGO] O armazenamento vetorial em `VectorStore` é em memória e simplificado.
- [NÃO_ENCONTRADO] Não foram encontradas bibliotecas explícitas de observabilidade, tracing, rate limiting, CORS ou validação de assinatura de webhook.

