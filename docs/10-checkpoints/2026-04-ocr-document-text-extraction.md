# Checkpoint — OCR and Document Text Extraction Foundation

## Objetivo

Implementar a primeira fundacao funcional de OCR local no JurisAI para extrair texto de `TXT`, `PDF` com camada textual e `DOCX`, sem chamadas a providers externos e sem sobrescrever `Document.content` por padrao.

## Formatos suportados

- `TXT`
- `PDF` textual
- `DOCX`

## Endpoints

- `POST /api/v1/ocr/documents/{document_id}/run/`
- `GET /api/v1/ocr/jobs/`
- `GET /api/v1/ocr/jobs/{id}/`
- `GET /api/v1/ocr/results/`
- `GET /api/v1/ocr/results/{id}/`
- `POST /api/v1/ocr/results/{id}/apply-to-document/`

## Seguranca

- Extracao apenas local nesta fase
- Nenhum documento enviado para provider externo
- `OCRJob` e `OCRResult` filtrados por `organization`
- Documento de outro tenant nao pode ser processado
- `Document.content` so muda com `update_document_content=true` ou `apply-to-document`
- Formatos `unsupported` falham de forma controlada e auditavel

## Testes

- `tests/test_ocr.py`: `11 passed`
- Suite completa apos a entrega: `140 passed`

## Limitacoes

- Nao existe OCR real para imagens nesta fase
- `PDF` so extrai texto quando existe camada textual
- Nao existe indexacao automatica no `knowledge_base`
- `DOC` binario legado continua fora do escopo

## Proximos passos

- OCR para imagens e PDFs escaneados
- Integracao opcional com pipeline de `knowledge_base`
- Extracao automatica de prazos a partir do texto extraido
- Observabilidade adicional para custo, volume e qualidade de extracao
