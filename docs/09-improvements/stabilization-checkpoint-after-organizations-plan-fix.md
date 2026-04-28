# Stabilization Checkpoint After Organizations Plan Fix

## 1. Resumo da correcao

- [CONFIRMADO_NO_CODIGO] O drift de `Organization.plan` foi corrigido em frente propria, sem misturar a mudanca com `billing`.
- [CONFIRMADO_NO_CODIGO] O projeto foi preparado em camadas:
  - seeds deixaram de usar `starter`
  - fallback residual de IA deixou de usar `starter`
  - migration de schema alinhou `Organization.plan` ao enum atual
  - data migration converteu `starter -> free`

## 2. Arquivos principais alterados

- [accounts/management/commands/seed_initial.py](/c:/projectos/JurisAI/accounts/management/commands/seed_initial.py)
- [accounts/management/commands/seed_demo.py](/c:/projectos/JurisAI/accounts/management/commands/seed_demo.py)
- [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py)
- [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py)
- [tests/test_organization_plan_seeds.py](/c:/projectos/JurisAI/tests/test_organization_plan_seeds.py)
- [tests/test_ai_plan_limits.py](/c:/projectos/JurisAI/tests/test_ai_plan_limits.py)

## 3. Migration criada

- [CONFIRMADO_NO_CODIGO] Foi criada [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py).

## 4. Data migration aplicada

- [CONFIRMADO_NO_CODIGO] A migration inclui `RunPython` para converter registros antigos com `plan='starter'` para `plan='free'`.
- [CONFIRMADO_NO_CODIGO] A reversao da data migration foi mantida como `noop` para evitar reclassificar incorretamente organizacoes `free` legitimas em rollback.

## 5. Mapeamento `starter -> free`

- [CONFIRMADO_NO_CODIGO] O mapeamento aplicado foi `starter -> free`.
- [CONFIRMADO_NO_CODIGO] Esse mapeamento aparece em:
  - alinhamento dos seeds
  - alinhamento do fallback `PLAN_IA_LIMITS`
  - data migration da `organizations.0002`

## 6. Testes criados

- [CONFIRMADO_NO_CODIGO] [tests/test_organization_plan_seeds.py](/c:/projectos/JurisAI/tests/test_organization_plan_seeds.py)
- [CONFIRMADO_NO_CODIGO] [tests/test_ai_plan_limits.py](/c:/projectos/JurisAI/tests/test_ai_plan_limits.py)

## 7. Resultado da suite

- [CONFIRMADO_NO_CODIGO] `.\.venv\Scripts\python.exe -m pytest`
- [CONFIRMADO_NO_CODIGO] Resultado: `38 passed`

## 8. Riscos mitigados

- [CONFIRMADO_NO_CODIGO] Seeds e bootstrap local deixaram de reintroduzir `starter`.
- [CONFIRMADO_NO_CODIGO] O fallback residual de IA deixou de referenciar plano antigo.
- [CONFIRMADO_NO_CODIGO] O schema migrado de `Organization.plan` passou a refletir o enum atual.
- [CONFIRMADO_NO_CODIGO] Dados antigos com `starter` passaram a ter caminho de conversao controlado para `free`.

## 9. Riscos restantes

- [CONFIRMADO_NO_CODIGO] A aplicacao local de `manage.py migrate` continua dependente do ambiente; neste workspace a validacao de migrations reais precisou de SQLite local porque o host Postgres padrao `db` nao estava disponivel.
- [CONFIRMADO_NO_CODIGO] Permanecem warnings tecnicos conhecidos:
  - `USE_L10N`
  - `InsecureKeyLengthWarning`
  - `UnorderedObjectListWarning`
- [PRECISA_VALIDAR] Ambientes reais com historico antigo ainda exigem validacao operacional antes da aplicacao da migration, mesmo com a data migration incluida.

## 10. Observacao sobre validacao operacional em ambientes reais

- [PRECISA_VALIDAR] Antes de aplicar `organizations.0002` em ambiente persistente, a equipa deve confirmar:
  - existencia ou nao de organizacoes com `starter`
  - janela segura para migracao
  - politica de backup/rollback
- [CONFIRMADO_NO_CODIGO] No ambiente local validado, a migracao nao removeu organizacoes e a suite completa permaneceu verde.

## 11. Recomendacao do proximo ciclo

- [INFERIDO_DO_CODIGO] O proximo ciclo mais seguro e voltar para divida tecnica de baixo/medio risco que nao mexa em contratos:
  - melhorar o ambiente local de `manage.py migrate` sem depender do host `db`
  - ou continuar a refatoracao interna do webhook/validacoes ainda concentradas em views
