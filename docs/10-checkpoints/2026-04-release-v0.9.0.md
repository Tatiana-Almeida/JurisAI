# Checkpoint - Release v0.9.0

## Release

- v0.9.0 - Local Scanned PDF OCR Foundation

## Objetivo

Adicionar uma fundacao de OCR local para PDFs escaneados ao JurisAI, mantendo processamento local, governanca por tenant, audit logs, fallback seguro e zero chamadas para providers externos.

## Commit funcional principal

- feat: add local scanned pdf ocr foundation

## Funcionalidades incluidas

- PDFRasterizationUnavailable
- ScannedPDFOCRUnavailable
- TesseractOCREngine.extract_text_from_scanned_pdf(...)
- run_local_scanned_pdf_ocr(...)
- rasterizacao local de PDF via pdf2image quando disponivel
- OCR local por pagina com engine governada
- falha controlada quando Poppler/pdf2image nao estao disponiveis
- falha controlada quando Tesseract nao esta disponivel
- OCRAuditLog para tentativas de OCR em PDF escaneado
- preservacao do OCR textual de PDF
- preservacao do OCR local de imagens
- preservacao do pipeline OCR -> KnowledgeBase

## Endpoints impactados

- POST /api/v1/ocr/documents/{document_id}/advanced-run/
- GET/PATCH /api/v1/ocr/settings/
- GET /api/v1/ocr/audit-logs/

## Dependencias

- pdf2image>=1.17.0
- pillow>=10.0
- pytesseract>=0.3.10

## Testes

- tests/test_ocr.py: 11 passed
- tests/test_ocr_pipeline.py: 8 passed
- tests/test_ocr_governance.py: 11 passed
- tests/test_local_image_ocr.py: 6 passed
- tests/test_local_scanned_pdf_ocr.py: 9 passed
- suite completa: 174 passed

## Seguranca

- nenhum provider externo chamado
- OCR externo continua desativado por padrao
- OCR de PDF escaneado so roda com configuracao explicita por tenant
- tentativas sao auditadas
- tenant isolation preservado
- falhas nao apagam documento nem conteudo existente
- Document.content nao e atualizado automaticamente

## Limitacoes conhecidas

- execucao real depende de pdf2image + Poppler + Tesseract instalados no ambiente
- testes usam mocks e nao exigem binarios reais
- Document.content continua sem atualizacao automatica nesse caminho
- nao ha provider externo nem OCR avancado remoto nesta fase

## Proximos passos

- integrar PDF escaneado ao pipeline OCR -> KnowledgeBase de forma opcional e explicita
- adicionar metricas de qualidade do OCR
- avaliar suporte a limites de paginas e tamanho por tenant
- manter provider externo desativado por padrao
