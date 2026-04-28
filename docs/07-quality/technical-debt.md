# Technical Debt

## Divida observada

- [CONFIRMADO_NO_CODIGO] Repeticao de logica de `organization_id` em varios serializers.
- [CONFIRMADO_NO_CODIGO] Regras de negocio distribuidas entre views, serializers, models e services.
- [CONFIRMADO_NO_CODIGO] Ausencia de camada de service consistente para billing e grande parte dos fluxos.
- [CONFIRMADO_NO_CODIGO] Inconsistencia entre README, models, migrations e seeds em alguns pontos.
- [CONFIRMADO_NO_CODIGO] `django_celery_beat` e referenciado em `INSTALLED_APPS`, mas a dependencia nao estava declarada em `requirements.txt`, o que bloqueia o bootstrap do Django em ambientes locais incompletos.
- [CONFIRMADO_NO_CODIGO] Cobertura de testes muito concentrada em happy path de poucos modulos.
- [CONFIRMADO_NO_CODIGO] `NotificationService.send_whatsapp` usa comportamento mock e cria novos registos em vez de integrar com fornecedor externo.
- [CONFIRMADO_NO_CODIGO] `billing.tasks.process_recurring_charges` usa status `past_due` em `Invoice`, que nao aparece no enum do model.

## Impacto

- [INFERIDO_DO_CODIGO] A manutencao tende a ficar mais arriscada a medida que novos fluxos forem adicionados.
- [INFERIDO_DO_CODIGO] Ha risco de regressao silenciosa em integracoes e fronteiras de seguranca.

## Divida pendente apos a correcao do billing

- [CONFIRMADO_NO_CODIGO] O drift de migrations do app `billing` para `Subscription` e `Invoice` foi corrigido com `billing.0003`.
- [CONFIRMADO_NO_CODIGO] O drift de `organizations.plan` foi tratado em frente propria com `organizations.0002_alter_organization_plan`.
- [CONFIRMADO_NO_CODIGO] Os comandos `seed_initial` e `seed_demo` ja foram alinhados para `free`, e o uso residual de `starter` em [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py) tambem foi removido.
