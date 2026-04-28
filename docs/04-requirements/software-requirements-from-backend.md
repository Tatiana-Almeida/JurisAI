# Software Requirements From Backend

## RF-001 Autenticar usuários por JWT

- Evidência: endpoints `/auth/token/`, `/auth/token/refresh/`, `/auth/token/verify/`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-002 Registrar organização e usuário inicial

- Evidência: `accounts.views.RegisterView.post`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-003 Gerir usuários por organização

- Evidência: `UserViewSet`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-004 Gerir organizações

- Evidência: `OrganizationViewSet`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-005 Gerir casos jurídicos

- Evidência: `LawCaseViewSet`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-006 Aplicar soft delete a casos

- Evidência: `LawCaseViewSet.perform_destroy`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-007 Gerir prazos e marcar conclusão

- Evidência: `DeadlineViewSet` e ação `complete`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-008 Gerir documentos com versionamento por caso

- Evidência: `DocumentSerializer.create` e `Document` model.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-009 Processar requisições de IA e armazenar histórico

- Evidência: endpoints `ai/` e model `AIRequest`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-010 Gerir pagamentos, assinaturas e faturas

- Evidência: `billing` app.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-011 Receber webhook de cobrança

- Evidência: `StripeWebhookView`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-012 Gerir notificações por email e WhatsApp mock

- Evidência: `notifications` app.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-013 Registar eventos de auditoria

- Evidência: `audit_logs.signals`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

## RF-014 Expor healthcheck

- Evidência: `jurisai.health.health_check`.
- Estado: [CONFIRMADO_NO_CÓDIGO]

