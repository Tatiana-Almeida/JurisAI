# Checkpoint - Release v0.5.0

## Release

- v0.5.0 - OCR and Document Text Extraction Foundation

## Commit funcional principal

- 52db4d9 feat: add local document text extraction foundation

## Objetivo

Adicionar extracao local de texto documental ao JurisAI, permitindo preparar documentos para uso posterior no Knowledge Base / RAG sem recorrer a providers externos.

## Funcionalidades incluidas

- OCRJob
- OCRResult
- detecao local de metodo por extensao
- extracao de TXT
- extracao de PDF textual
- extracao de DOCX
- falha controlada para formatos nao suportados
- atualizacao opcional de Document.content
- aplicacao explicita de OCRResult ao Document.content
- tenant isolation em jobs e results

## Endpoints

- POST /api/v1/ocr/documents/{document_id}/run/
- GET /api/v1/ocr/jobs/
- GET /api/v1/ocr/jobs/{id}/
- GET /api/v1/ocr/results/
- GET /api/v1/ocr/results/{id}/
- POST /api/v1/ocr/results/{id}/apply-to-document/

## Dependencias

- pypdf>=4.2
- python-docx>=1.1

## Testes

- tests/test_ocr.py: 11 passed
- suite completa: 140 passed

## Seguranca

- nenhum provider externo chamado
- Document.content so e atualizado com confirmacao explicita
- arquivo original preservado
- tenant isolation validado
- falhas sao registradas sem apagar conteudo existente

## Limitacoes conhecidas

- ainda nao ha OCR real para imagens
- PDF escaneado sem camada textual ainda nao extrai conteudo util
- DOC legado permanece fora do escopo
- nao ha indexacao automatica no knowledge_base nesta fase

## Proximos passos

- fluxo OCR -> apply-to-document -> indexar no knowledge_base
- OCR para imagens/PDF escaneado com provider local ou governanca externa
- observabilidade avancada do pipeline OCR
- integracao opcional com document_analysis
