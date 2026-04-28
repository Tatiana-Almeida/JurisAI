# Security Audit

## Resumo

- [CONFIRMADO_NO_CODIGO] A autenticacao base via JWT esta presente.
- [CONFIRMADO_NO_CODIGO] O backend tenta isolar dados por organizacao.
- [CONFIRMADO_NO_CODIGO] `SEC-002` foi mitigado tecnicamente na `IMP-001`.
- [CONFIRMADO_NO_CODIGO] `SEC-003` foi mitigado tecnicamente na `IMP-003`.
- [CONFIRMADO_NO_CODIGO] `SEC-001` foi mitigado tecnicamente na `IMP-002`, com assinatura obrigatoria, persistencia de `event_id` e protecao basica contra replay.

## Riscos

| ID | Risco | Severidade | Evidencia | Recomendacao | Estado |
|---|---|---|---|---|---|
| SEC-001 | Webhook de billing exigia assinatura, mas antes nao tinha idempotencia nem replay protection; agora mitigado com persistencia de `event_id` e tolerancia de timestamp | alto | `billing.views.StripeWebhookView`, `billing.models.BillingWebhookEvent`, testes de webhook | Monitorar operacao real e avaliar extracao para service dedicado | [CONFIRMADO_NO_CODIGO] mitigado na `IMP-002` |
| SEC-002 | Possivel bypass de isolamento de tenant via IDs relacionados | alto | serializers de `LawCase`, `Deadline`, `Document` recebiam FKs sem validar tenant das relacoes | Validar coerencia entre `organization` e entidades relacionadas | [CONFIRMADO_NO_CODIGO] mitigado na `IMP-001`, pendente validacao humana |
| SEC-003 | Auditoria sem FK de organizacao e endpoint global para admin | alto | `AuditLog` nao tinha `organization`; `AuditLogViewSet` nao filtrava por tenant | Adicionar contexto de tenant e restringir visibilidade | [CONFIRMADO_NO_CODIGO] mitigado na `IMP-003`, pendente validacao humana |
| SEC-004 | Ausencia de rate limiting observavel | medio | nenhum middleware/config de throttling encontrado | Configurar throttling por endpoint critico | [NAO_ENCONTRADO] |
| SEC-005 | Segredo padrao fraco em fallback | medio | `SECRET_KEY` default `replace-me` | Exigir variavel obrigatoria em producao | [CONFIRMADO_NO_CODIGO] |
| SEC-006 | Upload de ficheiros sem validacao explicita de tipo/tamanho | medio | `Document.file` era aceite sem validacao adicional observavel; `DocumentSerializer` agora valida extensao, tamanho maximo de 10 MB, compatibilidade basica de `content_type` e assinatura binaria leve para `PDF`, `PNG` e `JPG/JPEG`; `document_upload_path` sanitiza explicitamente o `filename` | Monitorar necessidade de expandir assinatura binaria para formatos adicionais como `DOC`/`DOCX` ou parse mais forte em fase posterior | [CONFIRMADO_NO_CODIGO] mitigado parcialmente nas `IMP-DOC-UPLOAD-001`, `IMP-DOC-UPLOAD-002` e `IMP-DOC-UPLOAD-003` |
| SEC-007 | Endpoint publico de documentacao Swagger/ReDoc | baixo | `/swagger/` e `/redoc/` publicos | Avaliar restricao em producao | [CONFIRMADO_NO_CODIGO] |
| SEC-008 | Ausencia de CORS explicito | medio | nenhuma config `corsheaders` encontrada | Validar politica CORS no ambiente real | [NAO_ENCONTRADO] |

## Notas adicionais

- [PRECISA_VALIDAR] Nao foi feita verificacao de vulnerabilidades de dependencias com scanner externo.
- [CONFIRMADO_NO_CODIGO] Permanecem warnings tecnicos conhecidos, incluindo `USE_L10N`, chave JWT curta no ambiente local e uso de `timezone.utc`.
