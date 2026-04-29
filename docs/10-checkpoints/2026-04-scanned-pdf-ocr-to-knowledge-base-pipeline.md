# Checkpoint - Scanned PDF OCR to KnowledgeBase Pipeline

## Objetivo

Integrar o OCR local governado para PDF escaneado ao pipeline `OCR -> Document.content -> KnowledgeBase`, sem chamadas externas e mantendo o contrato atual do endpoint com extensoes seguras no payload.

## Fluxo

- tentativa de OCR textual padrao para PDF
- verificacao de texto util
- fallback opcional para OCR local de PDF escaneado quando o tenant habilita `scanned_pdf_ocr_mode=local`
- atualizacao explicita de `Document.content` com `update_document_content=true`
- indexacao no `knowledge_base`
- `ask` com `sources`

## Configuracoes necessarias

- `advanced_ocr_enabled=true`
- `scanned_pdf_ocr_mode=local`
- provider local `tesseract` ou `local`
- dependencias nativas opcionais disponiveis quando se quiser execucao real

## Endpoints impactados

- `POST /api/v1/ocr/pipelines/knowledge-base/`
- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- `GET/PATCH /api/v1/ocr/settings/`
- `GET /api/v1/ocr/audit-logs/`

## Testes

- `tests/test_ocr_pipeline.py`
- `tests/test_local_scanned_pdf_ocr.py`
- `tests/test_scanned_pdf_ocr_pipeline.py`

## Seguranca

- nenhum provider externo chamado
- fallback para OCR avancado so acontece com configuracao explicita por tenant
- `Document.content` so muda com `update_document_content=true`
- falhas de OCR avancado nao apagam conteudo existente
- `OCRAuditLog` registra a tentativa avancada
- tenant isolation preservado em `document`, `knowledge_base`, `OCRJob`, `OCRResult` e `pipeline_run`

## Limitacoes

- a execucao real continua dependente de `pdf2image`, Poppler e Tesseract no ambiente
- o threshold de texto util e heuristico
- o fluxo ainda depende da aplicacao em `Document.content` antes da indexacao

## Proximos passos

- ligar OCR avancado de PDF escaneado a observabilidade por pagina
- avaliar limites de paginas e tamanho por tenant
- adicionar metrica de qualidade do OCR antes da indexacao
- manter providers externos desativados por padrao ate nova camada de governanca
