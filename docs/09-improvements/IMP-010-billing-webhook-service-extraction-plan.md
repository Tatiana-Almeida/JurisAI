# IMP-010 Billing Webhook Service Extraction Plan

## 1. Comportamento atual

- [CONFIRMADO_NO_CODIGO] O endpoint continua `POST /api/v1/webhook/` em [billing/urls.py](/c:/projectos/JurisAI/billing/urls.py).
- [CONFIRMADO_NO_CODIGO] [billing/views.py](/c:/projectos/JurisAI/billing/views.py) concentra:
  - leitura de `request.body`
  - leitura de `HTTP_STRIPE_SIGNATURE`
  - validacao de assinatura
  - validacao de timestamp com `STRIPE_WEBHOOK_TOLERANCE_SECONDS`
  - parse de JSON
  - validacao semantica de eventos conhecidos
  - chamada ao service para resolver `Organization`
  - chamada ao orquestrador transacional do webhook
  - resposta HTTP final
- [CONFIRMADO_NO_CODIGO] O payload publico de sucesso atual e `{'received': True, 'event_type': ...}`.
- [CONFIRMADO_NO_CODIGO] O comportamento atual esta protegido por [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py) e pela suite completa com `30 passed`.

## 2. Responsabilidades hoje concentradas em `billing/views.py`

- [CONFIRMADO_NO_CODIGO] Parse de assinatura Stripe-like
- [CONFIRMADO_NO_CODIGO] Calculo de HMAC
- [CONFIRMADO_NO_CODIGO] Validacao de frescor do timestamp
- [CONFIRMADO_NO_CODIGO] Parse do payload JSON
- [CONFIRMADO_NO_CODIGO] Validacao estrutural do evento
- [CONFIRMADO_NO_CODIGO] Chamada ao helper de resolucao de tenant por `metadata.organization_id` ou `customer`
- [CONFIRMADO_NO_CODIGO] Validacao de campos obrigatorios por tipo de evento
- [CONFIRMADO_NO_CODIGO] Chamada ao orquestrador para `payload_hash`, persistencia idempotente e side effects financeiros
- [CONFIRMADO_NO_CODIGO] Mapeamento de erros para `Response`

## 3. Funcoes e classes candidatas a extrair

### Funcoes candidatas

- [INFERIDO_DO_CODIGO] `parse_signature(signature_header)`
- [INFERIDO_DO_CODIGO] `validate_signature(payload_body, signature_header, secret)`
- [INFERIDO_DO_CODIGO] `validate_signature_timestamp(signature_header, tolerance_seconds)`
- [INFERIDO_DO_CODIGO] `parse_event(payload_body)`
- [INFERIDO_DO_CODIGO] `resolve_organization(payload)`
- [INFERIDO_DO_CODIGO] `validate_event_payload(event_type, payload, organization)`
- [INFERIDO_DO_CODIGO] `process_event(event, payload_body, signature_timestamp, organization)`

### Classes candidatas

- [INFERIDO_DO_CODIGO] `BillingWebhookService`
- [INFERIDO_DO_CODIGO] `BillingWebhookResult`
- [PRECISA_VALIDAR] excecoes internas dedicadas como `WebhookValidationError` e `WebhookDuplicateEvent`

## 4. Desenho recomendado para `billing/services.py`

### Estrutura recomendada

- [INFERIDO_DO_CODIGO] Criar [billing/services.py](/c:/projectos/JurisAI/billing/services.py)
- [INFERIDO_DO_CODIGO] Centralizar nele a logica do webhook
- [INFERIDO_DO_CODIGO] Manter a view apenas como adaptador HTTP

### API interna sugerida

```python
class BillingWebhookService:
    def __init__(self, secret: str, tolerance_seconds: int):
        ...

    def handle(self, payload_body: bytes, signature_header: str) -> BillingWebhookResult:
        ...
```

```python
@dataclass
class BillingWebhookResult:
    status_code: int
    payload: dict
```

### Fluxo recomendado

1. [INFERIDO_DO_CODIGO] `StripeWebhookView.post()` coleta `secret`, `tolerance_seconds`, `signature_header` e `request.body`
2. [INFERIDO_DO_CODIGO] instancia `BillingWebhookService`
3. [INFERIDO_DO_CODIGO] chama `handle(...)`
4. [INFERIDO_DO_CODIGO] converte `BillingWebhookResult` em `Response`

### Regras a preservar

- [CONFIRMADO_NO_CODIGO] mesmo endpoint
- [CONFIRMADO_NO_CODIGO] mesmos status codes
- [CONFIRMADO_NO_CODIGO] mesmo payload de sucesso
- [CONFIRMADO_NO_CODIGO] mesma politica de duplicado: `200` sem reaplicar efeitos
- [CONFIRMADO_NO_CODIGO] mesma politica de replay: `400` para timestamp invalido ou antigo

## 5. Arquivos afetados

- [billing/views.py](/c:/projectos/JurisAI/billing/views.py)
- [billing/services.py](/c:/projectos/JurisAI/billing/services.py) novo
- [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py) [PRECISA_VALIDAR] apenas se quisermos adicionar testes unitarios do service depois
- [docs/09-improvements/change-log.md](/c:/projectos/JurisAI/docs/09-improvements/change-log.md)
- [docs/07-quality/refactoring-plan.md](/c:/projectos/JurisAI/docs/07-quality/refactoring-plan.md) [PRECISA_VALIDAR]

## 6. Estrategia de refatoracao incremental

### Fase 1: extrair helpers puros

- [CONFIRMADO_NO_CODIGO] Helpers de assinatura, timestamp e parse foram movidos para `billing/services.py`
- [CONFIRMADO_NO_CODIGO] A view passou a importar esses helpers
- [CONFIRMADO_NO_CODIGO] Nao houve mudanca na transacao nem nos side effects

### Fase 2: extrair validacao de evento

- [INFERIDO_DO_CODIGO] Mover validacao estrutural e semantica para funcoes do service
- [INFERIDO_DO_CODIGO] Manter a view ainda coordenando a resposta HTTP
- [CONFIRMADO_NO_CODIGO] O primeiro passo desta fase ja moveu a leitura semantica minima de `event_id`, `event_type` e `data.object` para helpers pequenos em [billing/services.py](/c:/projectos/JurisAI/billing/services.py).
- [CONFIRMADO_NO_CODIGO] O segundo passo desta fase moveu a resolucao de `organization_id` e o lookup de `organization` para helpers pequenos em [billing/services.py](/c:/projectos/JurisAI/billing/services.py).
- [CONFIRMADO_NO_CODIGO] A validacao especifica por tipo continua na view nesta etapa.

### Fase 3: extrair processamento idempotente

- [INFERIDO_DO_CODIGO] Mover `transaction.atomic()`, persistencia de `BillingWebhookEvent` e side effects financeiros para metodo do service
- [INFERIDO_DO_CODIGO] A view passa a apenas delegar e devolver `Response`
- [CONFIRMADO_NO_CODIGO] Foi introduzido um resultado interno simples para a fase transacional.
- [CONFIRMADO_NO_CODIGO] `transaction.atomic()`, persistencia de `BillingWebhookEvent`, deteccao de duplicado e side effects financeiros foram movidos para um orquestrador em [billing/services.py](/c:/projectos/JurisAI/billing/services.py).
- [CONFIRMADO_NO_CODIGO] A view permaneceu responsavel por HTTP, validacao inicial e montagem do payload de resposta.

### Fase 4: consolidar contrato interno

- [INFERIDO_DO_CODIGO] Introduzir `BillingWebhookResult`
- [INFERIDO_DO_CODIGO] Eliminar logica residual da view

## 7. Testes que protegem o comportamento

- [CONFIRMADO_NO_CODIGO] `test_webhook_without_signature_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_webhook_with_invalid_signature_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_invalid_payload_should_not_change_financial_state`
- [CONFIRMADO_NO_CODIGO] `test_unknown_event_should_not_change_financial_state`
- [CONFIRMADO_NO_CODIGO] `test_valid_signed_payment_success_event_should_be_accepted_after_correction`
- [CONFIRMADO_NO_CODIGO] `test_repeated_event_id_should_be_idempotent_after_correction`
- [CONFIRMADO_NO_CODIGO] `test_webhook_with_old_timestamp_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_unsigned_subscription_update_should_be_rejected_and_not_change_subscription`
- [CONFIRMADO_NO_CODIGO] suite completa `.\.venv\Scripts\python.exe -m pytest`

## 8. Riscos

- [CONFIRMADO_NO_CODIGO] Risco de alterar status code ou payload de erro por acidente
- [CONFIRMADO_NO_CODIGO] Risco de quebrar a ordem atual de validacao
- [CONFIRMADO_NO_CODIGO] Risco de mover `transaction.atomic()` para lugar incorreto
- [CONFIRMADO_NO_CODIGO] Risco de perder a politica de duplicado com `200`
- [INFERIDO_DO_CODIGO] Risco de introduzir excecoes internas nao mapeadas corretamente para HTTP

## 9. Rollback plan

1. Reverter apenas [billing/views.py](/c:/projectos/JurisAI/billing/views.py) e [billing/services.py](/c:/projectos/JurisAI/billing/services.py)
2. Manter os testes do webhook como rede de seguranca
3. Como nao ha schema nem migration nesta refatoracao, o rollback e simples e local

## 10. Criterios de aceitacao

- [CONFIRMADO_NO_CODIGO] O endpoint continua `POST /api/v1/webhook/`
- [CONFIRMADO_NO_CODIGO] O payload de sucesso continua igual
- [CONFIRMADO_NO_CODIGO] A idempotencia por `event_id` continua funcionando
- [CONFIRMADO_NO_CODIGO] A protecao por timestamp continua funcionando
- [CONFIRMADO_NO_CODIGO] Os 8 testes do webhook continuam passando
- [CONFIRMADO_NO_CODIGO] A suite completa continua com `30 passed`
- [INFERIDO_DO_CODIGO] `billing/views.py` fica reduzido a um adaptador HTTP fino
