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
| SEC-004 | Ausencia de rate limiting observavel | medio | configuracao global de throttling do DRF presente; endpoints sensiveis ainda podem merecer limites dedicados futuros | Evoluir para throttles especificos em login, refresh, IA e uploads conforme carga real | [CONFIRMADO_NO_CODIGO] mitigado parcialmente |
| SEC-005 | Segredo padrao fraco em fallback | medio | `SECRET_KEY` default `replace-me` | Exigir variavel obrigatoria em producao | [CONFIRMADO_NO_CODIGO] |
| SEC-006 | Upload de ficheiros sem validacao explicita de tipo/tamanho | medio | `Document.file` era aceite sem validacao adicional observavel; `DocumentSerializer` agora valida extensao, tamanho maximo de 10 MB, compatibilidade basica de `content_type` e assinatura binaria leve para `PDF`, `PNG` e `JPG/JPEG`; `document_upload_path` sanitiza explicitamente o `filename` | Monitorar necessidade de expandir assinatura binaria para formatos adicionais como `DOC`/`DOCX` ou parse mais forte em fase posterior | [CONFIRMADO_NO_CODIGO] mitigado parcialmente nas `IMP-DOC-UPLOAD-001`, `IMP-DOC-UPLOAD-002` e `IMP-DOC-UPLOAD-003` |
| SEC-007 | Endpoint publico de documentacao Swagger/ReDoc | baixo | rotas de documentacao agora so sao registradas quando `DEBUG=True` | Se houver necessidade operacional em producao, expor apenas atras de autenticacao administrativa | [CONFIRMADO_NO_CODIGO] mitigado |
| SEC-008 | Ausencia de CORS explicito | medio | configuracao explicita de `corsheaders`, `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` presente; ainda depende de configuracao operacional correta por ambiente | Validar origins reais de frontend e manter lista explicita sem wildcard em producao | [CONFIRMADO_NO_CODIGO] mitigado parcialmente |
| SEC-009 | RAG poderia vazar documentos entre tenants ou enviar conteudo para provider externo | alto | `knowledge_base` indexa, pesquisa, reindexa e lista `IndexingJob` apenas por `organization`; `ask` retorna fontes explicitas, `confidence`, `retrieval_method`, `effective_retrieval_mode` e `fallback` textual obrigatorio; `RAGSettings` exige opt-in explicito para embeddings externos; embeddings locais `local-hash-v1` rodam apenas dentro do backend | Preservar filtros por tenant, manter respostas sem invencao de conteudo, separar claramente embeddings locais de embeddings externos e so evoluir para providers externos com controles explicitos, consentimento e configuracao por tenant | [CONFIRMADO_NO_CODIGO] mitigado parcialmente nas fases 1, 2, governanca e embeddings locais do `knowledge_base` |
| SEC-010 | OCR poderia expor documentos a terceiros ou sobrescrever `Document.content` sem confirmacao explicita | medio | `ocr` executa apenas extracao local para `TXT`, `PDF` textual e `DOCX`; `OCRJob` e `OCRResult` filtram por `organization`; `run` nao sobrescreve `Document.content` por padrao; `apply-to-document` exige chamada explicita | Manter OCR externo desativado por defeito, preservar isolamento por tenant e introduzir qualquer provider futuro apenas com consentimento/configuracao clara por organizacao | [CONFIRMADO_NO_CODIGO] mitigado parcialmente na fundacao local de OCR |

## Notas adicionais

- [PRECISA_VALIDAR] Nao foi feita verificacao de vulnerabilidades de dependencias com scanner externo.
- [CONFIRMADO_NO_CODIGO] O backend agora aplica throttling global basico com `AnonRateThrottle` e `UserRateThrottle`; os rates podem ser ajustados via `DRF_THROTTLE_ANON` e `DRF_THROTTLE_USER`.
- [CONFIRMADO_NO_CODIGO] Em ambiente de testes, os rates sobem para valores muito altos para evitar flakiness e nao mascarar regressions funcionais.
- [CONFIRMADO_NO_CODIGO] O backend agora declara origins explicitas para CORS e CSRF via `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS`, com defaults voltados a `localhost` para desenvolvimento.
- [CONFIRMADO_NO_CODIGO] A fase atual do `knowledge_base` usa apenas busca textual local, indexacao de chunks no banco relacional, `IndexingJob` para observabilidade e respostas com `sources`; nenhum documento da organizacao e enviado a provider externo nesta etapa.
- [CONFIRMADO_NO_CODIGO] O backend agora suporta embeddings locais deterministas via `local-hash-v1`, gerados internamente e sem trafego de conteudo para fora do sistema.
- [CONFIRMADO_NO_CODIGO] A fundacao de embeddings externos continua bloqueada nesta fase; `prepare-embeddings` retorna `skipped`/`not_implemented` para providers como `openai`, `azure_openai` e `other`.
- [CONFIRMADO_NO_CODIGO] `RAGSettings` fica por `organization`, nasce com defaults seguros e exige opt-in explicito antes de qualquer evolucao futura para embeddings externos.
- [CONFIRMADO_NO_CODIGO] `EmbeddingAuditLog` registra tentativas ignoradas de embeddings sem armazenar conteudo bruto do documento.
- [CONFIRMADO_NO_CODIGO] O fallback textual continua obrigatorio quando o retrieval esta configurado como `embeddings` ou `hybrid`, mas embeddings locais ainda nao foram preparados ou providers externos nao estao efetivos.
- [CONFIRMADO_NO_CODIGO] A fundacao atual de `ocr` trabalha apenas com extracao local de `TXT`, `PDF` textual e `DOCX`; nao ha chamadas para Google Vision, Azure OCR, AWS Textract, OpenAI Vision ou provider externo equivalente.
- [CONFIRMADO_NO_CODIGO] `OCRJob` e `OCRResult` ficam sempre associados a `organization`, e a aplicacao do texto extraido em `Document.content` requer `update_document_content=true` ou `POST /api/v1/ocr/results/{id}/apply-to-document/`.
- [PRECISA_VALIDAR] PDF escaneado ou imagem ainda nao recebe OCR real nesta fase; isso reduz superficie externa, mas deixa cobertura funcional incompleta para documentos sem camada textual.
