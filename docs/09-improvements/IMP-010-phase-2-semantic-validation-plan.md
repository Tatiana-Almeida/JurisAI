# IMP-010 Phase 2 Semantic Validation Plan

## 1. Comportamento atual

- [CONFIRMADO_NO_CODIGO] O endpoint continua `POST /api/v1/webhook/`.
- [CONFIRMADO_NO_CODIGO] [billing/views.py](/c:/projectos/JurisAI/billing/views.py) ja delega assinatura, timestamp e parse para [billing/services.py](/c:/projectos/JurisAI/billing/services.py).
- [CONFIRMADO_NO_CODIGO] A view ainda executa a validacao semantica do evento antes de `transaction.atomic()`.
- [CONFIRMADO_NO_CODIGO] A view ainda coordena:
  - request e response HTTP
  - idempotencia por `event_id`
  - persistencia de `BillingWebhookEvent`
  - side effects de `Payment` e `Subscription`
- [CONFIRMADO_NO_CODIGO] A suite focal do webhook passa com `8 passed`.
- [CONFIRMADO_NO_CODIGO] A suite completa passa com `30 passed`.

## 2. Validacoes semanticas hoje presentes em `billing/views.py`

- [CONFIRMADO_NO_CODIGO] verificar se `event_type` existe
- [CONFIRMADO_NO_CODIGO] verificar se `event_id` existe
- [CONFIRMADO_NO_CODIGO] verificar se `event.get('data', {}).get('object', {})` e `dict`
- [CONFIRMADO_NO_CODIGO] resolver `organization_id` via `metadata.organization_id` ou `payload.customer`
- [CONFIRMADO_NO_CODIGO] resolver `organization` por lookup em `Organization`
- [CONFIRMADO_NO_CODIGO] para `invoice.payment_succeeded` com `organization`, exigir `amount_paid`
- [CONFIRMADO_NO_CODIGO] para `invoice.payment_failed` com `organization`, exigir `amount_due`
- [CONFIRMADO_NO_CODIGO] para `customer.subscription.updated` com `organization`, exigir `payload.id` e `payload.status`
- [CONFIRMADO_NO_CODIGO] para evento desconhecido, aceitar `200` sem efeito colateral
- [CONFIRMADO_NO_CODIGO] para payload invalido, retornar `400`

## 3. Funcoes candidatas para `billing/services.py`

### Funcoes de extracao segura

- [INFERIDO_DO_CODIGO] `extract_event_core(event) -> tuple[event_type, event_id, payload]`
- [INFERIDO_DO_CODIGO] `resolve_event_organization(payload) -> Organization | None`
- [INFERIDO_DO_CODIGO] `validate_known_event_payload(event_type, payload, organization) -> dict`
- [INFERIDO_DO_CODIGO] `build_semantic_context(event) -> dict`

### Estrutura sugerida do retorno

- [INFERIDO_DO_CODIGO] Um dicionario simples ou dataclass contendo:
  - `event_type`
  - `event_id`
  - `payload`
  - `organization`
  - `metadata`
  - `subscription_id` opcional
  - `subscription_status` opcional

### O que nao mover nesta fase

- [CONFIRMADO_NO_CODIGO] `transaction.atomic()`
- [CONFIRMADO_NO_CODIGO] criacao de `BillingWebhookEvent`
- [CONFIRMADO_NO_CODIGO] `Payment.objects.create(...)`
- [CONFIRMADO_NO_CODIGO] `Subscription.objects.update_or_create(...)`
- [CONFIRMADO_NO_CODIGO] montagem final de `Response`

## 4. Erros e status codes que devem ser preservados

- [CONFIRMADO_NO_CODIGO] assinatura ausente: `400`
- [CONFIRMADO_NO_CODIGO] assinatura invalida: `400`
- [CONFIRMADO_NO_CODIGO] timestamp antigo ou invalido: `400`
- [CONFIRMADO_NO_CODIGO] JSON invalido: `400`
- [CONFIRMADO_NO_CODIGO] payload estruturalmente invalido: `400`
- [CONFIRMADO_NO_CODIGO] evento conhecido com campo obrigatorio faltando: `400`
- [CONFIRMADO_NO_CODIGO] evento duplicado: `200`
- [CONFIRMADO_NO_CODIGO] evento desconhecido: `200`
- [CONFIRMADO_NO_CODIGO] payload de sucesso deve continuar `{'received': True, 'event_type': ...}`

## 5. Arquivos afetados

- [billing/views.py](/c:/projectos/JurisAI/billing/views.py)
- [billing/services.py](/c:/projectos/JurisAI/billing/services.py)
- [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py) [PRECISA_VALIDAR] apenas se surgir necessidade de cobertura mais granular
- [docs/09-improvements/change-log.md](/c:/projectos/JurisAI/docs/09-improvements/change-log.md)
- [docs/07-quality/refactoring-plan.md](/c:/projectos/JurisAI/docs/07-quality/refactoring-plan.md) [PRECISA_VALIDAR]

## 6. Estrategia incremental

### Passo 1: extrair apenas validacao estrutural minima

- [CONFIRMADO_NO_CODIGO] `event_type`, `event_id` e `payload` foram extraidos para helpers pequenos no service
- [CONFIRMADO_NO_CODIGO] A view continua aplicando o `400` para payload invalido com a mesma condicao estrutural
- [CONFIRMADO_NO_CODIGO] O resto da validacao permaneceu na view

### Passo 2: extrair resolucao de organization

- [CONFIRMADO_NO_CODIGO] O lookup de `organization_id` via `metadata.organization_id` ou `customer` foi movido para helper do service
- [CONFIRMADO_NO_CODIGO] O lookup de `Organization` tambem foi movido para helper do service
- [CONFIRMADO_NO_CODIGO] A view continua decidindo o fluxo para `organization` ausente ou nao encontrada

### Passo 3: extrair validacao semantica por tipo

- [INFERIDO_DO_CODIGO] Mover checks de `amount_paid`, `amount_due`, `subscription_id` e `subscription_status`
- [INFERIDO_DO_CODIGO] Retornar contexto pronto para a parte transacional

### Passo 4: manter view fina, mas ainda dona da transacao

- [INFERIDO_DO_CODIGO] A view so:
  - valida assinatura e timestamp
  - chama `parse_webhook_payload`
  - chama o novo helper semantico
  - abre transacao
  - executa idempotencia e side effects
  - responde HTTP

## 7. Testes protegendo comportamento

- [CONFIRMADO_NO_CODIGO] `test_webhook_without_signature_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_webhook_with_invalid_signature_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_invalid_payload_should_not_change_financial_state`
- [CONFIRMADO_NO_CODIGO] `test_unknown_event_should_not_change_financial_state`
- [CONFIRMADO_NO_CODIGO] `test_valid_signed_payment_success_event_should_be_accepted_after_correction`
- [CONFIRMADO_NO_CODIGO] `test_repeated_event_id_should_be_idempotent_after_correction`
- [CONFIRMADO_NO_CODIGO] `test_webhook_with_old_timestamp_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_unsigned_subscription_update_should_be_rejected_and_not_change_subscription`
- [CONFIRMADO_NO_CODIGO] `.\.venv\Scripts\python.exe -m pytest`

## 8. Riscos

- [CONFIRMADO_NO_CODIGO] Risco de alterar a fronteira entre payload invalido `400` e evento desconhecido `200`
- [CONFIRMADO_NO_CODIGO] Risco de mudar a ordem de validacao e “consumir” evento cedo demais
- [CONFIRMADO_NO_CODIGO] Risco de mudar quando `organization` e resolvida
- [INFERIDO_DO_CODIGO] Risco de introduzir retorno complexo demais no service logo cedo

## 9. Rollback plan

1. Reverter apenas [billing/views.py](/c:/projectos/JurisAI/billing/views.py) e [billing/services.py](/c:/projectos/JurisAI/billing/services.py)
2. Nao ha schema nem migration a desfazer
3. Reexecutar a suite focal e a suite completa

## 10. Criterios de aceitacao

- [CONFIRMADO_NO_CODIGO] Os mesmos `8` testes do webhook continuam passando
- [CONFIRMADO_NO_CODIGO] A suite completa continua com `30 passed`
- [CONFIRMADO_NO_CODIGO] Mesmo endpoint
- [CONFIRMADO_NO_CODIGO] Mesmo payload de sucesso
- [CONFIRMADO_NO_CODIGO] Mesmos status codes
- [CONFIRMADO_NO_CODIGO] `transaction.atomic()` permanece na view
- [CONFIRMADO_NO_CODIGO] Idempotencia permanece na view
- [CONFIRMADO_NO_CODIGO] Side effects financeiros permanecem na view
