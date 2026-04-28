# IMP-002 Billing Webhook Plan

## Estado atual

- [CONFIRMADO_NO_CODIGO] A Fase 1 foi implementada com `STRIPE_WEBHOOK_SECRET` e validacao de `Stripe-Signature`.
- [CONFIRMADO_NO_CODIGO] A Fase 2 foi implementada com persistencia de `event_id` e tolerancia de timestamp.
- [CONFIRMADO_NO_CODIGO] O endpoint continua `POST /api/v1/webhook/`.
- [CONFIRMADO_NO_CODIGO] A suite de webhook passou integralmente e a suite completa do projeto tambem passou.

## Resultado tecnico

- [CONFIRMADO_NO_CODIGO] Requests sem assinatura ou com assinatura invalida sao rejeitados antes de qualquer efeito colateral.
- [CONFIRMADO_NO_CODIGO] `event_id` duplicado nao reaplica `Payment` nem `Subscription`.
- [CONFIRMADO_NO_CODIGO] Timestamp antigo ou invalido e rejeitado com `400`.
- [CONFIRMADO_NO_CODIGO] O payload de sucesso foi preservado: `received` e `event_type`.

## Pendencias restantes

- [INFERIDO_DO_CODIGO] Extracao da logica do webhook para `billing/services.py`.
- [INFERIDO_DO_CODIGO] Eventual endurecimento adicional do parse de timestamp e observabilidade operacional.
- [CONFIRMADO_NO_CODIGO] Warning tecnico restante por uso de `timezone.utc`.
