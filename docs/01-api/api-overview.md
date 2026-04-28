# API Overview

## Visão geral

- [CONFIRMADO_NO_CÓDIGO] A API principal está sob o prefixo `/api/v1/`.
- [CONFIRMADO_NO_CÓDIGO] Os endpoints de IA estão sob `/api/v1/ai/`.
- [CONFIRMADO_NO_CÓDIGO] A API usa autenticação JWT Bearer por padrão.
- [CONFIRMADO_NO_CÓDIGO] A maioria dos recursos usa `ModelViewSet` com paginação, filtros, busca e ordenação.

## Grupos principais de API

| Grupo | Prefixo | Observação | Estado |
|---|---|---|---|
| Auth | `/api/v1/auth/` | Token, refresh, verify | [CONFIRMADO_NO_CÓDIGO] |
| Usuários | `/api/v1/users/` | CRUD + perfil + registro + senha | [CONFIRMADO_NO_CÓDIGO] |
| Organizações | `/api/v1/organizations/` | CRUD + `plans` | [CONFIRMADO_NO_CÓDIGO] |
| Casos | `/api/v1/cases/` | CRUD com soft delete | [CONFIRMADO_NO_CÓDIGO] |
| Prazos | `/api/v1/deadlines/` | CRUD + `complete` | [CONFIRMADO_NO_CÓDIGO] |
| Documentos | `/api/v1/documents/` | CRUD com versionamento | [CONFIRMADO_NO_CÓDIGO] |
| Billing | `/api/v1/payments/`, `/subscriptions/`, `/invoices/`, `/webhook/` | CRUD + webhook | [CONFIRMADO_NO_CÓDIGO] |
| Auditoria | `/api/v1/audit-logs/` | Apenas leitura | [CONFIRMADO_NO_CÓDIGO] |
| Notificações | `/api/v1/notifications/` | CRUD | [CONFIRMADO_NO_CÓDIGO] |
| IA | `/api/v1/ai/` | Geração, análise, revisão e histórico | [CONFIRMADO_NO_CÓDIGO] |
| Saúde | `/api/v1/health/` | Healthcheck simples | [CONFIRMADO_NO_CÓDIGO] |

## Comportamentos transversais

- [CONFIRMADO_NO_CÓDIGO] O handler de exceções converte respostas de erro para `{error, details}`.
- [CONFIRMADO_NO_CÓDIGO] Os viewsets usam paginação padrão DRF configurada globalmente.
- [CONFIRMADO_NO_CÓDIGO] A maioria dos recursos filtra dados por `request.user.organization`.
- [INFERIDO_DO_CÓDIGO] As rotas CRUD básicas de `DefaultRouter` incluem list, create, retrieve, update, partial_update e destroy quando o `ModelViewSet` não restringe métodos.

