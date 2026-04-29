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
