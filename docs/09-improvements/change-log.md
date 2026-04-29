# Change Log

## Mudanca

- ID: `IMP-006`
- Titulo: Unificacao de validacoes repetidas de `organization_id`
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criado um mixin compartilhado em `jurisai/serializers.py`.
- [CONFIRMADO_NO_CODIGO] O contrato publico da API foi preservado.
- [CONFIRMADO_NO_CODIGO] A suite focal e a suite completa passaram.

## Mudanca

- ID: `IMP-009`
- Titulo: Correcao do fluxo de notificacoes WhatsApp mock
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] O fluxo assincrono deixou de criar duplicidade no caminho WhatsApp mock.
- [CONFIRMADO_NO_CODIGO] O comportamento legado do service foi preservado quando chamado isoladamente.
- [CONFIRMADO_NO_CODIGO] A suite focal e a suite completa passaram.

## Mudanca

- ID: `IMP-001`
- Titulo: Validacao multi-tenant em foreign keys relacionadas
- Risco: alto
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criado um mixin separado para validar coerencia entre `organization_id` e relacoes recebidas por foreign key.
- [CONFIRMADO_NO_CODIGO] `LawCase`, `Deadline` e `Document` passaram a bloquear relacoes cross-tenant.
- [CONFIRMADO_NO_CODIGO] O contrato publico da API foi preservado, exceto pela restricao correta de requests indevidos.
- [CONFIRMADO_NO_CODIGO] A suite focal e a suite completa passaram.

## Mudanca

- ID: `IMP-003`
- Titulo: Auditoria multi-tenant com isolamento por organizacao
- Risco: alto
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi adicionada `organization` a `AuditLog` como FK nullable.
- [CONFIRMADO_NO_CODIGO] Foi criada a migration [audit_logs/migrations/0002_auditlog_organization.py](/c:/projectos/JurisAI/audit_logs/migrations/0002_auditlog_organization.py).
- [CONFIRMADO_NO_CODIGO] `AuditLogViewSet` passou a filtrar por tenant.
- [CONFIRMADO_NO_CODIGO] A suite focal e a suite completa passaram.

## Mudanca

- ID: `IMP-002`
- Titulo: Webhook de billing com assinatura, idempotencia persistente e replay protection basica
- Risco: alto
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] A Fase 1 introduziu `STRIPE_WEBHOOK_SECRET` e validacao de `Stripe-Signature` sobre o payload bruto.
- [CONFIRMADO_NO_CODIGO] A Fase 2 adicionou o modelo `BillingWebhookEvent` para persistir `event_id` processado.
- [CONFIRMADO_NO_CODIGO] Foi criada a migration [billing/migrations/0002_billingwebhookevent.py](/c:/projectos/JurisAI/billing/migrations/0002_billingwebhookevent.py).
- [CONFIRMADO_NO_CODIGO] Eventos duplicados agora retornam `200` sem reaplicar efeitos financeiros.
- [CONFIRMADO_NO_CODIGO] Timestamps antigos ou invalidos agora sao rejeitados antes de qualquer efeito colateral.
- [CONFIRMADO_NO_CODIGO] O bug da colisao da variavel local `status` foi corrigido.
- [CONFIRMADO_NO_CODIGO] O payload publico de sucesso foi preservado para eventos aceitos e duplicados.
- [CONFIRMADO_NO_CODIGO] [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py) passou integralmente.
- [CONFIRMADO_NO_CODIGO] A suite completa do projeto passou apos a mudanca.

## Mudanca

- ID: `IMP-010`
- Titulo: Extracao minima de helpers puros do webhook para `billing/services.py`
- Risco: medio
- Estado: fase 1 implementada e validada tecnicamente; fase 2 passos 1 e 2 implementados e validados tecnicamente; fase 3 implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foram extraidos helpers puros de assinatura, timestamp e parse para [billing/services.py](/c:/projectos/JurisAI/billing/services.py).
- [CONFIRMADO_NO_CODIGO] A primeira parte da Fase 2 extraiu a leitura semantica minima de `event_id`, `event_type` e `data.object` para helpers pequenos no service.
- [CONFIRMADO_NO_CODIGO] A etapa seguinte da Fase 2 extraiu a resolucao de `organization_id` e o lookup de `organization` para helpers pequenos no service.
- [CONFIRMADO_NO_CODIGO] A Fase 3 moveu `transaction.atomic()`, criacao de `BillingWebhookEvent`, deteccao de duplicado e side effects financeiros para um orquestrador interno em [billing/services.py](/c:/projectos/JurisAI/billing/services.py).
- [CONFIRMADO_NO_CODIGO] [billing/views.py](/c:/projectos/JurisAI/billing/views.py) agora coordena assinatura, timestamp, parse, validacao semantica inicial e a resposta HTTP.
- [CONFIRMADO_NO_CODIGO] Endpoint, payloads, status codes, idempotencia e replay protection foram preservados.
- [CONFIRMADO_NO_CODIGO] A suite focal do webhook e a suite completa passaram apos a refatoracao.
- [CONFIRMADO_NO_CODIGO] O warning tecnico de `django.utils.timezone.utc` em [billing/services.py](/c:/projectos/JurisAI/billing/services.py) foi tratado com substituicao por `datetime.timezone.utc`, sem alterar comportamento funcional.
- [CONFIRMADO_NO_CODIGO] Foi adicionada uma suite unitaria dedicada ao orquestrador em [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py), cobrindo processamento novo, duplicado, rollback e eventos sem side effect.
- [CONFIRMADO_NO_CODIGO] Foi criada a migration [billing/migrations/0003_subscription_invoice.py](/c:/projectos/JurisAI/billing/migrations/0003_subscription_invoice.py) para alinhar o schema migrado com `Subscription` e `Invoice`.
- [CONFIRMADO_NO_CODIGO] A migration inesperada de `organizations.plan` foi descartada nesta etapa para isolar a correcao apenas no app `billing`.
- [CONFIRMADO_NO_CODIGO] O `skip` do teste de `Subscription` em [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py) foi removido apos a correcao do schema.
- [CONFIRMADO_NO_CODIGO] As suites de service, webhook e completa passaram apos a correcao do drift de migrations do `billing`.

## Mudanca

- ID: `IMP-ORG-SEEDS-001`
- Titulo: Alinhamento dos seeds de `Organization.plan` ao enum atual
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] [accounts/management/commands/seed_initial.py](/c:/projectos/JurisAI/accounts/management/commands/seed_initial.py) deixou de usar `default='starter'` e passou a usar `default='free'`.
- [CONFIRMADO_NO_CODIGO] [accounts/management/commands/seed_demo.py](/c:/projectos/JurisAI/accounts/management/commands/seed_demo.py) deixou de criar organizacao demo com `plan='starter'` e passou a usar `plan='free'`.
- [CONFIRMADO_NO_CODIGO] Foi adicionada a suite [tests/test_organization_plan_seeds.py](/c:/projectos/JurisAI/tests/test_organization_plan_seeds.py) para impedir o retorno de `starter` nesses dois comandos.
- [CONFIRMADO_NO_CODIGO] O fallback residual de `starter` em [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py) foi alinhado para `free/solo/growth/enterprise`.
- [CONFIRMADO_NO_CODIGO] Foi adicionada a suite [tests/test_ai_plan_limits.py](/c:/projectos/JurisAI/tests/test_ai_plan_limits.py) para impedir regressao nesse mapeamento de limites de IA por plano.
- [CONFIRMADO_NO_CODIGO] Nenhuma migration foi criada nesta etapa.

## Mudanca

- ID: `IMP-ORG-MIG-001`
- Titulo: Correcao controlada do drift de `Organization.plan`
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criada a migration [organizations/migrations/0002_alter_organization_plan.py](/c:/projectos/JurisAI/organizations/migrations/0002_alter_organization_plan.py).
- [CONFIRMADO_NO_CODIGO] A migration altera apenas o campo `Organization.plan` para refletir `free/solo/growth/enterprise` com default `free`.
- [CONFIRMADO_NO_CODIGO] Foi incluida uma `RunPython` controlada para converter dados antigos `starter -> free`.
- [CONFIRMADO_NO_CODIGO] Nenhuma alteracao foi feita em `billing`, endpoints ou payloads publicos.
- [CONFIRMADO_NO_CODIGO] A migration foi aplicada localmente com SQLite e a suite completa permaneceu verde.

## Mudanca

- ID: `IMP-ENV-LOCAL-001`
- Titulo: Estabilizacao minima do fluxo local de `manage.py migrate`
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] [.env.example](/c:/projectos/JurisAI/.env.example) passou a documentar `DJANGO_USE_SQLITE=True` como opcao explicita apenas para desenvolvimento local fora do Docker/Compose.
- [CONFIRMADO_NO_CODIGO] [README.md](/c:/projectos/JurisAI/README.md) agora separa claramente:
  - fluxo Docker/Compose com PostgreSQL e host `db`
  - fluxo local leve com SQLite
- [CONFIRMADO_NO_CODIGO] Nenhum fallback automatico para SQLite foi introduzido.

## Mudanca

- ID: `IMP-DOC-UPLOAD-TEST-001`
- Titulo: Cobertura de regressao e seguranca para endurecimento de uploads de documentos
- Risco: medio
- Estado: cobertura preparada antes da implementacao

- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) para expressar o comportamento seguro esperado em uploads de `Document`.
- [CONFIRMADO_NO_CODIGO] A cobertura inclui PDF valido, extensao invalida, tamanho acima do limite assumido de 10 MB, `content_type` incompatível, isolamento por tenant e nome de ficheiro com path traversal.
- [CONFIRMADO_NO_CODIGO] Nenhuma logica de producao, schema ou migration foi alterada nesta etapa.
- [INFERIDO_DO_CODIGO] Parte dos testes e esperada falhar antes do hardening porque o serializer atual nao valida explicitamente extensao, tamanho, MIME ou nome de ficheiro.

## Mudanca

- ID: `IMP-DOC-UPLOAD-001`
- Titulo: Hardening inicial de uploads de documentos no serializer
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py) passou a validar explicitamente extensao, tamanho maximo de 10 MB e compatibilidade entre extensao e `content_type`.
- [CONFIRMADO_NO_CODIGO] A whitelist inicial ficou limitada a `.pdf`, `.doc`, `.docx`, `.txt`, `.jpg`, `.jpeg` e `.png`.
- [CONFIRMADO_NO_CODIGO] Uploads invalidos agora retornam `400` sem alterar endpoint, schema ou payloads de sucesso.
- [CONFIRMADO_NO_CODIGO] O isolamento multi-tenant do upload de `Document` foi preservado.
- [CONFIRMADO_NO_CODIGO] A suite focal [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) e a suite completa passaram apos a correcao.

## Mudanca

- ID: `IMP-DOC-UPLOAD-002`
- Titulo: Sanitizacao explicita de filename em uploads de documentos
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criado o helper `sanitize_upload_filename()` em [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py).
- [CONFIRMADO_NO_CODIGO] `document_upload_path()` passou a usar basename sanitizado, com normalizacao ASCII-safe, substituicao de caracteres inseguros, truncamento do basename e preservacao da extensao.
- [CONFIRMADO_NO_CODIGO] O UUID no prefixo e a estrutura `documents/<organization>/<case>/` foram preservados.
- [CONFIRMADO_NO_CODIGO] Endpoint, schema, storage e payloads de sucesso nao mudaram.
- [CONFIRMADO_NO_CODIGO] [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) passou a cobrir traversal, caracteres especiais, nomes longos e multiplos pontos.
- [CONFIRMADO_NO_CODIGO] A suite focal e a suite completa passaram apos a correcao.

## Mudanca

- ID: `IMP-DOC-UPLOAD-TEST-002`
- Titulo: Cobertura de regressao para validacao leve de `magic bytes` em uploads
- Risco: medio
- Estado: cobertura preparada antes da implementacao

- [CONFIRMADO_NO_CODIGO] [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) passou a incluir cenarios de assinatura binaria para `PDF`, `PNG` e `JPG/JPEG`.
- [CONFIRMADO_NO_CODIGO] A cobertura tambem fixa o comportamento atual de `DOC`, `DOCX` e `TXT` nesta fase, sem exigir validacao binaria para esses formatos.
- [CONFIRMADO_NO_CODIGO] Nenhuma logica de producao, schema ou migration foi alterada nesta etapa.
- [INFERIDO_DO_CODIGO] Parte dos testes e esperada falhar antes da implementacao de `magic bytes`, porque o serializer atual ainda nao inspeciona os bytes iniciais do ficheiro.

## Mudanca

- ID: `IMP-DOC-UPLOAD-003`
- Titulo: Validacao leve de `magic bytes` para PDF e imagens
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py) passou a validar assinatura binaria para `.pdf`, `.png`, `.jpg` e `.jpeg`.
- [CONFIRMADO_NO_CODIGO] A leitura ficou limitada aos bytes iniciais necessarios e o ponteiro do ficheiro e reposicionado com `seek(0)` apos a inspecao.
- [CONFIRMADO_NO_CODIGO] `DOC`, `DOCX` e `TXT` mantiveram o comportamento anterior nesta fase.
- [CONFIRMADO_NO_CODIGO] Endpoint, schema, storage, payloads de sucesso, tenant isolation e validacoes anteriores foram preservados.
- [CONFIRMADO_NO_CODIGO] A suite focal [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) e a suite completa passaram apos a correcao.

## Mudanca

- ID: `IMP-EXPANDED-SERVICES-001`
- Titulo: Added foundation for expanded legal services modules.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foram adicionados os apps `tasks`, `dashboard`, `client_portal`, `calendar_events`, `legal_templates`, `legal_finance`, `crm`, `e_signature`, `business_intelligence`, `compliance`, `marketplace`, `knowledge_base`, `ocr` e `document_analysis` ao projeto.
- [CONFIRMADO_NO_CODIGO] A Fase 1 entregou endpoints funcionais para tarefas, dashboard juridico, portal do cliente, agenda juridica, templates dinamicos e financeiro de honorarios.
- [CONFIRMADO_NO_CODIGO] Os novos modelos internos preservam `organization` e os novos endpoints filtram por tenant autenticado.
- [CONFIRMADO_NO_CODIGO] Foram criadas fundacoes seguras para `knowledge_base`, `ocr` e `document_analysis` com placeholders `501 not implemented`.
- [CONFIRMADO_NO_CODIGO] Foram criadas fundacoes comerciais para `crm`, `e_signature`, `business_intelligence`, `compliance` e `marketplace`.
- [CONFIRMADO_NO_CODIGO] Foram adicionadas as suites [tests/test_tasks.py](/c:/projectos/JurisAI/tests/test_tasks.py), [tests/test_dashboard.py](/c:/projectos/JurisAI/tests/test_dashboard.py), [tests/test_client_portal.py](/c:/projectos/JurisAI/tests/test_client_portal.py), [tests/test_calendar_events.py](/c:/projectos/JurisAI/tests/test_calendar_events.py), [tests/test_legal_templates.py](/c:/projectos/JurisAI/tests/test_legal_templates.py) e [tests/test_legal_finance.py](/c:/projectos/JurisAI/tests/test_legal_finance.py).
- [CONFIRMADO_NO_CODIGO] As migrations iniciais dos novos apps foram geradas e aplicadas localmente em SQLite.
- [CONFIRMADO_NO_CODIGO] O checkpoint documental da fase publicada em `b69d65e` foi registado em [docs/10-checkpoints/2026-04-legal-services-foundation.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-legal-services-foundation.md).
- [CONFIRMADO_NO_CODIGO] A consolidacao da release publicada em `v0.2.0` foi registada em [docs/10-checkpoints/2026-04-release-v0.2.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.2.0.md).

## Mudanca

- ID: `IMP-KB-RAG-001`
- Titulo: Added initial functional Knowledge Base / RAG with tenant-isolated textual retrieval and source citations.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] O app `knowledge_base` deixou de ser apenas placeholder e passou a suportar bases por tenant, documentos indexados, `DocumentChunk` e historico de `RetrievalQuery`.
- [CONFIRMADO_NO_CODIGO] Foram implementados os endpoints `GET/POST /api/v1/knowledge-base/`, `GET/POST /api/v1/knowledge-base/documents/`, `POST /api/v1/knowledge-base/{id}/index-document/`, `POST /api/v1/knowledge-base/{id}/search/`, `POST /api/v1/knowledge-base/{id}/ask/` e `GET /api/v1/knowledge-base/queries/`.
- [CONFIRMADO_NO_CODIGO] A indexacao usa conteudo textual local do `Document`, gera chunks por caracteres, persiste `content_hash` e nao envia documentos para provider externo nesta fase.
- [CONFIRMADO_NO_CODIGO] A busca textual inicial filtra sempre por `organization`, suporta filtro por base de conhecimento e retorna `sources` explicitas sem vazar dados entre tenants.
- [CONFIRMADO_NO_CODIGO] O endpoint `ask` retorna resposta fundamentada apenas com base nos chunks encontrados e devolve `no_sources` quando nao ha base suficiente para responder com seguranca.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py) cobrindo tenant isolation, indexacao, busca e respostas com fontes.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta entrega foi registado em [docs/10-checkpoints/2026-04-knowledge-base-rag-initial.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-knowledge-base-rag-initial.md).
