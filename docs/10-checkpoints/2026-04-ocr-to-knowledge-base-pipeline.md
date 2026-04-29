# Checkpoint - OCR to Knowledge Base Pipeline

## Objetivo

Implementar um fluxo controlado para executar OCR local, aplicar o texto extraido em `Document.content` apenas com confirmacao explicita e indexar o documento numa `KnowledgeBase` da mesma organizacao.

## Fluxo

1. Validar `document`, `knowledge_base` e `user` no mesmo tenant
2. Criar `OCRKnowledgeBasePipelineRun`
3. Executar OCR local sem sobrescrever o documento por defeito
4. Aplicar `OCRResult` ao `Document.content`
5. Reutilizar a indexacao existente do `knowledge_base`
6. Persistir referencias a `OCRJob`, `OCRResult`, `KnowledgeDocument` e `IndexingJob`

## Modelo novo

- `OCRKnowledgeBasePipelineRun`

## Endpoints

- `POST /api/v1/ocr/pipelines/knowledge-base/`
- `GET /api/v1/ocr/pipelines/`
- `GET /api/v1/ocr/pipelines/{id}/`

## Seguranca

- nenhum provider externo chamado
- `update_document_content=true` e obrigatorio no pipeline
- `document` e `knowledge_base` de outro tenant sao bloqueados
- falha de OCR impede indexacao
- falha de indexacao nao apaga `OCRResult` nem `Document.content`

## Testes

- `tests/test_ocr.py`: `11 passed`
- `tests/test_ocr_pipeline.py`: `8 passed`
- suite completa apos a entrega: `148 passed`

## Limitacoes

- o pipeline ainda depende de OCR local para `TXT`, `PDF` textual e `DOCX`
- nao existe OCR real de imagem nesta fase
- a indexacao continua dependente do texto aplicado em `Document.content`

## Proximos passos

- pipeline assinado para OCR de imagens/PDF escaneado
- observabilidade adicional por etapa, duracao e volume
- integracao opcional com `document_analysis`
- automatismos futuros sempre com governanca explicita por tenant
