# Checkpoint - Release v0.8.0

## Release

- v0.8.0 - Local Image OCR Engine

## Commit funcional principal

- c7ffb5f feat: add local image ocr engine foundation

## Objetivo

Adicionar uma fundacao de OCR local para imagens ao JurisAI, usando adapter opcional de Tesseract, preservando governanca por tenant, audit logs, fallback seguro e zero chamadas externas.

## Funcionalidades incluidas

- LocalOCREngineUnavailable
- BaseLocalOCREngine
- TesseractOCREngine
- get_local_ocr_engine
- run_local_image_ocr
- run_local_scanned_pdf_ocr
- run_advanced_ocr
- suporte governado a PNG, JPG e JPEG
- falha controlada quando Tesseract nao esta disponivel
- OCRAuditLog para tentativas de OCR local avancado

## Endpoints impactados

- POST /api/v1/ocr/documents/{document_id}/advanced-run/
- GET/PATCH /api/v1/ocr/settings/
- GET /api/v1/ocr/audit-logs/

## Testes

- tests/test_ocr.py: 11 passed
- tests/test_ocr_pipeline.py: 8 passed
- tests/test_ocr_governance.py: 11 passed
- tests/test_local_image_ocr.py: 6 passed
- suite completa: 165 passed

## Seguranca

- nenhum provider externo chamado
- OCR externo continua desativado por padrao
- local image OCR so roda com configuracao explicita por tenant
- tentativas sao auditadas
- tenant isolation preservado
- OCR textual existente preservado
- OCR -> KnowledgeBase preservado

## Limitacoes conhecidas

- OCR real depende do binario Tesseract instalado no sistema
- testes usam mocks e nao exigem Tesseract real
- PDF escaneado ainda e placeholder governado
- image OCR nao atualiza Document.content automaticamente

## Proximos passos

- OCR local para PDFs escaneados
- integracao opcional com pipeline OCR -> KnowledgeBase
- metricas de qualidade do OCR
- provider externo somente com opt-in explicito
