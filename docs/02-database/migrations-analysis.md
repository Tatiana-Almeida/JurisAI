# Migrations Analysis

## Resumo

- [CONFIRMADO_NO_CODIGO] Cada app principal possui uma migration inicial `0001_initial.py`.
- [CONFIRMADO_NO_CODIGO] `organizations/0002_alter_organization_plan.py` foi adicionada para alinhar `Organization.plan` ao model atual e converter dados antigos `starter -> free`.
- [CONFIRMADO_NO_CODIGO] `audit_logs/0002_auditlog_organization.py` foi adicionada para a `IMP-003`.
- [CONFIRMADO_NO_CODIGO] `billing/0002_billingwebhookevent.py` foi adicionada para a Fase 2 da `IMP-002`.
- [CONFIRMADO_NO_CODIGO] `billing/0003_subscription_invoice.py` foi adicionada para corrigir o drift entre models e schema migrado de `Subscription` e `Invoice`.

## Divergencias relevantes

### Organization.plan

- [CONFIRMADO_NO_CODIGO] A migration inicial de `organizations` definia valores diferentes do model atual.
- [CONFIRMADO_NO_CODIGO] A migration [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py) corrige o schema e inclui conversao de dados `starter -> free`.

### AuditLog.organization

- [CONFIRMADO_NO_CODIGO] A migration `audit_logs/0002_auditlog_organization.py` adiciona `organization` a `AuditLog` como FK nullable.

### BillingWebhookEvent

- [CONFIRMADO_NO_CODIGO] A migration `billing/0002_billingwebhookevent.py` cria a tabela de idempotencia persistente do webhook.
- [CONFIRMADO_NO_CODIGO] A estrategia preserva o contrato publico do endpoint e move a deduplicacao para o banco.

### Billing Subscription / Invoice

- [CONFIRMADO_NO_CODIGO] A migration `billing/0003_subscription_invoice.py` cria `billing_subscription` e `billing_invoice`.
- [CONFIRMADO_NO_CODIGO] A correcao foi isolada no app `billing` e nao aplicou a migration inesperada de drift em `organizations.plan`.

## Cobertura das migrations lidas

- [CONFIRMADO_NO_CODIGO] `accounts`
- [CONFIRMADO_NO_CODIGO] `organizations`
- [CONFIRMADO_NO_CODIGO] `law_cases`
- [CONFIRMADO_NO_CODIGO] `deadlines`
- [CONFIRMADO_NO_CODIGO] `documents`
- [CONFIRMADO_NO_CODIGO] `billing`, contendo `Payment`, `BillingWebhookEvent`, `Subscription` e `Invoice`
- [CONFIRMADO_NO_CODIGO] `notifications`
- [CONFIRMADO_NO_CODIGO] `audit_logs`

## Lacunas

- [CONFIRMADO_NO_CODIGO] Nao ha lacuna observavel restante em `organizations.plan`; o drift de schema foi tratado em migration propria.
