# Traceability Matrix

| Codigo | Endpoint | Requisito | Regra | Entidade | Teste | Estado |
|---|---|---|---|---|---|---|
| `accounts.views.RegisterView` | API-010 | RF-002 | RN-008 | ENT-001, ENT-002 | [NAO_ENCONTRADO] | [CONFIRMADO_NO_CODIGO] |
| `accounts.views.UserViewSet.perform_create` | API-005 | RF-003 | RN-001, RN-006 | ENT-002, ENT-001 | [NAO_ENCONTRADO] | [CONFIRMADO_NO_CODIGO] |
| `law_cases.views.LawCaseViewSet` | API-016, API-017 | RF-005, RF-006 | RN-002, RN-009 | ENT-003 | `test_create_and_list_cases_for_organization` | [CONFIRMADO_NO_CODIGO] |
| `deadlines.views.DeadlineViewSet.complete` | API-020 | RF-007 | RN-010 | ENT-004 | CT-008 | [CONFIRMADO_NO_CODIGO] |
| `documents.serializers.DocumentSerializer.create` | API-021 | RF-008 | RN-012 | ENT-005 | CT-009 | [CONFIRMADO_NO_CODIGO] |
| `ai_assistant.services.ai_service._ensure_ai_quota` | API-034..039 | RF-009 | RN-004 | ENT-006, ENT-001 | CT-007 | [CONFIRMADO_NO_CODIGO] |
| `billing.views.StripeWebhookView` | API-029 | RF-011 | RN-016 | ENT-007, ENT-008, ENT-009, ENT-012 | CT-004, CT-019, CT-020, CT-021, CT-022, CT-023, CT-024 | [CONFIRMADO_NO_CODIGO] |
| `notifications.tasks.send_pending_notifications` | API-032, API-033 | RF-012 | RN-013 | ENT-010 | CT-010 | [CONFIRMADO_NO_CODIGO] |
| `audit_logs.signals`, `audit_logs.views.AuditLogViewSet` | API-030, API-031 | RF-013 | RN-015 | ENT-011, ENT-001 | CT-005, CT-016, CT-017, CT-018 | [CONFIRMADO_NO_CODIGO] |
| `jurisai.health.health_check` | API-042 | RF-014 | [NAO_ENCONTRADO] | [NAO_ENCONTRADO] | [NAO_ENCONTRADO] | [CONFIRMADO_NO_CODIGO] |
