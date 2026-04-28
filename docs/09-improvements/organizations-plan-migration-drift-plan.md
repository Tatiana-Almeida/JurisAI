# Organizations Plan Migration Drift Plan

## 1. Resumo do drift

- [CONFIRMADO_NO_CODIGO] O model atual de `Organization.plan` usa os valores `free`, `solo`, `growth` e `enterprise`.
- [CONFIRMADO_NO_CODIGO] A migration inicial `organizations/0001_initial.py` define `Organization.plan` com `starter`, `growth` e `enterprise`, e default `starter`.
- [CONFIRMADO_NO_CODIGO] `makemigrations organizations --dry-run --verbosity 3` tenta gerar `organizations/migrations/0002_alter_organization_plan.py` com um `AlterField` para alinhar a migration ao model atual.
- [CONFIRMADO_NO_CODIGO] O drift de `organizations.plan` e separado do drift ja corrigido no app `billing`.

## 2. Evidencias no codigo

### Model atual

- [CONFIRMADO_NO_CODIGO] [organizations/models.py](/c:/projectos/JurisAI/organizations/models.py) define:
  - `choices=[('free', 'Free'), ('solo', 'Solo'), ('growth', 'Escritorio'), ('enterprise', 'Enterprise')]`
  - `default='free'`
  - `max_length=50`

### Migration inicial

- [CONFIRMADO_NO_CODIGO] [organizations/migrations/0001_initial.py](/c:/projectos/JurisAI/organizations/migrations/0001_initial.py) define:
  - `choices=[('starter', 'Starter'), ('growth', 'Growth'), ('enterprise', 'Enterprise')]`
  - `default='starter'`
  - `max_length=50`

### Saida esperada de makemigrations

- [CONFIRMADO_NO_CODIGO] O comando abaixo gera uma migration candidata sem aplicar nada:
  - `$env:DJANGO_USE_SQLITE='True'; .\.venv\Scripts\python.exe manage.py makemigrations organizations --dry-run --verbosity 3`
- [CONFIRMADO_NO_CODIGO] A migration candidata observada e:

```python
migrations.AlterField(
    model_name='organization',
    name='plan',
    field=models.CharField(
        choices=[
            ('free', 'Free'),
            ('solo', 'Solo'),
            ('growth', 'Escritorio'),
            ('enterprise', 'Enterprise'),
        ],
        default='free',
        max_length=50,
    ),
)
```

## 3. Diferenca entre model e migration

- [CONFIRMADO_NO_CODIGO] Mudou o conjunto de `choices`:
  - removido: `starter`
  - adicionados: `free`, `solo`
- [CONFIRMADO_NO_CODIGO] Mudou o `default`:
  - de `starter`
  - para `free`
- [CONFIRMADO_NO_CODIGO] `max_length` permaneceu `50`.
- [CONFIRMADO_NO_CODIGO] `nullability` nao mudou.
- [CONFIRMADO_NO_CODIGO] O campo continua obrigatorio.

## 4. Impacto em dados existentes

- [PRECISA_VALIDAR] Se existirem registros de `Organization` com `plan='starter'`, a migration de schema isolada nao corrige esses dados.
- [INFERIDO_DO_CODIGO] Como o campo e `CharField` com `choices`, o banco provavelmente aceita valores antigos, mas o model e a aplicacao deixam de reconhece-los semanticamente.
- [INFERIDO_DO_CODIGO] Organizacoes antigas com `starter` podem continuar a existir no banco e cair no fallback dos metodos `max_users`, `max_cases`, `max_documents` e `ai_request_limit`.
- [CONFIRMADO_NO_CODIGO] Esses metodos usam `.get(self.plan, fallback)` em [organizations/models.py](/c:/projectos/JurisAI/organizations/models.py), entao valores inesperados nao quebram imediatamente, mas ficam semanticamente desalinhados.

## 5. Impacto em billing e subscriptions

- [CONFIRMADO_NO_CODIGO] `billing/models.py` referencia `Organization` por FK, mas nao define FK ou enum dependente de `Organization.plan`.
- [CONFIRMADO_NO_CODIGO] `Subscription.plan` em [billing/models.py](/c:/projectos/JurisAI/billing/models.py) e um `CharField` independente, sem `choices`.
- [INFERIDO_DO_CODIGO] O impacto em `billing` e indireto:
  - inconsistencias de plano podem afetar semantica de negocio ou comunicacao com o usuario
  - nao parecem afetar o schema ou a integridade relacional do `billing`

## 5.1 Impacto em limites de IA

- [CONFIRMADO_NO_CODIGO] [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py) tinha um fallback local `PLAN_IA_LIMITS` ainda com chave `starter`.
- [CONFIRMADO_NO_CODIGO] O caminho principal para `Organization` real usa `organization.ai_request_limit()` quando esse metodo existe.
- [INFERIDO_DO_CODIGO] Isso tornava o mapa local um fallback antigo, relevante sobretudo para objetos sem `ai_request_limit`.
- [CONFIRMADO_NO_CODIGO] O fallback residual ja foi alinhado para `free`, `solo`, `growth` e `enterprise`, sem criar migration.

## 6. Impacto em seeds e fixtures

- [CONFIRMADO_NO_CODIGO] Antes da correcao de seeds, [accounts/management/commands/seed_initial.py](/c:/projectos/JurisAI/accounts/management/commands/seed_initial.py) usava `default='starter'` no argumento `--plan`.
- [CONFIRMADO_NO_CODIGO] Antes da correcao de seeds, [accounts/management/commands/seed_demo.py](/c:/projectos/JurisAI/accounts/management/commands/seed_demo.py) criava organizacao demo com `defaults={'plan': 'starter'}`.
- [CONFIRMADO_NO_CODIGO] [organizations/views.py](/c:/projectos/JurisAI/organizations/views.py) ja expoe os planos `free`, `solo`, `growth`, `enterprise`.
- [CONFIRMADO_NO_CODIGO] Os testes atuais usam `plan='free'`.
- [CONFIRMADO_NO_CODIGO] Nesta fase previa ao schema, os dois seeds foram alinhados para `free` e passaram a ter teste de regressao proprio.
- [CONFIRMADO_NO_CODIGO] A documentacao ja registra essa divergencia em:
  - [docs/11-review/documentation-review-report.md](/c:/projectos/JurisAI/docs/11-review/documentation-review-report.md)
  - [docs/07-quality/refactoring-plan.md](/c:/projectos/JurisAI/docs/07-quality/refactoring-plan.md)
  - [docs/02-database/migrations-analysis.md](/c:/projectos/JurisAI/docs/02-database/migrations-analysis.md)

## 7. Estrategia recomendada

- [INFERIDO_DO_CODIGO] Tratar a correcao em duas partes coordenadas, nao como migration de schema isolada:
  1. alinhar os seeds e comandos para deixarem de produzir `starter`
  2. criar migration de schema para `AlterField`
  3. avaliar se e necessario data migration para converter `starter -> free` ou outro mapeamento aprovado
- [INFERIDO_DO_CODIGO] A migration de schema sozinha e pequena, mas pode deixar dados antigos e scripts de setup desalinhados.
- [INFERIDO_DO_CODIGO] O caminho mais seguro e aprovar primeiro o mapeamento funcional de `starter`:
  - `starter -> free`
  - ou outro mapeamento de negocio validado pela equipa

## 8. Alternativa conservadora

- [INFERIDO_DO_CODIGO] Nao criar a migration ainda.
- [INFERIDO_DO_CODIGO] Primeiro corrigir apenas seeds, setup e documentacao operacional para usar `free`.
- [INFERIDO_DO_CODIGO] Depois medir se ainda existem dados reais com `starter`.
- [INFERIDO_DO_CODIGO] So entao criar:
  - uma migration de schema (`AlterField`)
  - opcionalmente uma data migration

Essa alternativa reduz risco operacional se houver ambientes antigos com dados reais fora do padrao atual.

## 9. Plano de implementacao

### Fase 1: levantamento e decisao funcional

1. [PRECISA_VALIDAR] Confirmar com a equipa qual e o mapeamento correto de `starter`.
2. [PRECISA_VALIDAR] Verificar se existem dados reais com `plan='starter'` nos ambientes alvo.

### Fase 2: alinhamento operacional

1. Atualizar `seed_initial.py` para default valido no model atual.
2. Atualizar `seed_demo.py` para criar organizacao demo com plano valido.
3. Revisar README/setup se ainda mencionarem comportamento antigo.

### Fase 3: schema

1. Gerar `organizations/0002_alter_organization_plan.py`.
2. Revisar manualmente a migration candidata antes de aplicar.
3. Confirmar que ela altera apenas `Organization.plan`.

### Fase 4: dados

1. [PRECISA_VALIDAR] Se existirem registros `starter`, criar data migration ou script operacional controlado.
2. Validar que nenhum fluxo relevante continua dependente de `starter`.

## 10. Plano de testes

- Rodar:
  - `.\.venv\Scripts\python.exe -m pytest`
- Adicionar ou revisar depois da implementacao:
  - testes de seeds/commands para `seed_initial` e `seed_demo`
  - teste do endpoint `organizations/plans/` se necessario
  - teste de criacao de `Organization` com default alinhado

## 11. Riscos

- [PRECISA_VALIDAR] Dados existentes com `starter` podem ficar semanticamente invalidos sem data migration.
- [CONFIRMADO_NO_CODIGO] Seeds atuais continuariam reintroduzindo `starter` se a migration fosse criada sem corrigir os comandos.
- [INFERIDO_DO_CODIGO] Se o mapeamento funcional de `starter` nao for validado, uma data migration pode aplicar conversao errada.
- [INFERIDO_DO_CODIGO] Como `Organization.plan` e usado para limites de uso, uma conversao inadequada pode alterar permissao de casos, documentos, usuarios e pedidos de IA.

## 12. Rollback plan

1. Nao aplicar nenhuma migration ate aprovar o mapeamento funcional.
2. Se a migration vier a ser criada e causar problema:
  - reverter a migration de `organizations`
  - restaurar backup do banco em ambiente persistente, se necessario
  - reverter ajustes de seed que dependam do novo plano

## 13. Criterios de aceitacao

- [CONFIRMADO_NO_CODIGO] O motivo do drift fica documentado.
- [INFERIDO_DO_CODIGO] A equipa aprova o destino funcional de `starter`.
- [INFERIDO_DO_CODIGO] Seeds e setup deixam de produzir valor invalido para `Organization.plan`.
- [INFERIDO_DO_CODIGO] A migration futura altera apenas `Organization.plan`.
- [INFERIDO_DO_CODIGO] Se houver dados antigos, a estrategia de migracao de dados fica definida antes da aplicacao.

## 14. Perguntas para validacao humana

1. [PRECISA_VALIDAR] `starter` deve ser convertido para `free`, `solo` ou outro plano?
2. [PRECISA_VALIDAR] Existem organizacoes reais persistidas com `plan='starter'`?
3. [PRECISA_VALIDAR] A equipa quer tratar isso com:
   - migration de schema + data migration
   - ou primeiro alinhamento de seeds e depois migration
4. [PRECISA_VALIDAR] O endpoint de planos e os limites atuais (`free/solo/growth/enterprise`) representam a regra oficial de negocio?

## 15. Estado apos alinhamento dos seeds

- [CONFIRMADO_NO_CODIGO] `seed_initial.py` e `seed_demo.py` ja nao reintroduzem `starter`.
- [CONFIRMADO_NO_CODIGO] O bootstrap via `setup_local` deixa de reintroduzir `starter` de forma indireta porque continua chamando `seed_demo`, agora alinhado para `free`.
- [CONFIRMADO_NO_CODIGO] O uso residual de `starter` em `ai_assistant/services/ai_service.py` tambem foi removido.
- [CONFIRMADO_NO_CODIGO] O drift de schema/migration de `organizations.plan` foi tratado em [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py).

## 16. Estado apos implementacao da migration

- [CONFIRMADO_NO_CODIGO] Foi criada [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py).
- [CONFIRMADO_NO_CODIGO] A migration inclui:
  - `RunPython` para converter `starter -> free`
  - `AlterField` para alinhar `Organization.plan` com `free`, `solo`, `growth`, `enterprise`
- [CONFIRMADO_NO_CODIGO] Nenhuma mudanca foi feita em `billing`.
- [CONFIRMADO_NO_CODIGO] A suite completa permaneceu verde apos a aplicacao.
