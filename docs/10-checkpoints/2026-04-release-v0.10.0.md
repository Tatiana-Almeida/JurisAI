# Checkpoint - Release v0.10.0

## Release

- v0.10.0 - Scanned PDF OCR to Knowledge Base Pipeline

## Objetivo

Integrar OCR local governado de PDFs escaneados ao pipeline `OCR -> Document.content -> KnowledgeBase`, permitindo que PDFs sem texto util sejam processados e indexados de forma explicita, auditavel e tenant-isolated.

## Funcionalidades incluidas

- Fallback de OCR textual para OCR local de PDF escaneado
- has_useful_extracted_text(...)
- run_ocr_to_knowledge_base_pipeline(...) atualizado
- used_advanced_ocr no payload do pipeline
- advanced_ocr_reason no payload do pipeline
- ocr_audit_log no payload do pipeline
- preservacao de OCRJob, OCRResult, OCRAuditLog e metadados em falhas
- ask com sources apos pipeline concluido
- tenant isolation preservado
- zero chamadas externas

## Endpoints impactados

- POST /api/v1/ocr/pipelines/knowledge-base/
- POST /api/v1/ocr/documents/{document_id}/advanced-run/
- GET/PATCH /api/v1/ocr/settings/
- GET /api/v1/ocr/audit-logs/

## Testes

- tests/test_ocr.py: 11 passed
- tests/test_ocr_pipeline.py: 8 passed
- tests/test_local_scanned_pdf_ocr.py: 9 passed
- tests/test_scanned_pdf_ocr_pipeline.py: 6 passed
- suite completa: 180 passed

## Seguranca

- nenhum provider externo chamado
- scanned PDF OCR governado por settings do tenant
- Document.content so e atualizado com confirmacao explicita
- cross-tenant access bloqueado
- OCR attempts auditadas
- falha de OCR impede indexacao
- falha de indexacao preserva OCRResult e Document.content aplicado

## Limitacoes conhecidas

- execucao real ainda depende de pdf2image, Poppler e Tesseract no ambiente
- deteccao de texto util ainda e heuristica
- pipeline ainda depende de aplicar texto em Document.content antes da indexacao

## Proximos passos

- observabilidade por pagina
- limites configuraveis por tenant
- metricas de qualidade do OCR
- preparacao para release candidata v1.0.0
