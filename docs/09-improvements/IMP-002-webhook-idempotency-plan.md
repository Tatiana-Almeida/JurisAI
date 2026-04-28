# IMP-002 Webhook Idempotency Plan

## 1. Resumo da Fase 2

- [CONFIRMADO_NO_CODIGO] A Fase 2 foi implementada para impedir reaplicacao do mesmo `event_id`.
- [CONFIRMADO_NO_CODIGO] A correcao tambem adicionou protecao basica contra replay por timestamp antigo.

## 2. Problema atual

- [CONFIRMADO_NO_CODIGO] Antes da Fase 2, o webhook nao persistia `event_id`.
- [CONFIRMADO_NO_CODIGO] Antes da Fase 2, o teste de idempotencia estava marcado como `xfail`.

## 3. Evidencias no codigo e testes

- [CONFIRMADO_NO_CODIGO] [billing/models.py](/c:/projectos/JurisAI/billing/models.py) agora define `BillingWebhookEvent`.
- [CONFIRMADO_NO_CODIGO] [billing/migrations/0002_billingwebhookevent.py](/c:/projectos/JurisAI/billing/migrations/0002_billingwebhookevent.py) cria a persistencia dedicada.
- [CONFIRMADO_NO_CODIGO] [billing/views.py](/c:/projectos/JurisAI/billing/views.py) registra o evento em transacao e ignora duplicados com `200`.
- [CONFIRMADO_NO_CODIGO] [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py) agora cobre duplicidade e timestamp antigo sem `xfail`.

## 4. Desenho implementado

- [CONFIRMADO_NO_CODIGO] Modelo dedicado `BillingWebhookEvent`
- [CONFIRMADO_NO_CODIGO] Chave unica em `event_id`
- [CONFIRMADO_NO_CODIGO] Hash do payload para rastreabilidade
- [CONFIRMADO_NO_CODIGO] Timestamp da assinatura persistido
- [CONFIRMADO_NO_CODIGO] `transaction.atomic()` no processamento

## 5. Modelo ou tabela criada

- [CONFIRMADO_NO_CODIGO] `BillingWebhookEvent`

## 6. Campos criados

- [CONFIRMADO_NO_CODIGO] `id`
- [CONFIRMADO_NO_CODIGO] `event_id`
- [CONFIRMADO_NO_CODIGO] `event_type`
- [CONFIRMADO_NO_CODIGO] `organization`
- [CONFIRMADO_NO_CODIGO] `payload_hash`
- [CONFIRMADO_NO_CODIGO] `signature_timestamp`
- [CONFIRMADO_NO_CODIGO] `processed_at`
- [CONFIRMADO_NO_CODIGO] `created_at`

## 7. Migration criada

- [CONFIRMADO_NO_CODIGO] [billing/migrations/0002_billingwebhookevent.py](/c:/projectos/JurisAI/billing/migrations/0002_billingwebhookevent.py)

## 8. Fluxo de processamento idempotente

1. [CONFIRMADO_NO_CODIGO] validar assinatura
2. [CONFIRMADO_NO_CODIGO] validar timestamp dentro da tolerancia
3. [CONFIRMADO_NO_CODIGO] parsear payload e extrair `event_id`
4. [CONFIRMADO_NO_CODIGO] validar campos obrigatorios do evento conhecido
5. [CONFIRMADO_NO_CODIGO] abrir transacao
6. [CONFIRMADO_NO_CODIGO] tentar criar `BillingWebhookEvent`
7. [CONFIRMADO_NO_CODIGO] em duplicado, responder `200` sem side effect
8. [CONFIRMADO_NO_CODIGO] em evento novo, aplicar efeitos e concluir

## 9. Politica para evento duplicado

- [CONFIRMADO_NO_CODIGO] Evento duplicado responde `200`.
- [CONFIRMADO_NO_CODIGO] O payload de sucesso permanece compativel com o atual.
- [CONFIRMADO_NO_CODIGO] Nenhum efeito financeiro e reaplicado.

## 10. Politica para timestamp antigo

- [CONFIRMADO_NO_CODIGO] Timestamp fora da tolerancia e rejeitado com `400`.
- [CONFIRMADO_NO_CODIGO] A tolerancia e configuravel por `STRIPE_WEBHOOK_TOLERANCE_SECONDS`.
- [CONFIRMADO_NO_CODIGO] O default atual e `300` segundos.

## 11. Estrategia de atomicidade

- [CONFIRMADO_NO_CODIGO] O processamento usa `transaction.atomic()`.
- [CONFIRMADO_NO_CODIGO] A unicidade de `event_id` e a barreira principal contra corridas e duplicidade.

## 12. Plano de testes

- [CONFIRMADO_NO_CODIGO] Duplicidade por `event_id` coberta
- [CONFIRMADO_NO_CODIGO] Timestamp antigo coberto
- [CONFIRMADO_NO_CODIGO] Suite focal passou
- [CONFIRMADO_NO_CODIGO] Suite completa passou

## 13. Riscos restantes

- [CONFIRMADO_NO_CODIGO] O webhook ainda mistura parse, decisao e persistencia na view.
- [CONFIRMADO_NO_CODIGO] Permanece warning tecnico por uso de `timezone.utc`.
- [PRECISA_VALIDAR] Pode ser desejavel adicionar mais metadata operacional ao modelo no futuro.

## 14. Rollback plan

1. Reverter a integracao do webhook com `BillingWebhookEvent`
2. Reverter a migration apenas com avaliacao de dados ja gravados
3. Manter os testes para preservar visibilidade do risco restaurado

## 15. Perguntas para validacao humana

1. A equipa quer manter o payload idempotente estritamente igual ou incluir um marcador futuro como `duplicate: true`?
2. Querem evoluir para extracao do webhook em `billing/services.py` no proximo ciclo?
