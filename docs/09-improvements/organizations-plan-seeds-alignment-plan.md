# Organizations Plan Seeds Alignment Plan

## 1. Resumo do problema

- [CONFIRMADO_NO_CODIGO] O model e a API de `Organization.plan` usam `free`, `solo`, `growth` e `enterprise`.
- [CONFIRMADO_NO_CODIGO] Os comandos [accounts/management/commands/seed_initial.py](/c:/projectos/JurisAI/accounts/management/commands/seed_initial.py) e [accounts/management/commands/seed_demo.py](/c:/projectos/JurisAI/accounts/management/commands/seed_demo.py) ainda criam organizacoes com `plan='starter'`.
- [CONFIRMADO_NO_CODIGO] Isso reintroduz um valor que ja nao faz parte do enum oficial do model atual.
- [CONFIRMADO_NO_CODIGO] O objetivo desta frente e alinhar seeds e setup antes de qualquer migration de schema em `organizations`.

## 2. Arquivos afetados

- [CONFIRMADO_NO_CODIGO] [accounts/management/commands/seed_initial.py](/c:/projectos/JurisAI/accounts/management/commands/seed_initial.py)
- [CONFIRMADO_NO_CODIGO] [accounts/management/commands/seed_demo.py](/c:/projectos/JurisAI/accounts/management/commands/seed_demo.py)
- [CONFIRMADO_NO_CODIGO] [accounts/management/commands/setup_local.py](/c:/projectos/JurisAI/accounts/management/commands/setup_local.py)
- [CONFIRMADO_NO_CODIGO] [README.md](/c:/projectos/JurisAI/README.md) referencia `seed_demo` e `setup_local` como fluxo de bootstrap
- [PRECISA_VALIDAR] Eventuais docs operacionais adicionais que ainda mencionem `starter`

## 3. Valores antigos encontrados

- [CONFIRMADO_NO_CODIGO] `seed_initial.py` usa `default='starter'` no argumento `--plan`.
- [CONFIRMADO_NO_CODIGO] `seed_demo.py` usa `defaults={'plan': 'starter'}`.
- [CONFIRMADO_NO_CODIGO] `organizations/migrations/0001_initial.py` usa `starter/growth/enterprise` com default `starter`.
- [CONFIRMADO_NO_CODIGO] [docs/11-review/documentation-review-report.md](/c:/projectos/JurisAI/docs/11-review/documentation-review-report.md) ja registra esse drift.
- [CONFIRMADO_NO_CODIGO] [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py) ainda contem um mapa local com chave `starter`, mas isso fica fora do escopo imediato desta correcao de seeds.

## 4. Valores atuais esperados

- [CONFIRMADO_NO_CODIGO] [organizations/models.py](/c:/projectos/JurisAI/organizations/models.py) define:
  - `free`
  - `solo`
  - `growth`
  - `enterprise`
- [CONFIRMADO_NO_CODIGO] [organizations/views.py](/c:/projectos/JurisAI/organizations/views.py) expoe esses mesmos planos no endpoint de planos.
- [CONFIRMADO_NO_CODIGO] Os testes atuais criam `Organization(plan='free')`.

## 5. Mapeamento recomendado

- [INFERIDO_DO_CODIGO] O mapeamento mais seguro para `starter` nos seeds e setup e `starter -> free`.

### Justificativa

- [CONFIRMADO_NO_CODIGO] O model atual usa `default='free'`.
- [CONFIRMADO_NO_CODIGO] Os testes atuais estao padronizados em `free`.
- [CONFIRMADO_NO_CODIGO] O endpoint `organizations/plans/` apresenta `free` como plano de entrada.
- [INFERIDO_DO_CODIGO] `solo` parece um plano pago/intermediario e nao substituto natural do bootstrap minimo.

### Alternativas

- [PRECISA_VALIDAR] `starter -> solo` so faria sentido se a equipa confirmar que `starter` representava um plano pago individual.
- [NÃO_ENCONTRADO] Evidencia no codigo de que `starter` devesse mapear para `solo`.

## 6. Impacto nos dados de demo

- [CONFIRMADO_NO_CODIGO] `seed_demo.py` cria a organizacao base do ambiente local.
- [INFERIDO_DO_CODIGO] Trocar `starter` por `free` alinha o demo com o enum atual sem alterar schema.
- [INFERIDO_DO_CODIGO] O demo passara a refletir os limites atuais do plano `free`, o que e mais consistente com o dominio atual.

## 7. Impacto no setup inicial

- [CONFIRMADO_NO_CODIGO] `setup_local.py` chama `migrate` e depois `seed_demo`.
- [INFERIDO_DO_CODIGO] Ao alinhar `seed_demo.py`, o `setup_local` deixa automaticamente de reintroduzir `starter`.
- [CONFIRMADO_NO_CODIGO] `seed_initial.py` tambem precisa ser alinhado para que o CLI manual nao continue oferecendo um valor invalido por default.
- [PRECISA_VALIDAR] Se a equipa quiser preservar flexibilidade, o argumento `--plan` de `seed_initial.py` pode continuar existindo, mas com default valido.

## 8. Plano de implementacao

### Fase 1: alinhar defaults

1. Alterar o default de `--plan` em `seed_initial.py` de `starter` para `free`.
2. Alterar `seed_demo.py` para usar `plan='free'`.

### Fase 2: alinhar fluxo de bootstrap

1. Verificar se `setup_local.py` precisa apenas de documentacao atualizada ou se nenhuma mudanca de codigo e necessaria alem do seed.
2. Revisar `README.md` e docs operacionais que mencionem bootstrap local.

### Fase 3: endurecer contra regressao

1. Adicionar teste simples cobrindo que os seeds nao usam `starter`.
2. Validar que o ambiente local continua funcional com os comandos atuais.

## 9. Plano de testes

- [INFERIDO_DO_CODIGO] Adicionar teste de regressao pequeno e focado para impedir retorno de `starter` nos comandos de seed.
- [INFERIDO_DO_CODIGO] Rodar depois:
  - `.\.venv\Scripts\python.exe -m pytest`
- [PRECISA_VALIDAR] Se houver teste especifico para management commands, incluir:
  - `seed_initial`
  - `seed_demo`

## 10. Riscos

- [PRECISA_VALIDAR] Se algum ambiente operacional ainda depender semanticamente de `starter`, trocar para `free` pode mudar limites percebidos no bootstrap.
- [CONFIRMADO_NO_CODIGO] O uso isolado de `starter` em `ai_assistant/services/ai_service.py` continuaria existindo mesmo apos alinhar os seeds.
- [INFERIDO_DO_CODIGO] Corrigir apenas os seeds nao resolve sozinho o drift de schema de `organizations.plan`, mas evita que o problema continue sendo reintroduzido.

## 11. Rollback plan

1. Reverter apenas as alteracoes em `seed_initial.py`, `seed_demo.py` e docs relacionadas.
2. Reexecutar a suite para confirmar retorno ao estado anterior.
3. Manter a migration de `organizations.plan` fora do escopo ate nova validacao.

## 12. Criterios de aceitacao

- [INFERIDO_DO_CODIGO] `seed_initial.py` deixa de usar `starter` por default.
- [INFERIDO_DO_CODIGO] `seed_demo.py` deixa de criar organizacao com `starter`.
- [INFERIDO_DO_CODIGO] `setup_local` deixa de reintroduzir `starter` de forma indireta.
- [INFERIDO_DO_CODIGO] Existe pelo menos um teste de regressao impedindo retorno de `starter` nos seeds.
- [CONFIRMADO_NO_CODIGO] Nenhuma migration e criada nesta fase.

## 13. Perguntas para validacao humana

1. [PRECISA_VALIDAR] A equipa concorda com `starter -> free` como mapeamento operacional para bootstrap e demo?
2. [PRECISA_VALIDAR] O argumento `--plan` em `seed_initial.py` deve continuar exposto ao utilizador ou pode ser endurecido para choices validos no proximo passo?
3. [PRECISA_VALIDAR] O uso residual de `starter` em `ai_assistant/services/ai_service.py` deve ser tratado no mesmo ciclo ou em frente separada?

## 14. Estado apos implementacao

- [CONFIRMADO_NO_CODIGO] O mapeamento aplicado nesta etapa foi `starter -> free`.
- [CONFIRMADO_NO_CODIGO] `seed_initial.py` passou a usar `default='free'`.
- [CONFIRMADO_NO_CODIGO] `seed_demo.py` passou a criar organizacao demo com `plan='free'`.
- [CONFIRMADO_NO_CODIGO] Foi adicionada a suite [tests/test_organization_plan_seeds.py](/c:/projectos/JurisAI/tests/test_organization_plan_seeds.py) para impedir regressao.
- [CONFIRMADO_NO_CODIGO] Nenhuma migration foi criada.
