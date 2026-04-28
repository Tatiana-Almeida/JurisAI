# Data Dictionary

## Organization

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `id` | UUID | Sim | PK | [CONFIRMADO_NO_CODIGO] |
| `name` | string(180) | Sim | Unico | [CONFIRMADO_NO_CODIGO] |
| `plan` | string(50) | Sim | Enum `free/solo/growth/enterprise` | [CONFIRMADO_NO_CODIGO] |
| `created_at` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |

## User

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `email` | email | Sim | Unico | [CONFIRMADO_NO_CODIGO] |
| `organization_id` | UUID FK | Sim | Tenant do usuario | [CONFIRMADO_NO_CODIGO] |
| `role` | string | Sim | `admin/advogado/cliente` | [CONFIRMADO_NO_CODIGO] |

## LawCase

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `client_id` | UUID FK | Sim | Cliente do caso | [CONFIRMADO_NO_CODIGO] |
| `lawyer_id` | UUID FK | Sim | Advogado do caso | [CONFIRMADO_NO_CODIGO] |
| `status` | string | Sim | Enum de estado | [CONFIRMADO_NO_CODIGO] |
| `deleted` | bool | Sim | Soft delete | [CONFIRMADO_NO_CODIGO] |

## Document

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `type` | string | Sim | Enum de tipo | [CONFIRMADO_NO_CODIGO] |
| `content` | text | Nao | Conteudo textual | [CONFIRMADO_NO_CODIGO] |
| `file` | file | Nao | Upload opcional | [CONFIRMADO_NO_CODIGO] |
| `version` | int | Sim | Versionamento por caso | [CONFIRMADO_NO_CODIGO] |

## AuditLog

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `organization_id` | UUID FK | Nao | Tenant do log; nullable para historico ou sem contexto | [CONFIRMADO_NO_CODIGO] |
| `user_id` | UUID FK | Nao | Autor do log quando existir | [CONFIRMADO_NO_CODIGO] |
| `action` | string(50) | Sim | Tipo de acao auditada | [CONFIRMADO_NO_CODIGO] |
| `entity` | string(120) | Sim | Origem `app_label.model_name` | [CONFIRMADO_NO_CODIGO] |
| `before` | JSON | Nao | Snapshot anterior | [CONFIRMADO_NO_CODIGO] |
| `after` | JSON | Nao | Snapshot posterior | [CONFIRMADO_NO_CODIGO] |
| `ip` | IP | Nao | Endereco de origem | [CONFIRMADO_NO_CODIGO] |
| `timestamp` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |

## BillingWebhookEvent

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `event_id` | string(255) | Sim | Unico; chave de idempotencia | [CONFIRMADO_NO_CODIGO] |
| `event_type` | string(120) | Sim | Tipo do evento recebido | [CONFIRMADO_NO_CODIGO] |
| `organization_id` | UUID FK | Nao | Tenant relacionado quando resolvido | [CONFIRMADO_NO_CODIGO] |
| `payload_hash` | string(64) | Sim | SHA-256 do payload bruto | [CONFIRMADO_NO_CODIGO] |
| `signature_timestamp` | datetime | Sim | Timestamp do header assinado | [CONFIRMADO_NO_CODIGO] |
| `processed_at` | datetime | Sim | Momento do processamento | [CONFIRMADO_NO_CODIGO] |
| `created_at` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |

## Subscription

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `organization_id` | UUID FK | Sim | Tenant da assinatura | [CONFIRMADO_NO_CODIGO] |
| `stripe_subscription_id` | string(255) | Sim | Unico | [CONFIRMADO_NO_CODIGO] |
| `plan` | string(50) | Sim | Plano atual | [CONFIRMADO_NO_CODIGO] |
| `status` | string(30) | Sim | Enum com default `active` | [CONFIRMADO_NO_CODIGO] |
| `current_period_start` | datetime | Nao | Inicio do periodo atual | [CONFIRMADO_NO_CODIGO] |
| `current_period_end` | datetime | Nao | Fim do periodo atual | [CONFIRMADO_NO_CODIGO] |
| `trial_end` | datetime | Nao | Fim do trial, se existir | [CONFIRMADO_NO_CODIGO] |
| `created_at` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |
| `updated_at` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |

## Invoice

| Campo | Tipo | Obrigatorio | Observacao | Estado |
|---|---|---|---|---|
| `organization_id` | UUID FK | Sim | Tenant da fatura | [CONFIRMADO_NO_CODIGO] |
| `stripe_invoice_id` | string(255) | Sim | Unico | [CONFIRMADO_NO_CODIGO] |
| `amount` | decimal(12,2) | Sim | Valor da fatura | [CONFIRMADO_NO_CODIGO] |
| `status` | string(30) | Sim | Enum com default `open` | [CONFIRMADO_NO_CODIGO] |
| `due_date` | datetime | Nao | Data de vencimento | [CONFIRMADO_NO_CODIGO] |
| `paid_at` | datetime | Nao | Momento do pagamento | [CONFIRMADO_NO_CODIGO] |
| `created_at` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |
| `updated_at` | datetime | Sim | Auto | [CONFIRMADO_NO_CODIGO] |

## Itens nao encontrados explicitamente

- [NAO_ENCONTRADO] Constraints check customizadas no ORM alem de PK, FK e unique observados.
