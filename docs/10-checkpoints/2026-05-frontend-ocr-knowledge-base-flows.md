# Checkpoint - Frontend OCR and Knowledge Base Flows

## Objetivo

- [CONFIRMADO_NO_CODIGO] Integrar os fluxos reais de OCR e Knowledge Base no Frontend MVP.
- [CONFIRMADO_NO_CODIGO] Ligar o fluxo `documento -> OCR -> resultado -> Document.content -> Knowledge Base -> pergunta com fontes`.

## Endpoints integrados

- [CONFIRMADO_NO_CODIGO] `GET /api/v1/ocr/jobs/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/ocr/results/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/ocr/page-results/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/ocr/results/{id}/pages/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/ocr/audit-logs/`
- [CONFIRMADO_NO_CODIGO] `GET/PATCH /api/v1/ocr/settings/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/ocr/documents/{document_id}/run/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/ocr/results/{id}/apply-to-document/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/ocr/pipelines/knowledge-base/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/ocr/pipelines/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/knowledge-base/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/knowledge-base/{id}/stats/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/knowledge-base/documents/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/knowledge-base/queries/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/knowledge-base/indexing-jobs/`
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/knowledge-base/embedding-audit-logs/`
- [CONFIRMADO_NO_CODIGO] `GET/PATCH /api/v1/knowledge-base/settings/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/knowledge-base/{id}/search/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/knowledge-base/{id}/ask/`
- [CONFIRMADO_NO_CODIGO] `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`

## OCR UI

- [CONFIRMADO_NO_CODIGO] A pagina `frontend/app/ocr/page.tsx` passou a usar tabs para `Jobs`, `Results`, `Page Results`, `Audit Logs`, `Settings` e `Pipelines`.
- [CONFIRMADO_NO_CODIGO] `frontend/components/ocr/ocr-job-table.tsx` lista jobs com estado, metodo, datas e acoes de navegacao.
- [CONFIRMADO_NO_CODIGO] `frontend/components/ocr/ocr-result-card.tsx` mostra texto extraido, metadata operacional, avisos de truncamento e acao `Aplicar ao documento`.
- [CONFIRMADO_NO_CODIGO] `frontend/components/ocr/page-results-table.tsx` mostra OCR por pagina com detalhe expandivel.
- [CONFIRMADO_NO_CODIGO] `frontend/components/ocr/ocr-audit-log-table.tsx` mostra audit logs de OCR com metadata.

## OCR settings

- [CONFIRMADO_NO_CODIGO] `frontend/components/ocr/ocr-settings-panel.tsx` usa React Hook Form + Zod.
- [CONFIRMADO_NO_CODIGO] O formulario envia `PATCH /api/v1/ocr/settings/` e continua a mapear erros DRF para campos.
- [CONFIRMADO_NO_CODIGO] A UI deixa explicito que OCR externo continua desligado por padrao.

## OCR audit logs e page results

- [CONFIRMADO_NO_CODIGO] Jobs e pipelines usam polling apenas enquanto existirem itens `pending` ou `running`.
- [CONFIRMADO_NO_CODIGO] Page results e audit logs respeitam as query keys com `organizationId`.

## OCR -> Knowledge Base pipeline

- [CONFIRMADO_NO_CODIGO] `frontend/components/ocr/ocr-pipeline-card.tsx` prepara `POST /api/v1/ocr/pipelines/knowledge-base/`.
- [CONFIRMADO_NO_CODIGO] O frontend exige confirmacao explicita para `update_document_content=true`.
- [CONFIRMADO_NO_CODIGO] O detalhe do documento passou a expor a acao `OCR -> Knowledge Base`.

## Knowledge Base UI

- [CONFIRMADO_NO_CODIGO] `frontend/app/knowledge-base/page.tsx` lista bases, stats resumidos e indexing jobs.
- [CONFIRMADO_NO_CODIGO] `frontend/app/knowledge-base/[id]/page.tsx` usa tabs para `Overview`, `Search`, `Ask`, `Documents`, `Indexing Jobs`, `Settings` e `Audit Logs`.
- [CONFIRMADO_NO_CODIGO] `frontend/components/knowledge-base/kb-search.tsx` integra `search`.
- [CONFIRMADO_NO_CODIGO] `frontend/components/knowledge-base/kb-ask.tsx` integra `ask`.
- [CONFIRMADO_NO_CODIGO] `frontend/components/knowledge-base/sources-list.tsx` mostra `confidence`, `retrieval_method`, `fallback_used`, `fallback_reason`, `final_score`, `text_score` e `embedding_score` quando disponiveis.
- [CONFIRMADO_NO_CODIGO] `frontend/components/knowledge-base/rag-settings-panel.tsx` integra `PATCH /api/v1/knowledge-base/settings/`.
- [CONFIRMADO_NO_CODIGO] `frontend/components/knowledge-base/indexing-jobs-table.tsx` mostra jobs de indexacao com polling.

## Multi-tenancy

- [CONFIRMADO_NO_CODIGO] Query keys de OCR e Knowledge Base incluem `organizationId`.
- [CONFIRMADO_NO_CODIGO] Os hooks dependentes de tenant usam `enabled: Boolean(organizationId)`.
- [CONFIRMADO_NO_CODIGO] Sem organizacao ativa, as telas mostram estado explicito em vez de misturar dados entre tenants.

## Limitacoes

- [CONFIRMADO_NO_CODIGO] `local-hash-v1` continua documentado apenas como fundacao tecnica local, nao como IA semantica juridica completa.
- [CONFIRMADO_NO_CODIGO] Billing continua honesto e separado desta fase.
- [PRECISA_VALIDAR] O fluxo autenticado real contra staging continua dependente de credenciais fora do repositrio.
- [PRECISA_VALIDAR] No Render Free, jobs de OCR e indexacao podem continuar limitados se o worker Celery nao estiver ativo.

## Testes

- [CONFIRMADO_NO_CODIGO] `npm.cmd run typecheck`
- [CONFIRMADO_NO_CODIGO] `npm.cmd run lint`
- [CONFIRMADO_NO_CODIGO] `npm.cmd run test`
- [CONFIRMADO_NO_CODIGO] `npm.cmd run build`
- [CONFIRMADO_NO_CODIGO] `npm.cmd run test:e2e`
- [CONFIRMADO_NO_CODIGO] `python manage.py check`
- [CONFIRMADO_NO_CODIGO] `python -m pytest -q tests/test_knowledge_base.py tests/test_ocr.py tests/test_ocr_governance.py tests/test_ocr_observability.py tests/test_ocr_pipeline.py`
- [PRECISA_VALIDAR] `python -m pytest` completo excedeu o timeout desta sessao, apesar de nao terem existido alteracoes no backend nesta fase.

## Proximos passos

- [CONFIRMADO_NO_CODIGO] Refinar a UX de OCR e Knowledge Base com dados autenticados de staging.
- [CONFIRMADO_NO_CODIGO] Validar o fluxo real com worker Celery disponivel.
- [CONFIRMADO_NO_CODIGO] Fechar os modulos comerciais que ainda permanecem honestamente marcados como pendentes.
