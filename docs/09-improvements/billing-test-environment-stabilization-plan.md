# Billing Test Environment Stabilization Plan

## 1. Resumo do problema

- [CONFIRMADO_NO_CODIGO] O teste `test_process_billing_webhook_event_updates_subscription_event` em [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py) deixava de rodar quando a tabela `billing_subscription` nao existia no banco de teste atual.
- [CONFIRMADO_NO_CODIGO] A correcao do drift do app `billing` removeu esse bloqueio.
- [CONFIRMADO_NO_CODIGO] A suite do service agora fecha com `5 passed`.
- [CONFIRMADO_NO_CODIGO] A suite focal do webhook fecha com `8 passed`.
- [CONFIRMADO_NO_CODIGO] A suite completa fecha com `34 passed, 1 skipped`.

## 2. Evidencias encontradas

- [CONFIRMADO_NO_CODIGO] [billing/models.py](/c:/projectos/JurisAI/billing/models.py) define quatro models persistentes:
  - `Payment`
  - `Subscription`
  - `Invoice`
  - `BillingWebhookEvent`
- [CONFIRMADO_NO_CODIGO] A pasta [billing/migrations](/c:/projectos/JurisAI/billing/migrations) contem apenas:
  - `0001_initial.py`
  - `0002_billingwebhookevent.py`
- [CONFIRMADO_NO_CODIGO] [billing/migrations/0001_initial.py](/c:/projectos/JurisAI/billing/migrations/0001_initial.py) cria apenas o model `Payment`.
- [CONFIRMADO_NO_CODIGO] [billing/migrations/0002_billingwebhookevent.py](/c:/projectos/JurisAI/billing/migrations/0002_billingwebhookevent.py) cria apenas `BillingWebhookEvent`.
- [CONFIRMADO_NO_CODIGO] Nao ha migration encontrada para criar `billing_subscription`.
- [CONFIRMADO_NO_CODIGO] Nao ha migration encontrada para criar `billing_invoice`.
- [CONFIRMADO_NO_CODIGO] [pytest.ini](/c:/projectos/JurisAI/pytest.ini) usa `--reuse-db`.
- [CONFIRMADO_NO_CODIGO] Nao foi encontrado `conftest.py` na raiz do projeto com workaround de schema de teste.
- [CONFIRMADO_NO_CODIGO] [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py) e [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py) ja usam protecao por introspeccao da tabela antes de validar cenarios de `Subscription`.

## 3. Causa provavel

- [CONFIRMADO_NO_CODIGO] A causa principal provavel e drift entre models e migrations do app `billing`.
- [CONFIRMADO_NO_CODIGO] Como `Subscription` e `Invoice` existem no codigo, mas nao nas migrations observadas, um banco de teste criado a partir das migrations nao tem como criar essas tabelas.
- [INFERIDO_DO_CODIGO] O uso de `--reuse-db` pode mascarar ou variar o problema dependendo do estado anterior do banco local, mas nao parece ser a causa raiz.
- [CONFIRMADO_NO_CODIGO] O `skip` era um workaround defensivo para conviver com esse drift, nao uma necessidade funcional do dominio.

## 4. Opcoes de correcao

### Opcao A: corrigir apenas os testes/fixtures

- [INFERIDO_DO_CODIGO] Manter o `skip` e talvez expandir fixtures de teste.
- [INFERIDO_DO_CODIGO] Isso evita mexer em schema no curto prazo.
- [CONFIRMADO_NO_CODIGO] Isso nao resolve a ausencia real das tabelas `billing_subscription` e `billing_invoice`.
- [INFERIDO_DO_CODIGO] Continuaria a esconder um problema estrutural do app `billing`.

### Opcao B: forcar criacao de tabelas fora das migrations

- [INFERIDO_DO_CODIGO] Usar setup de teste customizado, schema editor ou fixture especial para criar tabelas em runtime.
- [CONFIRMADO_NO_CODIGO] Nao ha evidencia de que o projeto siga esse padrao hoje.
- [INFERIDO_DO_CODIGO] Isso adicionaria complexidade e aumentaria divergencia entre ambiente de teste e ambiente real.

### Opcao C: alinhar migrations do app `billing` aos models atuais

- [INFERIDO_DO_CODIGO] Criar migration(s) faltante(s) para `Subscription` e `Invoice`.
- [CONFIRMADO_NO_CODIGO] Esta e a unica opcao que resolve a causa estrutural observada.
- [INFERIDO_DO_CODIGO] Tambem tende a eliminar o `skip` do teste de `Subscription` sem hacks no ambiente.

## 5. Opcao recomendada

- [INFERIDO_DO_CODIGO] A opcao recomendada e corrigir as migrations do app `billing`, nao apenas fixtures/testes.
- [CONFIRMADO_NO_CODIGO] O problema observado nao parece ser falta de fixture; parece ausencia de schema migrado para models existentes.
- [CONFIRMADO_NO_CODIGO] Essa estrategia foi aplicada com uma migration nova do `billing`, sem arrastar a migration inesperada de `organizations`.

## 6. Impacto em migrations

- [CONFIRMADO_NO_CODIGO] Sera necessario tocar em migrations para estabilizar o ambiente de teste de forma correta.
- [INFERIDO_DO_CODIGO] O ideal e gerar uma nova migration do app `billing` que crie `Subscription` e `Invoice`, preservando o historico existente.
- [PRECISA_VALIDAR] E preciso validar se ja existem bancos reais rodando com tabelas manuais ou estados divergentes, para evitar conflito em ambientes partilhados.

## 7. Impacto em testes

- [CONFIRMADO_NO_CODIGO] Depois de alinhar migrations, o teste antes marcado com `skip` passou a rodar normalmente.
- [CONFIRMADO_NO_CODIGO] Estado atual:
  - `tests/test_billing_webhook_services.py` -> `5 passed`
  - `tests/test_billing_webhook_security.py` -> `8 passed`
  - suite completa -> `35 passed`

## 8. Riscos

- [CONFIRMADO_NO_CODIGO] Risco de haver drift adicional entre migrations e models no app `billing`, alem de `Subscription` e `Invoice`.
- [INFERIDO_DO_CODIGO] Risco de a migration corretiva expor inconsistencias em ambientes locais que hoje passam despercebidas.
- [INFERIDO_DO_CODIGO] Risco operacional com `--reuse-db`: depois da correcao, pode ser necessario recriar o banco de teste para validar corretamente o novo schema.

## 9. Rollback plan

1. Reverter apenas a migration corretiva do app `billing`, se ainda nao tiver sido aplicada amplamente.
2. Restaurar temporariamente o `skip` do teste de `Subscription` se a correcao de schema nao puder seguir.
3. Reexecutar:
   - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_services.py`
   - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_security.py`
   - `.\.venv\Scripts\python.exe -m pytest`

## 10. Criterios de aceitacao

- [CONFIRMADO_NO_CODIGO] O banco de teste passa a conter `billing_subscription` e `billing_invoice` via migrations normais.
- [CONFIRMADO_NO_CODIGO] O `skip` do teste de `Subscription` deixou de ser necessario.
- [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_services.py` passou integralmente sem `skip`.
- [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_security.py` continua passando.
- [CONFIRMADO_NO_CODIGO] A suite completa continua passando.
- [INFERIDO_DO_CODIGO] O ambiente de teste fica mais coerente com o schema real esperado pelo codigo.
