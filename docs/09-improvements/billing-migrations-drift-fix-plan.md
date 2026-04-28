# Billing Migrations Drift Fix Plan

## 1. Resumo do drift

- [CONFIRMADO_NO_CODIGO] O app `billing` define os models `Payment`, `Subscription`, `Invoice` e `BillingWebhookEvent`.
- [CONFIRMADO_NO_CODIGO] As migrations observadas do app criam apenas `Payment` e `BillingWebhookEvent`.
- [CONFIRMADO_NO_CODIGO] Nao ha migration observavel criando `billing_subscription` nem `billing_invoice`.
- [CONFIRMADO_NO_CODIGO] Isso deixa o schema migrado do app `billing` desalinhado com os models atuais.
- [CONFIRMADO_NO_CODIGO] Um efeito direto desse drift e o `skip` do teste de `Subscription` no orquestrador quando a tabela `billing_subscription` nao existe no banco de teste.

## 2. Evidencias no codigo

### Models atuais

- [CONFIRMADO_NO_CODIGO] [billing/models.py](/c:/projectos/JurisAI/billing/models.py) define:
  - `Payment`
  - `Subscription`
  - `Invoice`
  - `BillingWebhookEvent`

### Migrations atuais

- [CONFIRMADO_NO_CODIGO] [billing/migrations/0001_initial.py](/c:/projectos/JurisAI/billing/migrations/0001_initial.py) cria apenas `Payment`.
- [CONFIRMADO_NO_CODIGO] [billing/migrations/0002_billingwebhookevent.py](/c:/projectos/JurisAI/billing/migrations/0002_billingwebhookevent.py) cria apenas `BillingWebhookEvent`.
- [NÃO_ENCONTRADO] Nenhuma migration criando `Subscription`.
- [NÃO_ENCONTRADO] Nenhuma migration criando `Invoice`.

### Uso no codigo

- [CONFIRMADO_NO_CODIGO] `Subscription` e usada em:
  - [billing/views.py](/c:/projectos/JurisAI/billing/views.py)
  - [billing/serializers.py](/c:/projectos/JurisAI/billing/serializers.py)
  - [billing/services.py](/c:/projectos/JurisAI/billing/services.py)
  - [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)
  - [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py)
- [CONFIRMADO_NO_CODIGO] `Invoice` e usada em:
  - [billing/views.py](/c:/projectos/JurisAI/billing/views.py)
  - [billing/serializers.py](/c:/projectos/JurisAI/billing/serializers.py)
  - [billing/tasks.py](/c:/projectos/JurisAI/billing/tasks.py)
- [CONFIRMADO_NO_CODIGO] Os endpoints `subscriptions/` e `invoices/` estao registrados em [billing/urls.py](/c:/projectos/JurisAI/billing/urls.py).

## 3. Models afetados

### `Subscription`

- [CONFIRMADO_NO_CODIGO] FK obrigatoria para `organizations.Organization`
- [CONFIRMADO_NO_CODIGO] `stripe_subscription_id` com `unique=True`
- [CONFIRMADO_NO_CODIGO] `plan` obrigatorio
- [CONFIRMADO_NO_CODIGO] `status` com default `'active'`
- [CONFIRMADO_NO_CODIGO] `current_period_start`, `current_period_end` e `trial_end` nullable
- [CONFIRMADO_NO_CODIGO] `created_at` e `updated_at` automaticos

### `Invoice`

- [CONFIRMADO_NO_CODIGO] FK obrigatoria para `organizations.Organization`
- [CONFIRMADO_NO_CODIGO] `stripe_invoice_id` com `unique=True`
- [CONFIRMADO_NO_CODIGO] `amount` obrigatorio
- [CONFIRMADO_NO_CODIGO] `status` com default `'open'`
- [CONFIRMADO_NO_CODIGO] `due_date` e `paid_at` nullable
- [CONFIRMADO_NO_CODIGO] `created_at` e `updated_at` automaticos

## 4. Tabelas ausentes

- [CONFIRMADO_NO_CODIGO] `billing_subscription`
- [CONFIRMADO_NO_CODIGO] `billing_invoice`

## 5. Dependencias

- [CONFIRMADO_NO_CODIGO] As migrations do app `billing` dependem de `organizations.0001_initial`.
- [CONFIRMADO_NO_CODIGO] `Payment`, `Subscription`, `Invoice` e `BillingWebhookEvent` dependem de `organizations.Organization`.
- [NÃO_ENCONTRADO] Dependencia direta de `accounts.User` nesses models do `billing`.
- [INFERIDO_DO_CODIGO] A migration corretiva deve depender de `billing.0002_billingwebhookevent` para manter a ordem historica.

## 6. Estrategia recomendada

- [INFERIDO_DO_CODIGO] Criar uma nova migration `0003` no app `billing` que crie `Subscription` e `Invoice`.
- [INFERIDO_DO_CODIGO] A migration deve ser revista manualmente antes de aplicar, mesmo que `makemigrations` gere a base automaticamente.
- [CONFIRMADO_NO_CODIGO] Essa abordagem preserva o historico de migrations existente e alinha o schema ao codigo atual sem editar migrations ja aplicadas.
- [INFERIDO_DO_CODIGO] Depois da migration, o teste atualmente marcado com `skip` deve poder ser endurecido para exigir a tabela.

### Ordem segura sugerida

1. gerar migration candidata com `makemigrations billing`
2. revisar manualmente o arquivo gerado
3. validar dependencias, nomes de tabela, `unique=True`, `null=True`, defaults e FKs
4. recriar ou atualizar banco de teste sem depender de schema reutilizado desatualizado
5. reexecutar a suite do service, a suite focal do webhook e a suite completa
6. remover o `skip` do teste de `Subscription` apenas depois de confirmar o schema estavel

## 7. Alternativa com migration manual

- [INFERIDO_DO_CODIGO] Se `makemigrations` gerar algo inesperado ou poluido por drift adicional, a alternativa e criar manualmente uma migration `0003` com dois `CreateModel`.
- [INFERIDO_DO_CODIGO] Essa opcao pode ser mais segura se a equipa quiser controle total sobre:
  - nomes de campos
  - choices
  - defaults
  - `null` / `blank`
  - FKs
  - ordem exata das operacoes
- [INFERIDO_DO_CODIGO] Mesmo nessa opcao, o conteudo manual deve espelhar exatamente `billing/models.py`.

## 8. Riscos de ambientes existentes

- [PRECISA_VALIDAR] O banco atual de desenvolvimento ou producao pode ja ter `billing_subscription` e `billing_invoice` criadas manualmente fora das migrations.
- [NÃO_ENCONTRADO] Evidencia no repositorio de criacao manual dessas tabelas.
- [INFERIDO_DO_CODIGO] Se essas tabelas ja existirem em algum ambiente, uma migration `CreateModel` pura pode colidir com erro de tabela existente.
- [PRECISA_VALIDAR] E necessario validar com a equipa se ha ambientes antigos com schema divergente.

### Estrategia para evitar colisao

- [INFERIDO_DO_CODIGO] Em ambiente local/teste, a estrategia ideal e recriar o banco de teste a partir das migrations corrigidas.
- [PRECISA_VALIDAR] Para ambientes existentes compartilhados, pode ser necessario:
  - inspecionar se as tabelas ja existem
  - comparar schema real com os models atuais
  - decidir entre migration padrao, migration manual especial ou procedimento operacional controlado
- [INFERIDO_DO_CODIGO] Se houver chance real de tabela preexistente, a migration deve ser revisada manualmente com esse risco em mente antes de aplicar.

## 9. Plano de backup/rollback

1. Fazer backup do banco antes de aplicar migration em ambiente persistente.  
   [PRECISA_VALIDAR] Procedimento exato depende do ambiente alvo.
2. Aplicar a migration primeiro em ambiente local/teste recriado.
3. Se houver falha:
   - reverter a nova migration `0003`
   - restaurar o banco a partir do backup, se necessario
   - manter temporariamente o `skip` do teste de `Subscription`
4. Reexecutar:
   - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_services.py`
   - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_security.py`
   - `.\.venv\Scripts\python.exe -m pytest`

## 10. Plano de implementacao

### Fase 1: preparar migration candidata

- [INFERIDO_DO_CODIGO] Rodar `makemigrations billing`
- [INFERIDO_DO_CODIGO] Inspecionar se a migration gerada cria apenas `Subscription` e `Invoice`

### Fase 2: revisar manualmente

- [CONFIRMADO_NO_CODIGO] Conferir:
  - FKs para `organizations.Organization`
  - `unique=True` em `stripe_subscription_id` e `stripe_invoice_id`
  - defaults de `status`
  - campos nullable
  - timestamps automáticos

### Fase 3: validar schema em banco de teste limpo

- [INFERIDO_DO_CODIGO] Recriar banco de teste para evitar efeito de `--reuse-db`
- [INFERIDO_DO_CODIGO] Confirmar existencia de:
  - `billing_payment`
  - `billing_subscription`
  - `billing_invoice`
  - `billing_webhookevent`

### Fase 4: endurecer teste hoje skipped

- [INFERIDO_DO_CODIGO] Remover o `skip` de `test_process_billing_webhook_event_updates_subscription_event`
- [INFERIDO_DO_CODIGO] Tornar o teste obrigatorio depois que o schema estiver estavel

## 11. Plano de testes

- [INFERIDO_DO_CODIGO] Rodar primeiro a suite do service:
  - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_services.py`
- [INFERIDO_DO_CODIGO] Rodar depois a suite focal do webhook:
  - `.\.venv\Scripts\python.exe -m pytest tests/test_billing_webhook_security.py`
- [INFERIDO_DO_CODIGO] Rodar por fim a suite completa:
  - `.\.venv\Scripts\python.exe -m pytest`
- [INFERIDO_DO_CODIGO] Se o banco de teste reutilizado continuar contaminando o resultado, recriar explicitamente o banco de teste antes da rodada final.

## 12. Criterios de aceitacao

- [CONFIRMADO_NO_CODIGO] O app `billing` passa a ter migration observavel para `Subscription` e `Invoice`.
- [CONFIRMADO_NO_CODIGO] `billing_subscription` e `billing_invoice` passam a existir em banco de teste criado a partir das migrations corrigidas.
- [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_services.py` passa sem `skip`.
- [CONFIRMADO_NO_CODIGO] `tests/test_billing_webhook_security.py` continua passando.
- [CONFIRMADO_NO_CODIGO] A suite completa continua passando.
- [CONFIRMADO_NO_CODIGO] O drift entre `billing/models.py` e migrations do app `billing` fica resolvido para esses models.

## 13. Perguntas para validacao humana

1. [PRECISA_VALIDAR] Existe algum ambiente de desenvolvimento ou producao onde `billing_subscription` ou `billing_invoice` ja tenham sido criadas manualmente?
2. [PRECISA_VALIDAR] A equipa prefere confiar numa migration gerada por `makemigrations` com revisao manual, ou prefere escrever a `0003` manualmente desde o inicio?
3. [PRECISA_VALIDAR] Podemos recriar o banco de teste local depois da correcao para eliminar os efeitos de `--reuse-db`?
4. [PRECISA_VALIDAR] Ha algum dado real em `Subscription` ou `Invoice` fora do fluxo normal de migrations que precise de verificacao previa?

## 14. Estado apos implementacao

- [CONFIRMADO_NO_CODIGO] A migration [billing/migrations/0003_subscription_invoice.py](/c:/projectos/JurisAI/billing/migrations/0003_subscription_invoice.py) foi mantida como correcao controlada do app `billing`.
- [CONFIRMADO_NO_CODIGO] A migration inesperada `organizations/migrations/0002_alter_organization_plan.py` foi descartada e nao faz parte desta correcao.
- [CONFIRMADO_NO_CODIGO] A dependencia final da `billing.0003` aponta para:
  - `billing.0002_billingwebhookevent`
  - `organizations.0001_initial`
- [CONFIRMADO_NO_CODIGO] A `billing.0003` cria apenas `Subscription` e `Invoice`.
- [CONFIRMADO_NO_CODIGO] A migracao foi validada localmente com:
  - `$env:DJANGO_USE_SQLITE='True'; .\.venv\Scripts\python.exe manage.py migrate`
- [CONFIRMADO_NO_CODIGO] O `skip` do teste de `Subscription` foi removido depois da criacao migrada da tabela.
- [CONFIRMADO_NO_CODIGO] Resultados apos a correcao:
  - `tests/test_billing_webhook_services.py`: `5 passed`
  - `tests/test_billing_webhook_security.py`: `8 passed`
  - suite completa: `35 passed`
- [PRECISA_VALIDAR] Continua pendente, em item separado, o drift de `organizations.plan`, que nao foi arrastado para esta correcao.
