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

## Mudanca

- ID: `IMP-KB-RAG-002`
- Titulo: Improved Knowledge Base retrieval with indexing observability, safer ranking, stats and embedding foundation.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] O `knowledge_base` passou a registrar `IndexingJob` para observabilidade de indexacao e reindexacao por tenant.
- [CONFIRMADO_NO_CODIGO] A busca textual ganhou ranking mais robusto com frase exata, frequencia de termos, ocorrencias no titulo e desempate por recencia.
- [CONFIRMADO_NO_CODIGO] O endpoint `ask` agora retorna `retrieval_method`, `sources_count`, `confidence` e `sources` ordenadas por score.
- [CONFIRMADO_NO_CODIGO] Foi adicionado `GET /api/v1/knowledge-base/{id}/stats/` com contagens e datas agregadas por base e por tenant.
- [CONFIRMADO_NO_CODIGO] Foi adicionado `POST /api/v1/knowledge-base/{id}/reindex-document/` com reposicao segura de chunks e registro de `chunks_deleted` e `chunks_created`.
- [CONFIRMADO_NO_CODIGO] Foi criada a fundacao `ChunkEmbedding` para embeddings opcionais futuros, sem chamar provider externo nesta fase.
- [CONFIRMADO_NO_CODIGO] A suite [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py) foi expandida para cobrir jobs, ranking, `stats`, reindexacao, embeddings foundation e os novos campos de `ask`.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-knowledge-base-rag-phase-2.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-knowledge-base-rag-phase-2.md).

## Mudanca

- ID: `IMP-KB-RAG-003`
- Titulo: Added RAG governance settings, embedding opt-in controls and audit logs without enabling external providers.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi adicionado `RAGSettings` por `organization` com defaults seguros, `retrieval_mode`, opt-in explicito para embeddings externos, `max_sources_per_answer` e limiar minimo de confianca.
- [CONFIRMADO_NO_CODIGO] Foi adicionado `EmbeddingAuditLog` para registrar tentativas de embeddings sem expor conteudo bruto do documento.
- [CONFIRMADO_NO_CODIGO] Foram adicionados `GET/PATCH /api/v1/knowledge-base/settings/`, `GET /api/v1/knowledge-base/embedding-audit-logs/` e `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`.
- [CONFIRMADO_NO_CODIGO] `prepare-embeddings` nao chama provider externo nesta fase e retorna `skipped` seguro com motivo auditavel.
- [CONFIRMADO_NO_CODIGO] O endpoint `ask` passou a retornar `effective_retrieval_mode`, `fallback_used` e `fallback_reason`, mantendo `retrieval_method=\"textual\"` enquanto embeddings nao estao efetivos.
- [CONFIRMADO_NO_CODIGO] A suite [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py) foi expandida para cobrir settings, opt-in, audit logs, fallback textual e limite de fontes.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta camada foi registado em [docs/10-checkpoints/2026-04-rag-governance.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-rag-governance.md).

## Mudanca

- ID: `IMP-KB-RAG-004`
- Titulo: Added optional local embedding pipeline and hybrid retrieval foundation.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criado [knowledge_base/embedding_providers.py](/c:/projectos/JurisAI/knowledge_base/embedding_providers.py) com `LocalHashEmbeddingProvider`, deterministico e totalmente local, e `ExternalEmbeddingProviderPlaceholder`, que continua sem chamadas reais para providers externos.
- [CONFIRMADO_NO_CODIGO] `prepare-embeddings` agora gera `ChunkEmbedding` local com `provider=\"local\"` e `model=\"local-hash-v1\"`, sem duplicar embeddings existentes do mesmo chunk.
- [CONFIRMADO_NO_CODIGO] O `knowledge_base` agora suporta retrieval `local_embedding` e `hybrid`, combinando score textual e score de similaridade local sem remover o pipeline textual existente.
- [CONFIRMADO_NO_CODIGO] O endpoint `ask` passou a devolver `final_score`, `text_score` e `embedding_score` nas fontes quando aplicavel, mantendo `sources` obrigatorias e fallback textual seguro.
- [CONFIRMADO_NO_CODIGO] Providers externos continuam sem implementacao real nesta fase e `prepare-embeddings` registra `EmbeddingAuditLog` com `skipped` e `provider_not_implemented` quando configurados.
- [CONFIRMADO_NO_CODIGO] A suite [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py) foi expandida para cobrir provider local, retrieval hibrido, fallback textual, nao duplicacao e auditabilidade do placeholder externo.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-local-embeddings-hybrid-retrieval.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-local-embeddings-hybrid-retrieval.md).

## Mudanca

- ID: `IMP-OCR-001`
- Titulo: Added OCR and document text extraction foundation for TXT, textual PDF and DOCX without external providers.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] O app `ocr` deixou de ser apenas placeholder e passou a suportar `OCRJob` e `OCRResult` funcionais por `organization`.
- [CONFIRMADO_NO_CODIGO] Foram adicionados extratores locais para `TXT`, `PDF` com camada textual e `DOCX`, sem qualquer chamada a provider externo.
- [CONFIRMADO_NO_CODIGO] Foram adicionados `POST /api/v1/ocr/documents/{document_id}/run/`, `GET /api/v1/ocr/jobs/`, `GET /api/v1/ocr/results/` e `POST /api/v1/ocr/results/{id}/apply-to-document/`.
- [CONFIRMADO_NO_CODIGO] `Document.content` so e atualizado quando `update_document_content=true` ou quando um resultado armazenado e aplicado explicitamente.
- [CONFIRMADO_NO_CODIGO] Formatos nao suportados e falhas de extracao geram `OCRJob` com `status=failed`, sem apagar o documento original.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py) cobrindo formatos suportados, falha controlada, `apply-to-document` e isolamento multi-tenant.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-ocr-document-text-extraction.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-ocr-document-text-extraction.md).

## Mudanca

- ID: `IMP-OCR-002`
- Titulo: Added controlled OCR-to-KnowledgeBase pipeline with tenant isolation and explicit document content update.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi adicionado o modelo `OCRKnowledgeBasePipelineRun` para rastrear o fluxo `OCR -> apply-to-document -> index-document`.
- [CONFIRMADO_NO_CODIGO] Foi adicionado `POST /api/v1/ocr/pipelines/knowledge-base/` com validacao explicita de `document`, `knowledge_base` e `update_document_content=true`.
- [CONFIRMADO_NO_CODIGO] Foram adicionados `GET /api/v1/ocr/pipelines/` e `GET /api/v1/ocr/pipelines/{id}/`, sempre filtrados por `organization`.
- [CONFIRMADO_NO_CODIGO] O pipeline executa OCR local, aplica `Document.content` apenas com confirmacao explicita e depois reutiliza a indexacao existente do `knowledge_base`.
- [CONFIRMADO_NO_CODIGO] Se o OCR falhar, o pipeline para antes da indexacao; se a indexacao falhar, `OCRResult` e `Document.content` ja aplicados sao preservados.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py) cobrindo sucesso, bloqueio cross-tenant, `update_document_content=false`, falha controlada e `ask` com `sources` apos o pipeline.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-ocr-to-knowledge-base-pipeline.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-ocr-to-knowledge-base-pipeline.md).

## Mudanca

- ID: `IMP-OCR-003`
- Titulo: Added advanced OCR governance settings and audit logs without enabling external OCR providers.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foram adicionados `OCRSettings` e `OCRAuditLog` por `organization`, com defaults seguros e sem envio de documentos para fora do sistema.
- [CONFIRMADO_NO_CODIGO] Foram adicionados `GET/PATCH /api/v1/ocr/settings/`, `GET /api/v1/ocr/audit-logs/` e `POST /api/v1/ocr/documents/{document_id}/advanced-run/`.
- [CONFIRMADO_NO_CODIGO] OCR externo continua desativado por defeito; mesmo quando configurado, `advanced-run` retorna `skipped`/`not_implemented` sem chamar provider real.
- [CONFIRMADO_NO_CODIGO] Toda tentativa de OCR avancado gera `OCRAuditLog` sem armazenar conteudo bruto do documento.
- [CONFIRMADO_NO_CODIGO] O OCR local existente para `TXT`, `PDF` textual e `DOCX` foi preservado, assim como o pipeline `OCR -> KnowledgeBase`.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py) cobrindo defaults, opt-in, `advanced-run`, logs, cross-tenant e regressao do pipeline existente.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-advanced-ocr-governance.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-advanced-ocr-governance.md).

## Mudanca

- ID: `IMP-OCR-004`
- Titulo: Added local image OCR engine foundation with governed Tesseract adapter and safe fallback.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criado [ocr/local_engines.py](/c:/projectos/JurisAI/ocr/local_engines.py) com `TesseractOCREngine`, detecao segura de dependencias opcionais e fallback controlado quando a engine local nao esta disponivel.
- [CONFIRMADO_NO_CODIGO] `OCRSettings` passou a aceitar `image_ocr_mode=\"local\"` e `scanned_pdf_ocr_mode=\"local\"`, preservando defaults seguros e sem ativar OCR externo.
- [CONFIRMADO_NO_CODIGO] `advanced-run` agora tenta OCR local para imagens `PNG`, `JPG` e `JPEG` quando o tenant habilita local OCR e o provider preferido e `tesseract` ou `local`.
- [CONFIRMADO_NO_CODIGO] Quando o binario do Tesseract ou as bindings opcionais nao estao disponiveis, o backend retorna falha controlada com `OCRJob` e `OCRAuditLog`, sem quebrar OCR textual existente nem o pipeline `OCR -> KnowledgeBase`.
- [CONFIRMADO_NO_CODIGO] OCR de PDF escaneado continua como placeholder governado nesta fase e responde com motivo auditavel em vez de chamar provider externo.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_local_image_ocr.py](/c:/projectos/JurisAI/tests/test_local_image_ocr.py) para validar OCR local mockado, indisponibilidade da engine, tenant isolation e placeholder seguro para PDF escaneado.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-local-image-ocr-engine.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-local-image-ocr-engine.md).

## Mudanca

- ID: `IMP-OCR-005`
- Titulo: Added local scanned PDF OCR foundation with safe rasterization fallback and audit logs.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] `ocr/local_engines.py` passou a suportar rasterizacao opcional de PDF escaneado via `pdf2image`, com erros controlados para indisponibilidade de `pdf2image` ou Poppler.
- [CONFIRMADO_NO_CODIGO] `run_local_scanned_pdf_ocr()` agora tenta OCR local por pagina com a engine governada de Tesseract, concatena o texto extraido e cria `OCRResult` quando ha conteudo util.
- [CONFIRMADO_NO_CODIGO] Quando rasterizacao local nao esta disponivel, o backend retorna `pdf_rasterization_unavailable`; quando Tesseract nao esta disponivel, retorna `local_ocr_engine_unavailable`, sempre com `OCRJob` e `OCRAuditLog`.
- [CONFIRMADO_NO_CODIGO] Nenhum provider externo e chamado nesta fase; OCR textual de `PDF`, OCR de imagem e o pipeline `OCR -> KnowledgeBase` permaneceram preservados.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_local_scanned_pdf_ocr.py](/c:/projectos/JurisAI/tests/test_local_scanned_pdf_ocr.py) para validar fluxo mockado, indisponibilidade de rasterizacao, indisponibilidade de Tesseract, tenant isolation e regressao dos fluxos existentes.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-local-scanned-pdf-ocr.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-local-scanned-pdf-ocr.md).

## Mudanca

- ID: `IMP-OCR-006`
- Titulo: Integrated local scanned PDF OCR with the OCR-to-KnowledgeBase pipeline using explicit tenant settings and safe fallback.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] `run_ocr_to_knowledge_base_pipeline()` agora tenta OCR textual primeiro e so cai para OCR local de PDF escaneado quando o documento e PDF, a extracao padrao nao produz texto util e `scanned_pdf_ocr_mode=\"local\"` esta habilitado.
- [CONFIRMADO_NO_CODIGO] O fallback avancado preserva `update_document_content=true` como requisito obrigatorio, mantendo a indexacao bloqueada quando OCR avancado falha.
- [CONFIRMADO_NO_CODIGO] O pipeline agora expoe `used_advanced_ocr`, `advanced_ocr_reason` e `ocr_audit_log` derivados de `metadata`, sem quebrar os campos anteriores do endpoint.
- [CONFIRMADO_NO_CODIGO] `OCRJob`, `OCRResult` e `OCRAuditLog` do caminho avancado permanecem associados ao `pipeline_run` por referencias diretas e/ou `metadata`, com tenant isolation preservado.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py) para cobrir PDF textual, fallback mockado para PDF escaneado, falhas de configuracao, falhas sem Poppler/Tesseract e `ask` com `sources` apos indexacao.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-scanned-pdf-ocr-to-knowledge-base-pipeline.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-scanned-pdf-ocr-to-knowledge-base-pipeline.md).

## Mudanca

- ID: `IMP-OCR-007`
- Titulo: Added OCR page-level observability and tenant-configurable OCR limits.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] `OCRSettings` passou a suportar `max_scanned_pdf_pages`, `max_ocr_file_size_mb`, `max_ocr_chars_output` e `store_page_level_ocr` por `organization`.
- [CONFIRMADO_NO_CODIGO] Foi adicionado o modelo `OCRPageResult` para observabilidade por pagina em OCR de PDF escaneado, sempre filtrado por tenant.
- [CONFIRMADO_NO_CODIGO] `run_local_scanned_pdf_ocr()` agora aplica limite de paginas, limite de tamanho de ficheiro, truncamento seguro de output e metadata como `pages_processed`, `pages_failed`, `total_pages_detected`, `pages_limit_applied` e `output_truncated`.
- [CONFIRMADO_NO_CODIGO] Foram adicionados `GET /api/v1/ocr/page-results/` e `GET /api/v1/ocr/results/{id}/pages/`, sempre isolados por `organization`.
- [CONFIRMADO_NO_CODIGO] Ficheiros acima do limite falham com `ocr_file_size_limit_exceeded` e geram `OCRAuditLog`, sem enviar documentos para provider externo nem apagar artefatos anteriores.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py) cobrindo limites, truncamento, `OCRPageResult`, isolamento por tenant e regressao do pipeline com metadata de paginas.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-ocr-observability-tenant-limits.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-ocr-observability-tenant-limits.md).

## v0.3.0 — Tenant-Isolated Legal RAG Foundation

Resumo:

- Added functional tenant-isolated textual RAG
- Added sources, confidence and retrieval metadata
- Added indexing observability
- Added stats and reindexing
- Added RAGSettings and EmbeddingAuditLog
- Added explicit governance for future external embeddings
- No external provider enabled by default
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.3.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.3.0.md)

## v0.4.0 — Local Embeddings and Hybrid Retrieval

- Added `LocalHashEmbeddingProvider`
- Added local `ChunkEmbedding` generation
- Added `local_embedding` retrieval method
- Added `hybrid` retrieval method
- Added `textual_fallback` retrieval method
- Added `final_score`, `text_score` and `embedding_score` in sources
- Preserved mandatory sources and textual fallback
- Kept external providers disabled/not implemented
- Full suite: `129 passed`
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.4.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.4.0.md)

## v0.5.0 - OCR and Document Text Extraction Foundation

- Added `OCRJob` and `OCRResult`.
- Added local TXT extraction.
- Added textual PDF extraction.
- Added DOCX extraction.
- Added explicit `apply-to-document` flow.
- Added tenant-isolated OCR jobs and results.
- Preserved original document files.
- Added controlled failure handling for unsupported formats.
- No external OCR provider enabled.
- Full suite: `140 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.5.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.5.0.md)

## v0.6.0 - OCR to Knowledge Base Pipeline

- Added `OCRKnowledgeBasePipelineRun`.
- Added controlled OCR -> Document.content -> KnowledgeBase pipeline.
- Added pipeline endpoint for tenant-isolated document ingestion.
- Required explicit `update_document_content=true` for pipeline execution.
- Linked pipeline runs to `OCRJob`, `OCRResult`, `KnowledgeDocument` and `IndexingJob`.
- Added ask-with-sources validation after pipeline completion.
- Preserved existing OCR and KnowledgeBase endpoints.
- No external OCR provider enabled.
- Full suite: `148 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.6.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.6.0.md)

## v0.7.0 - Advanced OCR Governance

- Added `OCRSettings`.
- Added `OCRAuditLog`.
- Added tenant-specific OCR settings.
- Added explicit opt-in controls for external OCR.
- Added governed `advanced-run` endpoint.
- Preserved existing local OCR for TXT, textual PDF and DOCX.
- Preserved OCR-to-KnowledgeBase pipeline.
- Kept all external OCR providers disabled.
- Added audit logs for advanced OCR attempts.
- Full suite: `159 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.7.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.7.0.md)

## v0.8.0 - Local Image OCR Engine

- Added local image OCR foundation.
- Added optional Tesseract adapter.
- Added governed OCR for PNG, JPG and JPEG.
- Added safe fallback when Tesseract is unavailable.
- Added OCRJob and OCRAuditLog tracking for local image OCR attempts.
- Preserved TXT, textual PDF and DOCX extraction.
- Preserved OCR-to-KnowledgeBase pipeline.
- Kept external OCR providers disabled.
- Full suite: `165 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.8.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.8.0.md)

## v0.9.0 - Local Scanned PDF OCR Foundation

- Added local scanned PDF OCR foundation.
- Added `PDFRasterizationUnavailable`.
- Added `ScannedPDFOCRUnavailable`.
- Added scanned PDF OCR support through local `pdf2image` rasterization when available.
- Added governed per-page OCR with local Tesseract adapter.
- Added safe fallback when Poppler/pdf2image is unavailable.
- Added safe fallback when Tesseract is unavailable.
- Preserved textual PDF extraction.
- Preserved local image OCR.
- Preserved OCR-to-KnowledgeBase pipeline.
- Kept all external OCR providers disabled.
- Full suite: `174 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.9.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.9.0.md)

## v0.10.0 - Scanned PDF OCR to Knowledge Base Pipeline

- Integrated local scanned PDF OCR with the OCR-to-KnowledgeBase pipeline.
- Added fallback from textual PDF extraction to governed scanned PDF OCR.
- Added has_useful_extracted_text(...).
- Updated run_ocr_to_knowledge_base_pipeline(...).
- Added used_advanced_ocr, advanced_ocr_reason and ocr_audit_log in pipeline payloads.
- Preserved explicit update_document_content=true requirement.
- Preserved OCRJob, OCRResult, OCRAuditLog and pipeline metadata on failures.
- Preserved tenant isolation.
- Kept all external OCR providers disabled.
- Full suite: `180 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.10.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.10.0.md)

## v0.11.0 - OCR Observability and Tenant Limits

- Added `OCRPageResult`.
- Added tenant-configurable OCR limits through `max_scanned_pdf_pages`, `max_ocr_file_size_mb`, `max_ocr_chars_output` and `store_page_level_ocr`.
- Added `GET /api/v1/ocr/page-results/`, `GET /api/v1/ocr/page-results/{id}/` and `GET /api/v1/ocr/results/{id}/pages/`.
- Added page-level OCR observability for scanned PDF processing.
- Added output truncation metadata and page limit metadata.
- Preserved OCR textual extraction, image OCR, scanned PDF OCR and the OCR-to-KnowledgeBase pipeline.
- Kept all external OCR providers disabled.
- Full suite: `190 passed`.
- Release checkpoint: [docs/10-checkpoints/2026-04-release-v0.11.0.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-release-v0.11.0.md)

## Mudanca

- ID: `IMP-STAB-001`
- Titulo: Added CI workflow, healthcheck endpoint and backend stabilization checks.
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] Foi criado o workflow [ .github/workflows/ci.yml ](/c:/projectos/JurisAI/.github/workflows/ci.yml) para `push` e `pull_request` em `main`, usando SQLite e executando `manage.py check`, `makemigrations --check --dry-run` e `pytest`.
- [CONFIRMADO_NO_CODIGO] Foi adicionado o endpoint publico `GET /health/`, preservando tambem `GET /api/v1/health/` para compatibilidade.
- [CONFIRMADO_NO_CODIGO] O healthcheck retorna apenas `status`, `service` e `version`, sem consultar dados sensiveis nem expor segredos.
- [CONFIRMADO_NO_CODIGO] Foi criada a suite [tests/test_healthcheck.py](/c:/projectos/JurisAI/tests/test_healthcheck.py) cobrindo disponibilidade publica do healthcheck e compatibilidade com a rota legada.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-backend-stabilization-ci-healthcheck.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-backend-stabilization-ci-healthcheck.md).

## Mudanca

- ID: `IMP-STAB-002`
- Titulo: Added deployment hardening for Docker, Redis, Flower, pinned dependencies, healthchecks and OCR native binaries.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] O `Dockerfile` deixou de executar `collectstatic` no build e passou a usar `entrypoint.sh` com `RUN_COLLECTSTATIC=True` apenas em runtime.
- [CONFIRMADO_NO_CODIGO] O container agora instala `tesseract-ocr` e `poppler-utils`, alinhando o runtime Docker com os caminhos locais de OCR.
- [CONFIRMADO_NO_CODIGO] `docker-compose.yml` passou a exigir password no Redis, autenticacao basica no Flower e healthchecks para `web`, `db`, `redis`, `worker` e `flower`.
- [CONFIRMADO_NO_CODIGO] `requirements.txt` passou a usar versoes pinadas com `==`.
- [CONFIRMADO_NO_CODIGO] `pytest.ini` deixou de ativar `--reuse-db` por defeito.
- [CONFIRMADO_NO_CODIGO] O ficheiro `JURISAI_MASTER_PROMPT (1).md` foi renomeado para [docs/00-project/JURISAI_MASTER_PROMPT.md](/c:/projectos/JurisAI/docs/00-project/JURISAI_MASTER_PROMPT.md).
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-deployment-security-hardening.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-deployment-security-hardening.md).

## Mudanca

- ID: `IMP-STAB-003`
- Titulo: Validated Docker runtime build, healthchecks and container smoke tests.
- Risco: baixo
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] `docker compose build` passou com a stack endurecida e a imagem unica `jurisai-app:latest` passou a ser reutilizada por `web`, `worker` e `flower`, evitando colisao de exportacao do buildx no Windows.
- [CONFIRMADO_NO_CODIGO] Foi adicionada a dependencia pinada `flower==2.0.1` para garantir que o comando `celery flower` existe no runtime do container.
- [CONFIRMADO_NO_CODIGO] `docker compose up -d` subiu `web`, `db`, `redis`, `worker` e `flower`, com `GET /health/` retornando `200`.
- [CONFIRMADO_NO_CODIGO] `docker compose exec web python manage.py check`, `makemigrations --check --dry-run`, `python -m pytest tests/test_healthcheck.py` e `python -m pytest` passaram dentro do container.
- [CONFIRMADO_NO_CODIGO] O Redis respondeu `PONG` com password e o Flower permaneceu sem exposicao publica por porta direta.
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-docker-runtime-validation.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-docker-runtime-validation.md).

## Mudanca

- ID: `IMP-STAB-004`
- Titulo: Added final runtime hardening with non-root containers, private Redis networking and production readiness checklist.
- Risco: medio
- Estado: implementada e validada tecnicamente

- [CONFIRMADO_NO_CODIGO] O `Dockerfile` passou a criar `appuser/appgroup`, preparar diretórios de runtime e executar `web`, `worker` e `flower` como utilizador nao-root.
- [CONFIRMADO_NO_CODIGO] O Redis deixou de expor porta publica no host e ficou restrito a networking interno do Compose, mantendo password obrigatoria.
- [CONFIRMADO_NO_CODIGO] Foi criada a checklist de producao em [docs/11-production/production-readiness-checklist.md](/c:/projectos/JurisAI/docs/11-production/production-readiness-checklist.md).
- [CONFIRMADO_NO_CODIGO] O checkpoint tecnico desta fase foi registado em [docs/10-checkpoints/2026-04-runtime-hardening-production-checklist.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-04-runtime-hardening-production-checklist.md).

## v1.0.0-rc.1 - Backend MVP Stabilization

- Consolidated backend MVP release candidate.
- Validated CI, healthcheck and Docker runtime.
- Consolidated SaaS legal services, Knowledge Base/RAG, OCR and document pipelines.
- Added deployment hardening and runtime hardening.
- Added production readiness checklist.
- Preserved tenant isolation.
- Preserved external providers disabled by default.
- Local and container test suites passed.

## v1.0.0-rc.2 - Staging Deployment Validation

- Added staging Docker Compose template.
- Added staging environment template.
- Added staging deployment guide.
- Added reverse proxy and TLS documentation.
- Added backup and restore documentation.
- Added monitoring and observability documentation.
- Added rollback checklist.
- Added staging smoke test scripts.
- Preserved secrets outside the repository.
- Preserved Redis, database and Flower as private services.
- Local validation passed.

## v1.0.0-rc.3 - Real Staging Runtime Validation

- Validated real staging runtime with Docker build/up, healthcheck, smoke tests, network privacy and backup procedure.

## v1.0.0-rc.4 - HTTPS and Monitoring Validation

- Added/validated staging reverse proxy and TLS documentation.
- Added HTTPS smoke validation.
- Added staging monitoring validation documentation.
- Added backup scheduling documentation.
- Preserved private Redis/PostgreSQL/Flower networking.
- Preserved environment-managed secrets.

## v1.0.0-rc.5 - Render Public Staging Validation

- Validated initial public Render staging URL.
- Confirmed public HTTPS `/health/` endpoint.
- Confirmed Django Admin login page is reachable.
- Documented Render Free limitations for Shell and background worker.
- Documented pending superuser bootstrap, credential rotation, monitoring and backups.

## Render operational security follow-up

- Added opt-in superuser bootstrap for Render deployments without Shell access.
- Added environment examples for one-time admin bootstrap.
- Added bootstrap coverage tests and Render follow-up checkpoint documentation.
- Prioritized `DATABASE_URL` for managed deployments such as Render.
- Added `RUN_MIGRATIONS` startup flag for restricted hosting environments.
- Added WhiteNoise support for Django static files on Render.
- Added commercial readiness gap analysis.
- Added billing readiness audit.
- Added AI readiness audit.
- Added Render staging hardening notes.
- Started frontend MVP environment setup on separate branch.
- Added Next.js frontend scaffold.
- Installed frontend skills stack.
- Added JurisAI frontend architecture foundation.

## Frontend MVP initial build

- Added initial JurisAI SaaS layout with sidebar, topbar, theming and brand logo.
- Added JWT auth bootstrap, organization switching and tenant cache isolation.
- Added Axios API client integration with refresh-token foundation.
- Added dashboard, cases, clients, documents, OCR, Knowledge Base, deadlines, calendar, finance, billing, settings and client portal pages.
- Added DRF form error mapping across login, client and case flows.
- Added honest billing UI without pretending checkout is already active.

## Frontend auth routing and staging integration hardening

- Hardened frontend auth routing.
- Added protected route foundation.
- Added staging API environment documentation.
- Improved tenant cache invalidation flow.
- Improved dashboard staging awareness.

## Frontend cases, clients and documents flows

- Integrated initial clients, cases and documents frontend flows.
- Added document upload foundation.
- Added document-to-OCR frontend actions.
- Improved multi-tenant states across legal data pages.
