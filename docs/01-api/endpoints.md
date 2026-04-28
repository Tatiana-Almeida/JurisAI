# Endpoints

## Convenções

- [CONFIRMADO_NO_CÓDIGO] IDs são UUIDs na maioria das entidades.
- [INFERIDO_DO_CÓDIGO] Rotas de `DefaultRouter` seguem o padrão DRF com barra final.
- [CONFIRMADO_NO_CÓDIGO] Endpoints protegidos usam JWT Bearer salvo exceções explícitas.

## Catálogo

| ID | Método | Rota | Origem | Auth | Estado |
|---|---|---|---|---|---|
| API-001 | POST | `/api/v1/auth/token/` | SimpleJWT `TokenObtainPairView` | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-002 | POST | `/api/v1/auth/token/refresh/` | SimpleJWT `TokenRefreshView` | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-003 | POST | `/api/v1/auth/token/verify/` | SimpleJWT `TokenVerifyView` | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-004 | GET | `/api/v1/users/` | `UserViewSet.list` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-005 | POST | `/api/v1/users/` | `UserViewSet.create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-006 | GET | `/api/v1/users/{id}/` | `UserViewSet.retrieve` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-007 | PUT/PATCH | `/api/v1/users/{id}/` | `UserViewSet.update/partial_update` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-008 | DELETE | `/api/v1/users/{id}/` | `UserViewSet.destroy` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-009 | GET/PUT/PATCH | `/api/v1/users/profile/` | `UserViewSet.profile` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-010 | POST | `/api/v1/users/register/` | `RegisterView.post` | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-011 | GET | `/api/v1/users/me/` | `MeView.get` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-012 | POST | `/api/v1/users/change-password/` | `ChangePasswordView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-013 | GET/POST | `/api/v1/organizations/` | `OrganizationViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-014 | GET/PUT/PATCH/DELETE | `/api/v1/organizations/{id}/` | `OrganizationViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-015 | GET | `/api/v1/organizations/plans/` | `OrganizationViewSet.plans` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-016 | GET/POST | `/api/v1/cases/` | `LawCaseViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-017 | GET/PUT/PATCH/DELETE | `/api/v1/cases/{id}/` | `LawCaseViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-018 | GET/POST | `/api/v1/deadlines/` | `DeadlineViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-019 | GET/PUT/PATCH/DELETE | `/api/v1/deadlines/{id}/` | `DeadlineViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-020 | POST | `/api/v1/deadlines/{id}/complete/` | `DeadlineViewSet.complete` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-021 | GET/POST | `/api/v1/documents/` | `DocumentViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-022 | GET/PUT/PATCH/DELETE | `/api/v1/documents/{id}/` | `DocumentViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-023 | GET/POST | `/api/v1/payments/` | `PaymentViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-024 | GET/PUT/PATCH/DELETE | `/api/v1/payments/{id}/` | `PaymentViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-025 | GET/POST | `/api/v1/subscriptions/` | `SubscriptionViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-026 | GET/PUT/PATCH/DELETE | `/api/v1/subscriptions/{id}/` | `SubscriptionViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-027 | GET/POST | `/api/v1/invoices/` | `InvoiceViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-028 | GET/PUT/PATCH/DELETE | `/api/v1/invoices/{id}/` | `InvoiceViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-029 | POST | `/api/v1/webhook/` | `StripeWebhookView.post` | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-030 | GET | `/api/v1/audit-logs/` | `AuditLogViewSet.list` | JWT admin | [INFERIDO_DO_CÓDIGO] |
| API-031 | GET | `/api/v1/audit-logs/{id}/` | `AuditLogViewSet.retrieve` | JWT admin | [INFERIDO_DO_CÓDIGO] |
| API-032 | GET/POST | `/api/v1/notifications/` | `NotificationViewSet.list/create` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-033 | GET/PUT/PATCH/DELETE | `/api/v1/notifications/{id}/` | `NotificationViewSet.*` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-034 | POST | `/api/v1/ai/generate-petition/` | `GeneratePetitionView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-035 | POST | `/api/v1/ai/summarize-document/` | `SummarizeDocumentView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-036 | POST | `/api/v1/ai/analyze-risk/` | `AnalyzeRiskView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-037 | POST | `/api/v1/ai/search-jurisprudence/` | `SearchJurisprudenceView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-038 | POST | `/api/v1/ai/draft-contract/` | `DraftContractView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-039 | POST | `/api/v1/ai/review-document/` | `ReviewDocumentView.post` | JWT | [CONFIRMADO_NO_CÓDIGO] |
| API-040 | GET | `/api/v1/ai/history/` | `AIRequestViewSet.list` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-041 | GET | `/api/v1/ai/history/{id}/` | `AIRequestViewSet.retrieve` | JWT | [INFERIDO_DO_CÓDIGO] |
| API-042 | GET | `/api/v1/health/` | `health_check` | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-043 | GET | `/swagger/` | Swagger UI | Pública | [CONFIRMADO_NO_CÓDIGO] |
| API-044 | GET | `/redoc/` | ReDoc UI | Pública | [CONFIRMADO_NO_CÓDIGO] |

## Observações

- [CONFIRMADO_NO_CÓDIGO] `AuditLogViewSet` é `ReadOnlyModelViewSet`.
- [CONFIRMADO_NO_CÓDIGO] `AIRequestViewSet` também é `ReadOnlyModelViewSet`.
- [CONFIRMADO_NO_CÓDIGO] `health_check` não exige autenticação.
- [PRECISA_VALIDAR] A geração automática exata de algumas rotas DRF depende do comportamento padrão do `DefaultRouter`, embora o padrão esteja consistente com o uso observado.

