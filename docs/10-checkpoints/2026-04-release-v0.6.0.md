# Checkpoint - Release v0.6.0

## Release

- v0.6.0 - OCR to Knowledge Base Pipeline

## Objetivo

Adicionar um pipeline controlado para executar OCR, aplicar o texto extraido em `Document.content` e indexar o documento em uma `KnowledgeBase` com isolamento por tenant e fontes obrigatorias.

## Funcionalidades incluidas

- OCRKnowledgeBasePipelineRun
- Pipeline OCR -> Document.content -> KnowledgeBase
- Execucao explicita por endpoint
- Validacao de `document`, `knowledge_base` e `user` no mesmo tenant
- Exigencia de `update_document_content=true`
- Referencias para `OCRJob`, `OCRResult`, `KnowledgeDocument` e `IndexingJob`
- Falha controlada quando OCR falha
- Preservacao de `OCRResult` e `Document.content` se a indexacao falhar
- Ask com `sources` apos pipeline concluido

## Endpoints

- POST /api/v1/ocr/pipelines/knowledge-base/
- GET /api/v1/ocr/pipelines/
- GET /api/v1/ocr/pipelines/{id}/

## Testes

- tests/test_ocr.py: 11 passed
- tests/test_ocr_pipeline.py: 8 passed
- suite completa: 148 passed

## Seguranca

- nenhum provider externo chamado
- tenant isolation validado
- cross-tenant document bloqueado
- cross-tenant KnowledgeBase bloqueado
- Document.content so e atualizado com confirmacao explicita
- OCR failure impede indexacao
- indexing failure preserva OCRResult e Document.content aplicado

## Limitacoes conhecidas

- ainda nao ha OCR real para imagens
- PDFs escaneados sem camada textual ainda nao sao cobertos
- o pipeline depende de aplicar texto em Document.content antes da indexacao
- nao ha reindexacao automatica fora da execucao explicita do pipeline

## Proximos passos

- OCR para imagens/PDF escaneado
- observabilidade avancada por etapa
- provider externo com governanca e opt-in
- integracao opcional com document_analysis
- metricas de qualidade do OCR e do retrieval
