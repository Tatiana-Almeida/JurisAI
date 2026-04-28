# Test Coverage Analysis

## Visão geral

- [CONFIRMADO_NO_CÓDIGO] Existe um ficheiro principal de testes: `tests/test_api.py`.
- [CONFIRMADO_NO_CÓDIGO] Os testes usam `pytest`, `pytest-django` e `rest_framework.test.APIClient`.
- [PRECISA_VALIDAR] Não foi possível executar a suíte no ambiente atual por ausência de runtime Python acessível no PATH.

## Cobertura observada

| Área | Cobertura atual | Estado |
|---|---|---|
| Login JWT | Testado | [CONFIRMADO_NO_CÓDIGO] |
| Refresh JWT | Testado | [CONFIRMADO_NO_CÓDIGO] |
| Endpoint protegido `/users/` | Testado | [CONFIRMADO_NO_CÓDIGO] |
| Criação/listagem de casos | Testado | [CONFIRMADO_NO_CÓDIGO] |
| Isolamento de listagem entre tenants | Testado | [CONFIRMADO_NO_CÓDIGO] |
| Perfil do usuário | Testado | [CONFIRMADO_NO_CÓDIGO] |
| Histórico de IA | Testado | [CONFIRMADO_NO_CÓDIGO] |

## Lacunas

- [CONFIRMADO_NO_CÓDIGO] Não há testes observados para `organizations`, `deadlines`, `documents`, `billing`, `notifications`, `audit_logs`.
- [CONFIRMADO_NO_CÓDIGO] Não há testes observados para webhook público.
- [CONFIRMADO_NO_CÓDIGO] Não há testes observados para tasks Celery.
- [CONFIRMADO_NO_CÓDIGO] Não há testes observados para auditoria via signals.
- [CONFIRMADO_NO_CÓDIGO] Não há testes observados para cenários negativos de autorização por papel.
- [CONFIRMADO_NO_CÓDIGO] Não há testes observados para validação cruzada de tenant em foreign keys.

