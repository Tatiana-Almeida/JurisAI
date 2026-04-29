# Checkpoint — Release v0.11.0

## Release

- v0.11.0 — OCR Observability and Tenant Limits

## Objetivo

Adicionar observabilidade por página e limites configuráveis por tenant ao OCR de PDFs escaneados, protegendo o sistema contra abuso, custos excessivos de processamento e crescimento descontrolado de armazenamento.

## Funcionalidades incluídas

- `OCRPageResult`
- `max_scanned_pdf_pages`
- `max_ocr_file_size_mb`
- `max_ocr_chars_output`
- `store_page_level_ocr`
- page results endpoints
- OCR result pages endpoint
- metadata de truncamento
- metadata de limite de páginas
- proteção contra ficheiros grandes
- observabilidade por página
- tenant isolation em page results

## Endpoints

- `GET /api/v1/ocr/page-results/`
- `GET /api/v1/ocr/page-results/{id}/`
- `GET /api/v1/ocr/results/{id}/pages/`

## Testes

- `tests/test_ocr.py`: 11 passed
- `tests/test_ocr_pipeline.py`: 8 passed
- `tests/test_ocr_governance.py`: 11 passed
- `tests/test_local_image_ocr.py`: 6 passed
- `tests/test_local_scanned_pdf_ocr.py`: 9 passed
- `tests/test_scanned_pdf_ocr_pipeline.py`: 6 passed
- `tests/test_ocr_observability.py`: 10 passed
- suíte completa: 190 passed

## Segurança

- nenhum provider externo chamado
- tenant isolation preservado
- OCR page results filtrados por `organization`
- limites de tamanho ajudam a prevenir abuso
- limites de páginas ajudam a controlar custo de processamento
- truncamento controla crescimento de armazenamento
- OCR e OCR-to-KnowledgeBase existentes preservados

## Limitações conhecidas

- execução real ainda depende de `pdf2image`, Poppler e Tesseract no ambiente
- testes nativos continuam mockados por desenho
- pipeline ainda depende de aplicar texto em `Document.content` antes da indexação
- limite de páginas atualmente reduz o processamento em vez de rejeitar o documento completo

## Próximos passos

- adicionar observabilidade por página no payload do pipeline
- adicionar timeout configurável por tenant
- adicionar orçamento de processamento por tenant
- preparar release candidata `v1.0.0`
