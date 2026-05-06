# Checkpoint - Billing Readiness Audit

## Objetivo

Avaliar o estado real do modulo de billing para decidir se ele esta pronto para um SaaS comercial.

## Modelos existentes

- `Payment`: implemented
  - [CONFIRMADO_NO_CODIGO] Presente em `billing/models.py` com `amount`, `status`, `method` e relacao com `organization`.
- `Subscription`: implemented
  - [CONFIRMADO_NO_CODIGO] Presente em `billing/models.py` com `stripe_subscription_id`, `plan`, `status` e periodos.
- `Invoice`: implemented
  - [CONFIRMADO_NO_CODIGO] Presente em `billing/models.py` com `stripe_invoice_id`, `amount`, `status`, `due_date` e `paid_at`.
- `BillingWebhookEvent`: implemented
  - [CONFIRMADO_NO_CODIGO] Persistencia de eventos recebidos para idempotencia/auditoria.

## Endpoints existentes

- `GET/POST /api/v1/payments/`: implemented
  - [CONFIRMADO_NO_CODIGO] Registrado por `PaymentViewSet`.
- `GET/POST /api/v1/subscriptions/`: implemented
  - [CONFIRMADO_NO_CODIGO] Registrado por `SubscriptionViewSet`.
- `GET/POST /api/v1/invoices/`: implemented
  - [CONFIRMADO_NO_CODIGO] Registrado por `InvoiceViewSet`.
- `POST /api/v1/webhook/`: implemented
  - [CONFIRMADO_NO_CODIGO] `StripeWebhookView` exige assinatura e timestamp.

## Fluxos comerciais criticos

- Checkout Stripe: missing
  - [CONFIRMADO_NO_CODIGO] Nao existe rota `checkout` em `billing/urls.py`.
  - [CONFIRMADO_NO_CODIGO] O master prompt em `docs/00-project/JURISAI_MASTER_PROMPT.md` promete `POST /api/v1/billing/checkout/`, mas o codigo atual nao a implementa.

- Cancelamento de subscricao: missing
  - [CONFIRMADO_NO_CODIGO] Nao existe rota `cancel` em `billing/urls.py`.
  - [CONFIRMADO_NO_CODIGO] O master prompt promete `POST /api/v1/billing/cancel/`, mas o codigo atual nao a implementa.

- Portal de faturacao / billing portal: missing
  - [NAO_ENCONTRADO] Nao foi encontrado endpoint, service ou integracao de portal de faturacao autoatendido.

- Webhook Stripe: implemented
  - [CONFIRMADO_NO_CODIGO] `StripeWebhookView` valida `HTTP_STRIPE_SIGNATURE`, timestamp e payload.
  - [CONFIRMADO_NO_CODIGO] O processamento persiste `BillingWebhookEvent` e atualiza `Payment`/`Subscription` em `billing/services.py`.

- Estado da assinatura: partial
  - [CONFIRMADO_NO_CODIGO] O estado e armazenado e pode ser lido via CRUD de `Subscription`.
  - [INFERIDO_DO_CODIGO] Falta um endpoint mais orientado a "assinatura atual do tenant" como experiencia comercial simplificada.

- Bloqueio por plano: partial
  - [CONFIRMADO_NO_CODIGO] Existem limites por plano em organizacao e IA.
  - [NAO_ENCONTRADO] Nao foi encontrado bloqueio comercial forte que desligue recursos de billing/assinatura por falta de pagamento.

## Testes

- Webhook security: implemented
  - [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_security.py`
- Webhook orchestration/service: implemented
  - [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_services.py`
- Checkout: missing
  - [NAO_ENCONTRADO] Nao existem testes de checkout.
- Cancelamento: missing
  - [NAO_ENCONTRADO] Nao existem testes de cancelamento.
- Portal de faturacao: missing
  - [NAO_ENCONTRADO] Nao existem testes de portal de faturacao.

## Decisao

- [CONFIRMADO_NO_CODIGO] Billing tecnico existe como fundacao e trilha de webhook.
- [CONFIRMADO_NO_CODIGO] Billing comercial para venda ainda nao existe.
- [INFERIDO_DO_CODIGO] Antes do Frontend MVP comercial, o minimo seguro e implementar:
  1. checkout
  2. cancelamento
  3. leitura simples da assinatura atual
  4. testes de ponta a ponta para esses fluxos
