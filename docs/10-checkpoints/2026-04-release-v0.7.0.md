# Checkpoint - Release v0.7.0

## Release

- v0.7.0 - Advanced OCR Governance

## Objetivo

Adicionar governanca para OCR avancado, preparando suporte futuro a imagens e PDFs escaneados sem ativar provider externo por padrao.

## Funcionalidades incluidas

- OCRSettings
- OCRAuditLog
- settings de OCR por organization
- opt-in explicito para OCR externo
- endpoint advanced-run governado
- audit logs para tentativas de OCR avancado
- preservacao do OCR local atual para TXT, PDF textual e DOCX
- preservacao do pipeline OCR -> KnowledgeBase

## Endpoints

- GET/PATCH /api/v1/ocr/settings/
- GET /api/v1/ocr/audit-logs/
- POST /api/v1/ocr/documents/{document_id}/advanced-run/

## Testes

- tests/test_ocr.py: 11 passed
- tests/test_ocr_pipeline.py: 8 passed
- tests/test_ocr_governance.py: 11 passed
- suite completa: 159 passed

## Seguranca

- OCR externo desativado por padrao
- opt-in explicito obrigatorio para OCR externo
- nenhum provider externo chamado
- nenhum conteudo documental sai do sistema
- tenant isolation validado
- tentativas de OCR avancado auditadas
- fluxos OCR e OCR -> KnowledgeBase existentes preservados

## Limitacoes conhecidas

- ainda nao ha OCR real para imagens
- PDFs escaneados continuam sem extracao util
- advanced-run ainda e placeholder governado
- providers externos ainda nao estao implementados

## Proximos passos

- OCR local real para imagens/PDFs escaneados
- Tesseract/local OCR opcional
- observabilidade por etapa
- integracao futura com provider externo apenas com opt-in explicito
