# Checkpoint - Local Scanned PDF OCR Foundation

## Objetivo

Adicionar uma fundacao segura de OCR local para PDFs escaneados no JurisAI, usando rasterizacao local opcional e OCR por pagina com Tesseract, sem qualquer chamada a provider externo.

## Engine local

- `ocr/local_engines.py`
- `TesseractOCREngine.extract_text_from_scanned_pdf()`
- rasterizacao local opcional via `pdf2image`
- OCR local por pagina usando a mesma fundacao governada da image OCR
- fallback controlado quando `pdf2image`, Poppler ou Tesseract nao estao disponiveis

## Dependencias opcionais

- `pdf2image`
- Poppler instalado no sistema
- `pytesseract`
- binario nativo do Tesseract

## Endpoints impactados

- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- `GET/PATCH /api/v1/ocr/settings/`
- `GET /api/v1/ocr/audit-logs/`

## Testes

- `tests/test_local_scanned_pdf_ocr.py`
- regressao de `tests/test_ocr.py`
- regressao de `tests/test_local_image_ocr.py`
- regressao de `tests/test_ocr_pipeline.py`
- regressao de `tests/test_ocr_governance.py`

## Limitacoes

- a execucao real depende de `pdf2image` e Poppler disponiveis no ambiente
- a execucao real continua dependente do binario do Tesseract
- os testes validam o adapter e o fluxo com mocks, nao com binarios reais obrigatorios
- `Document.content` nao e atualizado automaticamente neste fluxo

## Proximos passos

- limitar paginas por configuracao por tenant, se o custo justificar
- integrar scanned PDF OCR ao pipeline `OCR -> KnowledgeBase` de forma opcional e explicita
- adicionar observabilidade mais fina por pagina
- manter providers externos bloqueados por defeito ate haver governanca operacional completa
