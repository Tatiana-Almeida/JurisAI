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

## CT-051 Validar placeholders seguros de `knowledge_base`, `ocr` e `document_analysis`

- Risco: medio
- Estado: [INFERIDO_DO_CODIGO] cobertura recomendada para futuras fases
