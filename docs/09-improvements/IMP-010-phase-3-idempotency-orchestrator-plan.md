# IMP-010 Phase 3 Idempotency Orchestrator Plan

## 1. Comportamento atual

- [CONFIRMADO_NO_CODIGO] O endpoint continua `POST /api/v1/webhook/`.
- [CONFIRMADO_NO_CODIGO] [billing/views.py](/c:/projectos/JurisAI/billing/views.py) agora faz a validacao HTTP inicial, a validacao semantica por tipo e a conversao do resultado interno em `Response`.
- [CONFIRMADO_NO_CODIGO] [billing/services.py](/c:/projectos/JurisAI/billing/services.py) passou a concentrar helpers puros, leitura semantica minima, resolucao de `organization` e a orquestracao transacional do webhook.
- [CONFIRMADO_NO_CODIGO] Evento duplicado hoje retorna `200` com `{'received': True, 'event_type': ...}`.
- [CONFIRMADO_NO_CODIGO] O comportamento atual esta protegido por [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py), com `8 passed`, e pela suite completa com `30 passed`.

## 2. Responsabilidades atuais da view

- [CONFIRMADO_NO_CODIGO] Ler `STRIPE_WEBHOOK_SECRET`, `STRIPE_WEBHOOK_TOLERANCE_SECONDS`, `HTTP_STRIPE_SIGNATURE` e `request.body`.
- [CONFIRMADO_NO_CODIGO] Rejeitar assinatura ausente, assinatura invalida e timestamp antigo ou invalido com `400`.
- [CONFIRMADO_NO_CODIGO] Fazer parse do JSON e validar `event_type`, `event_id` e `data.object`.
- [CONFIRMADO_NO_CODIGO] Resolver `organization` via helper do service.
- [CONFIRMADO_NO_CODIGO] Validar campos obrigatorios por tipo conhecido de evento.
- [CONFIRMADO_NO_CODIGO] Chamar o orquestrador transacional no service.
- [CONFIRMADO_NO_CODIGO] Converter o resultado interno em `Response` HTTP.

## 3. Responsabilidades propostas para o service

### Permanecem na view

- [CONFIRMADO_NO_CODIGO] Leitura do request e montagem de `Response`.
- [CONFIRMADO_NO_CODIGO] Mapeamento final de status codes.
- [CONFIRMADO_NO_CODIGO] Validacao de assinatura, timestamp e parse, salvo se ja estiverem delegados a helpers puros.
- [CONFIRMADO_NO_CODIGO] Validacao semantica por tipo nesta fase, porque o objetivo pedido e mover apenas orquestracao transacional e idempotencia.

### Migram para o service orquestrador

- [CONFIRMADO_NO_CODIGO] Abertura de `transaction.atomic()` dentro de uma funcao unica de orquestracao.
- [CONFIRMADO_NO_CODIGO] Criacao de `BillingWebhookEvent`.
- [CONFIRMADO_NO_CODIGO] Captura de `IntegrityError` para evento duplicado.
- [CONFIRMADO_NO_CODIGO] Execucao dos side effects financeiros, preservando a mesma ordem atual.
- [CONFIRMADO_NO_CODIGO] Retorno estruturado para a view informando se o evento foi processado com sucesso ou detectado como duplicado.

## 4. Desenho recomendado do service orquestrador

### Estrutura sugerida

- [INFERIDO_DO_CODIGO] Expandir [billing/services.py](/c:/projectos/JurisAI/billing/services.py) com um orquestrador dedicado, sem criar novo schema.
- [INFERIDO_DO_CODIGO] Nome sugerido: `process_webhook_event` ou `BillingWebhookOrchestrator`.
- [INFERIDO_DO_CODIGO] Nesta fase, uma funcao simples tende a ser a menor mudanca segura.

### API interna implementada

```python
@dataclass
class BillingWebhookProcessResult:
    outcome: str  # "processed" | "duplicate"
    event_type: str
```

```python
def process_billing_webhook_event(
    *,
    event_id: str,
    event_type: str,
    payload: dict,
    payload_body: bytes,
    signature_timestamp: int,
    organization,
    subscription_id: str | None = None,
    subscription_status: str | None = None,
) -> BillingWebhookProcessResult:
    ...
```

### Justificativa do formato

- [CONFIRMADO_NO_CODIGO] Um `dataclass` pequeno deixa explicito o resultado sem obrigar a view a interpretar excecoes de dominio demais.
- [CONFIRMADO_NO_CODIGO] `outcome="duplicate"` permite a view continuar devolvendo `200` com o mesmo payload atual.
- [CONFIRMADO_NO_CODIGO] Como a API publica ja esta estabilizada, o retorno do service deve ser minimo e interno.

## 5. Formato de retorno do service para a view

- [CONFIRMADO_NO_CODIGO] Retorno implementado:
  - `outcome="processed"` para evento novo processado com sucesso
  - `outcome="duplicate"` para evento com `event_id` ja persistido
  - `event_type` sempre devolvido para a view montar `{'received': True, 'event_type': ...}`
- [CONFIRMADO_NO_CODIGO] Nao foi necessario expor `created_payment`, `updated_subscription` ou metadados extras porque a view nao usa isso hoje.

## 6. Estrategia para preservar status codes

- [CONFIRMADO_NO_CODIGO] A view deve continuar retornando `400` antes de chamar o orquestrador quando assinatura, timestamp, JSON ou payload estrutural/semantico forem invalidos.
- [CONFIRMADO_NO_CODIGO] O orquestrador lida apenas com a fase transacional.
- [CONFIRMADO_NO_CODIGO] A view converte:
  - `processed` -> `200`
  - `duplicate` -> `200`
- [PRECISA_VALIDAR] Excecoes inesperadas do orquestrador devem continuar se propagando como erro de servidor, como acontece hoje, a menos que a equipa queira padronizar isso numa fase futura.

## 7. Estrategia para preservar `transaction.atomic()`

- [CONFIRMADO_NO_CODIGO] Hoje `transaction.atomic()` cobre criacao de `BillingWebhookEvent` e todos os efeitos financeiros.
- [CONFIRMADO_NO_CODIGO] O service mantem exatamente o mesmo boundary transacional: primeiro criar `BillingWebhookEvent`, depois executar side effects.
- [CONFIRMADO_NO_CODIGO] A ordem atual foi mantida para preservar a semantica de idempotencia.
- [CONFIRMADO_NO_CODIGO] Em caso de erro durante a transacao, o rollback atual evita commits parciais.

## 8. Estrategia para idempotencia

- [CONFIRMADO_NO_CODIGO] Hoje a idempotencia e garantida por unicidade de `event_id` em `BillingWebhookEvent`, materializada como `IntegrityError`.
- [CONFIRMADO_NO_CODIGO] O service continua usando esse mesmo mecanismo.
- [CONFIRMADO_NO_CODIGO] O `try/except IntegrityError` foi movido para dentro do service, retornando `outcome="duplicate"` sem reaplicar efeitos.
- [CONFIRMADO_NO_CODIGO] Nao ha necessidade de mudar schema nem regras de `event_id` nesta fase.

## 9. Estrategia para side effects financeiros

- [CONFIRMADO_NO_CODIGO] Nesta fase nao ha mudanca funcional permitida em `Payment` ou `Subscription`.
- [CONFIRMADO_NO_CODIGO] Os side effects migraram para o orquestrador junto com a transacao, com logica por tipo literalmente equivalente.
- [CONFIRMADO_NO_CODIGO] A implementacao copiou a logica atual para o service sem reestruturar calculos nem nomes intermediarios.
- [PRECISA_VALIDAR] Uma fase posterior pode separar `process_payment_succeeded`, `process_payment_failed` e `process_subscription_updated`, mas isso nao e necessario no primeiro passo.

## 10. Estrategia incremental de implementacao

### Passo 1: introduzir resultado interno

- [CONFIRMADO_NO_CODIGO] Foi criado `BillingWebhookProcessResult` em `billing/services.py`.

### Passo 2: extrair um orquestrador fino

- [CONFIRMADO_NO_CODIGO] Foi criado `process_billing_webhook_event(...)` em `billing/services.py`.
- [CONFIRMADO_NO_CODIGO] Foi movido para ele:
  - `payload_hash`
  - `signature_datetime`
  - `transaction.atomic()`
  - criacao de `BillingWebhookEvent`
  - side effects financeiros
  - captura de `IntegrityError`

### Passo 3: simplificar a view

- [INFERIDO_DO_CODIGO] Manter na view:
  - validacao HTTP
  - validacao semantica por tipo
  - chamada ao orquestrador
  - montagem do `Response`

### Passo 4: validar sem alterar contrato

- [CONFIRMADO_NO_CODIGO] Rodar a suite focal do webhook e a suite completa.
- [CONFIRMADO_NO_CODIGO] A Fase 3 foi validada mantendo os testes atuais.
- [INFERIDO_DO_CODIGO] O proximo passo natural e avaliar uma Fase 4 para mover tambem a validacao semantica por tipo.

## 11. Testes protegendo comportamento

- [CONFIRMADO_NO_CODIGO] `test_webhook_without_signature_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_webhook_with_invalid_signature_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_invalid_payload_should_not_change_financial_state`
- [CONFIRMADO_NO_CODIGO] `test_unknown_event_should_not_change_financial_state`
- [CONFIRMADO_NO_CODIGO] `test_valid_signed_payment_success_event_should_be_accepted_after_correction`
- [CONFIRMADO_NO_CODIGO] `test_repeated_event_id_should_be_idempotent_after_correction`
- [CONFIRMADO_NO_CODIGO] `test_webhook_with_old_timestamp_should_be_rejected_and_not_create_payment`
- [CONFIRMADO_NO_CODIGO] `test_unsigned_subscription_update_should_be_rejected_and_not_change_subscription`
- [CONFIRMADO_NO_CODIGO] Suite completa: `.\.venv\Scripts\python.exe -m pytest`

## 12. Testes novos recomendados

- [INFERIDO_DO_CODIGO] Testes unitarios para o orquestrador em arquivo novo, por exemplo `tests/test_billing_webhook_orchestrator.py`.
- [INFERIDO_DO_CODIGO] Casos recomendados:
  - evento novo processado retorna `outcome="processed"`
  - evento duplicado retorna `outcome="duplicate"`
  - erro durante side effect faz rollback e nao deixa `BillingWebhookEvent` persistido parcialmente
  - `invoice.payment_succeeded` cria `Payment` correto
  - `invoice.payment_failed` cria `Payment` com status `failed`
  - `customer.subscription.updated` atualiza ou cria `Subscription`
- [PRECISA_VALIDAR] Esses testes unitarios sao desejaveis, mas podem ser adicionados no mesmo PR apenas se a mudanca permanecer pequena; os testes de integracao atuais ja protegem o contrato externo.

## 13. Riscos

- [CONFIRMADO_NO_CODIGO] Risco de quebrar a politica atual de duplicado com `200`.
- [CONFIRMADO_NO_CODIGO] Risco de mover `transaction.atomic()` para um boundary diferente.
- [CONFIRMADO_NO_CODIGO] Risco de alterar a ordem entre criacao de `BillingWebhookEvent` e side effects.
- [INFERIDO_DO_CODIGO] Risco de a view passar a depender de detalhes internos demais do retorno do service.
- [INFERIDO_DO_CODIGO] Risco de introduzir excecoes internas mal mapeadas se a implementacao preferir excecoes em vez de `dataclass`.

## 14. Rollback plan

1. Reverter apenas [billing/views.py](/c:/projectos/JurisAI/billing/views.py) e [billing/services.py](/c:/projectos/JurisAI/billing/services.py)
2. Nao ha schema nem migration para desfazer
3. Reexecutar:
   - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_security.py`
   - `.\.venv\Scripts\python.exe -m pytest`

## 15. Criterios de aceitacao

- [CONFIRMADO_NO_CODIGO] Mesmo endpoint
- [CONFIRMADO_NO_CODIGO] Mesmo payload de sucesso
- [CONFIRMADO_NO_CODIGO] Mesmos status codes
- [CONFIRMADO_NO_CODIGO] Evento duplicado continua retornando `200`
- [CONFIRMADO_NO_CODIGO] Timestamp antigo continua retornando `400`
- [CONFIRMADO_NO_CODIGO] Evento desconhecido continua `200` sem efeito financeiro
- [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_security.py` continua com `8 passed`
- [CONFIRMADO_NO_CODIGO] Suite completa continua com `30 passed`
- [INFERIDO_DO_CODIGO] [billing/views.py](/c:/projectos/JurisAI/billing/views.py) fica reduzido a HTTP + validacao semantica por tipo + mapeamento de resultado
