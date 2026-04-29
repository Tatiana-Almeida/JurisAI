# Checkpoint - Advanced OCR Governance

## Objetivo

Adicionar governanca para OCR avancado por organizacao, preparando suporte futuro a imagens e PDFs escaneados sem ativar provider externo por defeito.

## Modelos

- OCRSettings
- OCRAuditLog

## Endpoints

- GET/PATCH /api/v1/ocr/settings/
- GET /api/v1/ocr/audit-logs/
- POST /api/v1/ocr/documents/{document_id}/advanced-run/

## Seguranca

- defaults seguros por `organization`
- OCR externo desativado por defeito
- opt-in explicito obrigatorio para qualquer OCR externo futuro
- nenhuma tentativa envia documentos para fora do sistema nesta fase
- `OCRAuditLog` registra provider, modo e motivo sem guardar conteudo bruto
- `advanced-run` e filtrado por tenant

## Limitacoes

- nenhum OCR real de imagem nesta fase
- nenhum provider externo implementado
- `local_placeholder` ainda so registra `skipped`
- PDFs escaneados continuam sem extracao util real

## Testes

- tests/test_ocr.py: 11 passed
- tests/test_ocr_pipeline.py: 8 passed
- tests/test_ocr_governance.py: 11 passed
- suite completa apos a entrega: 159 passed

## Proximos passos

- OCR local real para imagens/PDF escaneado
- provider externo opcional com consentimento explicito por tenant
- observabilidade por custo, duracao e volume de OCR avancado
- integracao futura com `document_analysis`
