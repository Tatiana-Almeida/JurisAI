# Checkpoint — OCR Observability and Tenant Limits

## Objetivo

Adicionar observabilidade por pagina e limites configuraveis por tenant ao OCR local de PDFs escaneados, mantendo processamento totalmente local, audit logs, fallback seguro e compatibilidade com o pipeline `OCR -> Document.content -> KnowledgeBase`.

## Modelos

- `OCRSettings`
  - `max_scanned_pdf_pages`
  - `max_ocr_file_size_mb`
  - `max_ocr_chars_output`
  - `store_page_level_ocr`
- `OCRPageResult`

## Endpoints

- `GET /api/v1/ocr/page-results/`
- `GET /api/v1/ocr/page-results/{id}/`
- `GET /api/v1/ocr/results/{id}/pages/`
- `GET/PATCH /api/v1/ocr/settings/`
- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`

## Limites

- `max_scanned_pdf_pages` controla quantas paginas de PDF escaneado podem ser processadas por tenant
- `max_ocr_file_size_mb` bloqueia OCR avancado para ficheiros acima do limite
- `max_ocr_chars_output` trunca output excessivo e marca metadata
- `store_page_level_ocr` controla se o backend persiste `OCRPageResult`

## Testes

- `tests/test_ocr.py`
- `tests/test_ocr_pipeline.py`
- `tests/test_ocr_governance.py`
- `tests/test_local_image_ocr.py`
- `tests/test_local_scanned_pdf_ocr.py`
- `tests/test_scanned_pdf_ocr_pipeline.py`
- `tests/test_ocr_observability.py`

## Seguranca

- nenhum provider externo chamado
- limites configurados por `organization`
- `OCRPageResult` filtrado por tenant
- ficheiros grandes falham com seguranca e geram `OCRAuditLog`
- truncamento de output e limite de paginas nao apagam ficheiro original nem `Document.content`

## Limitacoes

- execucao real ainda depende de `pdf2image`, Poppler e Tesseract no ambiente
- testes continuam a usar mocks para rasterizacao e OCR nativos
- o limite de paginas hoje e aplicado por truncamento de processamento, nao por rejeicao total do documento
- `Document.content` continua a ser atualizado apenas em fluxos explicitos

## Proximos passos

- observabilidade por pagina no payload do pipeline OCR -> KnowledgeBase
- limites adicionais por tenant para timeout e memoria de OCR
- metricas de qualidade do OCR por pagina
- controles operacionais antes de qualquer automacao adicional
