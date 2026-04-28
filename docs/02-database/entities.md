# Entities

## ENT-001 Organization

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `name`, `plan`, `created_at`.
- [CONFIRMADO_NO_CODIGO] Referenciada por `User`, `LawCase`, `Deadline`, `Document`, `AIRequest`, `Payment`, `Subscription`, `Invoice`, `Notification`, `AuditLog`, `BillingWebhookEvent`.
- [CONFIRMADO_NO_CODIGO] `plan` esta alinhado no schema migrado e no model atual com `free`, `solo`, `growth` e `enterprise` apos [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py).

## ENT-002 User

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `name`, `email`, `organization`, `role`, `is_active`, `is_staff`, `created_at`, `updated_at`.

## ENT-003 LawCase

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `title`, `description`, `client`, `lawyer`, `status`, `organization`, `created_at`, `updated_at`, `deleted`.

## ENT-004 Deadline

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `law_case`, `due_date`, `completed`, `organization`, `created_at`, `updated_at`.

## ENT-005 Document

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `law_case`, `type`, `content`, `file`, `version`, `organization`, `created_at`, `updated_at`.

## ENT-006 AIRequest

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `user`, `organization`, `prompt`, `response`, `tokens_used`, `cost`, `created_at`.

## ENT-007 Payment

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `organization`, `amount`, `status`, `method`, `created_at`, `updated_at`.

## ENT-008 Subscription

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `organization`, `stripe_subscription_id`, `plan`, `status`, `current_period_start`, `current_period_end`, `trial_end`, `created_at`, `updated_at`.
- [CONFIRMADO_NO_CODIGO] O schema migrado passou a incluir esta entidade via [billing/migrations/0003_subscription_invoice.py](/c:/projectos/JurisAI/billing/migrations/0003_subscription_invoice.py).

## ENT-009 Invoice

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `organization`, `stripe_invoice_id`, `amount`, `status`, `due_date`, `paid_at`, `created_at`, `updated_at`.
- [CONFIRMADO_NO_CODIGO] O schema migrado passou a incluir esta entidade via [billing/migrations/0003_subscription_invoice.py](/c:/projectos/JurisAI/billing/migrations/0003_subscription_invoice.py).

## ENT-010 Notification

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `organization`, `channel`, `recipient`, `subject`, `body`, `sent`, `created_at`, `sent_at`.

## ENT-011 AuditLog

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `organization`, `user`, `action`, `entity`, `before`, `after`, `ip`, `timestamp`.
- [CONFIRMADO_NO_CODIGO] `organization` e nullable para preservar logs antigos ou sem contexto de tenant.

## ENT-012 BillingWebhookEvent

- [CONFIRMADO_NO_CODIGO] Campos: `id`, `event_id`, `event_type`, `organization`, `payload_hash`, `signature_timestamp`, `processed_at`, `created_at`.
- [CONFIRMADO_NO_CODIGO] `event_id` e unico e suporta idempotencia persistente do webhook de billing.
