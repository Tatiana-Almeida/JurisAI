# Checkpoint - Local Image OCR Engine Foundation

## Objetivo

Adicionar uma fundacao segura de OCR local para imagens no JurisAI, sem qualquer chamada a provider externo e sem quebrar o OCR textual atual, o pipeline `OCR -> KnowledgeBase` ou o isolamento por tenant.

## Engine local

- `ocr/local_engines.py`
- `TesseractOCREngine` como adapter opcional e local
- deteccao segura de dependencias Python opcionais
- deteccao segura da indisponibilidade do binario nativo do Tesseract
- fallback controlado com erro auditavel quando a engine nao esta disponivel

## Endpoints impactados

- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- `GET/PATCH /api/v1/ocr/settings/`
- `GET /api/v1/ocr/audit-logs/`

## Comportamento

- `advanced-run` continua governado por `OCRSettings`
- imagens `PNG`, `JPG` e `JPEG` podem usar OCR local quando `image_ocr_mode=local`
- o provider preferido pode ser `local` ou `tesseract`
- se a engine local estiver indisponivel, o backend retorna falha controlada com `OCRJob` e `OCRAuditLog`
- OCR de PDF escaneado continua placeholder seguro nesta fase
- nenhum documento e enviado para fora do sistema

## Testes

- `tests/test_local_image_ocr.py`
- `tests/test_ocr_governance.py`
- `tests/test_ocr.py`
- `tests/test_ocr_pipeline.py`

## Limitacoes

- `tesseract` continua opcional e nao e exigido para a suite
- OCR de imagem foi validado por adapter e fluxo com mocks, nao por binario real em CI local
- PDF escaneado ainda nao tem pipeline local estavel nesta fase
- OCR atual para `TXT`, `PDF` textual e `DOCX` continua sendo o caminho funcional principal

## Proximos passos

- adicionar OCR local real para PDF escaneado quando a cadeia nativa estiver estavel
- melhorar deteccao de candidatos a imagem/PDF escaneado
- avaliar Tesseract real em pipeline opcional de desenvolvimento
- manter provider externo bloqueado por defeito ate haver governanca operacional completa
