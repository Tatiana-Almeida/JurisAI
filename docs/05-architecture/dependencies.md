# Dependencies

## Dependências internas

- [CONFIRMADO_NO_CÓDIGO] `accounts` depende de `organizations`.
- [CONFIRMADO_NO_CÓDIGO] `law_cases` depende de `accounts` e `organizations`.
- [CONFIRMADO_NO_CÓDIGO] `deadlines` depende de `law_cases`, `organizations` e `notifications`.
- [CONFIRMADO_NO_CÓDIGO] `documents` depende de `law_cases`, `organizations` e `jurisai.utils`.
- [CONFIRMADO_NO_CÓDIGO] `ai_assistant` depende de `organizations`, `accounts` e OpenAI SDK.
- [CONFIRMADO_NO_CÓDIGO] `billing` depende de `organizations` e `notifications`.
- [CONFIRMADO_NO_CÓDIGO] `audit_logs` depende de `accounts` e `jurisai.middleware`.

## Dependências externas principais

- [CONFIRMADO_NO_CÓDIGO] Django
- [CONFIRMADO_NO_CÓDIGO] DRF
- [CONFIRMADO_NO_CÓDIGO] SimpleJWT
- [CONFIRMADO_NO_CÓDIGO] django-filter
- [CONFIRMADO_NO_CÓDIGO] Celery
- [CONFIRMADO_NO_CÓDIGO] Redis
- [CONFIRMADO_NO_CÓDIGO] OpenAI SDK
- [CONFIRMADO_NO_CÓDIGO] drf-yasg
- [CONFIRMADO_NO_CÓDIGO] pytest e pytest-django

## Dependências inconsistentes

- [PRECISA_VALIDAR] `django_celery_beat` aparece em `INSTALLED_APPS`, mas não em `requirements.txt`.

