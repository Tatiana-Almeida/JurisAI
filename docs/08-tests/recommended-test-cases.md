# Recommended Test Cases

## CT-001 Bloquear criacao de caso com `client_id` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e correcao aplicada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-002 Bloquear criacao de prazo com `law_case_id` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e correcao aplicada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-003 Bloquear criacao de documento com `law_case_id` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e correcao aplicada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-004 Rejeitar webhook sem assinatura

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-005 Garantir que `AuditLog` nao vaza dados entre organizacoes

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e correcao aplicada
- Cobertura preparada: [tests/test_audit_log_tenant_regressions.py](/c:/projectos/JurisAI/tests/test_audit_log_tenant_regressions.py)

## CT-006 Verificar limites por plano para usuarios, casos e documentos

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO]

## CT-007 Verificar quota mensal de IA

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO]

## CT-008 Verificar `complete` em prazos

- Risco: baixo
- Estado: [CONFIRMADO_NO_CODIGO]

## CT-009 Verificar versionamento concorrente de documentos

- Risco: medio
- Estado: [INFERIDO_DO_CODIGO]

## CT-010 Verificar tasks de notificacao e lembretes

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO]

## CT-011 Bloquear criacao de caso com `lawyer_id` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e correcao aplicada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-012 Permitir criacao de prazo com `law_case_id` da mesma organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-013 Permitir criacao de documento com `law_case_id` da mesma organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-014 Bloquear update de prazo para `law_case_id` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-015 Bloquear update de documento para `law_case_id` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_tenant_validation_regressions.py](/c:/projectos/JurisAI/tests/test_tenant_validation_regressions.py)

## CT-016 Bloquear detalhe de `AuditLog` de outra organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e correcao aplicada
- Cobertura preparada: [tests/test_audit_log_tenant_regressions.py](/c:/projectos/JurisAI/tests/test_audit_log_tenant_regressions.py)

## CT-017 Confirmar bloqueio de nao-admin no endpoint de auditoria

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_audit_log_tenant_regressions.py](/c:/projectos/JurisAI/tests/test_audit_log_tenant_regressions.py)

## CT-018 Garantir que logs sem `organization` nao aparecem para admins de tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_audit_log_tenant_regressions.py](/c:/projectos/JurisAI/tests/test_audit_log_tenant_regressions.py)

## CT-019 Rejeitar webhook com assinatura invalida sem criar `Payment`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-020 Garantir que payload invalido nao altera estado financeiro

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-021 Garantir que evento desconhecido nao altera estado financeiro

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-022 Garantir que `event_id` repetido nao reaplica efeitos financeiros

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-023 Rejeitar update de `Subscription` sem assinatura valida

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-024 Rejeitar webhook com timestamp antigo

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_billing_webhook_security.py](/c:/projectos/JurisAI/tests/test_billing_webhook_security.py)

## CT-025 Validar orquestrador do webhook para evento novo

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py)

## CT-026 Validar orquestrador do webhook para evento duplicado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py)

## CT-027 Validar rollback transacional do orquestrador do webhook

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py)

## CT-028 Validar atualizacao de `Subscription` no orquestrador do webhook

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada apos correcao do schema migrado de `billing`
- Cobertura preparada: [tests/test_billing_webhook_services.py](/c:/projectos/JurisAI/tests/test_billing_webhook_services.py)

## CT-029 Permitir upload valido de PDF em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-030 Rejeitar upload de `Document` com extensao invalida

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-031 Rejeitar upload de `Document` acima do limite de tamanho

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-032 Rejeitar upload de `Document` com `content_type` incompatível

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-033 Manter upload de `Document` valido no mesmo tenant

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-034 Bloquear upload de `Document` para `LawCase` de outro tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao preservada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-035 Rejeitar ou sanitizar nome de ficheiro com path traversal em `Document`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e sanitizacao explicita aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-036 Sanitizar nome de ficheiro com espacos e caracteres especiais em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e sanitizacao explicita aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-037 Truncar basename excessivamente longo preservando extensao em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e sanitizacao explicita aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-038 Sanitizar basename com multiplos pontos em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e sanitizacao explicita aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-039 Validar `magic bytes` de PDF em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-040 Validar `magic bytes` de PNG em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-041 Validar `magic bytes` de JPG/JPEG em `Document`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e mitigacao aplicada
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-042 Preservar comportamento atual de `DOC`, `DOCX` e `TXT` enquanto `magic bytes` nao e aplicado

- Risco: baixo
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada e comportamento preservado nesta fase
- Cobertura preparada: [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## CT-043 Garantir isolamento multi-tenant em `Task`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_tasks.py](/c:/projectos/JurisAI/tests/test_tasks.py)

## CT-044 Garantir comentarios e checklist isolados por tenant em `Task`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_tasks.py](/c:/projectos/JurisAI/tests/test_tasks.py)

## CT-045 Validar agregacoes do `dashboard` sem mistura entre organizacoes

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_dashboard.py](/c:/projectos/JurisAI/tests/test_dashboard.py)

## CT-046 Garantir visibilidade explicita de casos no `client_portal`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_client_portal.py](/c:/projectos/JurisAI/tests/test_client_portal.py)

## CT-047 Garantir partilha explicita de documentos no `client_portal`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_client_portal.py](/c:/projectos/JurisAI/tests/test_client_portal.py)

## CT-048 Garantir isolamento multi-tenant em `calendar_events`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_calendar_events.py](/c:/projectos/JurisAI/tests/test_calendar_events.py)

## CT-049 Validar geracao segura de `legal_templates`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_legal_templates.py](/c:/projectos/JurisAI/tests/test_legal_templates.py)

## CT-050 Validar isolamento multi-tenant em `legal_finance`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_legal_finance.py](/c:/projectos/JurisAI/tests/test_legal_finance.py)

## CT-051 Criar `KnowledgeBase` apenas na organizacao do utilizador

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-052 Indexar documento proprio em `knowledge_base`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-053 Bloquear indexacao de documento de outro tenant em `knowledge_base`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-054 Garantir que busca em `knowledge_base` nao mistura chunks entre tenants

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-055 Garantir `ask` com fontes explicitas em `knowledge_base`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-056 Retornar `no_sources` quando a base nao tem fontes suficientes

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-057 Validar `IndexingJob` em indexacao bem-sucedida

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-058 Validar `IndexingJob` em erro controlado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-059 Validar ranking textual por frase exata e limite de resultados em `knowledge_base`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-060 Validar `stats` sem mistura entre tenants em `knowledge_base`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-061 Validar `reindex-document` com `chunks_deleted` e `chunks_created`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-062 Validar fundacao de embeddings opcionais por tenant

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-063 Validar `ask` com `retrieval_method`, `sources_count` e `confidence`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-064 Validar `RAGSettings` com defaults seguros por organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-065 Validar opt-in explicito para embeddings externos

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-066 Validar `prepare-embeddings` com `skipped` seguro e auditavel

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-067 Validar `EmbeddingAuditLog` filtrado por tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-068 Validar fallback textual obrigatorio em `ask`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-069 Validar `max_sources_per_answer` em `RAGSettings`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-070 Validar placeholders seguros remanescentes de `ocr` e `document_analysis`

- Risco: medio
- Estado: [INFERIDO_DO_CODIGO] cobertura recomendada para futuras fases

## CT-071 Validar configuracao de provider local em `RAGSettings` sem consentimento externo

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-072 Validar `prepare-embeddings` com provider local e evitar duplicacao

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-073 Validar retrieval `local_embedding` e `hybrid` com `final_score`, `text_score` e `embedding_score`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-074 Validar fallback textual quando embeddings locais nao estao preparados

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-075 Validar `prepare-embeddings` externo como `skipped` seguro e auditavel

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)

## CT-076 Validar extracao local de `TXT` em `ocr`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-077 Validar extracao local de `PDF` textual em `ocr`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-078 Validar extracao local de `DOCX` em `ocr`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-079 Validar `update_document_content` explicito em `ocr`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-080 Validar falha controlada para formato `unsupported` em `ocr`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-081 Validar isolamento multi-tenant em `OCRJob` e `OCRResult`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-082 Validar `apply-to-document` com bloqueio cross-tenant em `ocr`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-083 Validar falha de extracao sem apagar `Document.content`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr.py](/c:/projectos/JurisAI/tests/test_ocr.py)

## CT-084 Validar pipeline `OCR -> KnowledgeBase` com sucesso

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-085 Bloquear pipeline com `document` de outro tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-086 Bloquear pipeline com `knowledge_base` de outro tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-087 Rejeitar pipeline com `update_document_content=false`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-088 Validar falha controlada do pipeline quando o OCR falha

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-089 Validar listagem e detalhe do pipeline por tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-090 Validar `ask` com `sources` apos pipeline OCR -> KnowledgeBase

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_ocr_pipeline.py)

## CT-091 Validar `OCRSettings` com defaults seguros por organizacao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-092 Validar opt-in explicito para OCR externo

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-093 Validar `advanced-run` como `skipped` seguro e auditavel

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-094 Validar `OCRAuditLog` filtrado por tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-095 Bloquear `advanced-run` com documento de outro tenant

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-096 Preservar OCR local e pipeline OCR -> KnowledgeBase apos governanca avancada

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-097 Validar OCR local de imagem com engine mockada e `advanced-run`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_image_ocr.py](/c:/projectos/JurisAI/tests/test_local_image_ocr.py)

## CT-098 Validar falha controlada quando engine local de OCR nao esta disponivel

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_image_ocr.py](/c:/projectos/JurisAI/tests/test_local_image_ocr.py)

## CT-099 Validar bloqueio cross-tenant no OCR local de imagem

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_image_ocr.py](/c:/projectos/JurisAI/tests/test_local_image_ocr.py)

## CT-100 Validar placeholder seguro para OCR local de PDF escaneado

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_image_ocr.py](/c:/projectos/JurisAI/tests/test_local_image_ocr.py)

## CT-101 Preservar regressao do OCR textual existente e do pipeline OCR -> KnowledgeBase apos OCR local de imagem

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_governance.py](/c:/projectos/JurisAI/tests/test_ocr_governance.py)

## CT-102 Validar OCR local mockado para PDF escaneado via `advanced-run`

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_scanned_pdf_ocr.py](/c:/projectos/JurisAI/tests/test_local_scanned_pdf_ocr.py)

## CT-103 Validar falha controlada quando rasterizacao local de PDF nao esta disponivel

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_scanned_pdf_ocr.py](/c:/projectos/JurisAI/tests/test_local_scanned_pdf_ocr.py)

## CT-104 Validar falha controlada quando Tesseract nao esta disponivel para PDF escaneado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_scanned_pdf_ocr.py](/c:/projectos/JurisAI/tests/test_local_scanned_pdf_ocr.py)

## CT-105 Validar isolamento multi-tenant no OCR local de PDF escaneado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_scanned_pdf_ocr.py](/c:/projectos/JurisAI/tests/test_local_scanned_pdf_ocr.py)

## CT-106 Preservar regressao do OCR textual de PDF, OCR de imagem e pipeline OCR -> KnowledgeBase apos OCR local de PDF escaneado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_local_scanned_pdf_ocr.py](/c:/projectos/JurisAI/tests/test_local_scanned_pdf_ocr.py)

## CT-107 Validar pipeline com PDF textual mantendo OCR padrao

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py)

## CT-108 Validar pipeline com PDF escaneado mockado usando fallback OCR local governado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py)

## CT-109 Validar pipeline com falha quando `scanned_pdf_ocr_mode` nao esta habilitado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py)

## CT-110 Validar pipeline com falha controlada sem Poppler/pdf2image

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py)

## CT-111 Validar pipeline com falha controlada sem Tesseract

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py)

## CT-112 Validar `ask` com `sources` apos pipeline com PDF escaneado

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_scanned_pdf_ocr_pipeline.py](/c:/projectos/JurisAI/tests/test_scanned_pdf_ocr_pipeline.py)

## CT-113 Validar `OCRPageResult` por pagina em OCR de PDF escaneado

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py)

## CT-114 Validar limites de OCR por tenant em `OCRSettings`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py)

## CT-115 Validar truncamento de output OCR com metadata auditavel

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py)

## CT-116 Validar bloqueio seguro por limite de tamanho de ficheiro OCR

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py)

## CT-117 Validar limite de paginas aplicado em OCR de PDF escaneado

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py)

## CT-118 Validar isolamento multi-tenant em endpoints de `OCRPageResult`

- Risco: alto
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_ocr_observability.py](/c:/projectos/JurisAI/tests/test_ocr_observability.py)

## CT-119 Validar healthcheck publico do backend

- Risco: baixo
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_healthcheck.py](/c:/projectos/JurisAI/tests/test_healthcheck.py)

## CT-120 Validar rota legada de healthcheck sem autenticacao

- Risco: baixo
- Estado: [CONFIRMADO_NO_CODIGO] cobertura implementada
- Cobertura preparada: [tests/test_healthcheck.py](/c:/projectos/JurisAI/tests/test_healthcheck.py)

## CT-121 Validar `manage.py check` e drift de migrations no CI

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura operacional preparada no workflow
- Cobertura preparada: [.github/workflows/ci.yml](/c:/projectos/JurisAI/.github/workflows/ci.yml)

## CT-122 Validar smoke de estabilizacao backend em SQLite

- Risco: medio
- Estado: [CONFIRMADO_NO_CODIGO] cobertura operacional preparada no workflow
- Cobertura preparada: [.github/workflows/ci.yml](/c:/projectos/JurisAI/.github/workflows/ci.yml)
