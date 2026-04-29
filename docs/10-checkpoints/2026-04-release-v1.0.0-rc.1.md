# Checkpoint — Release v1.0.0-rc.1

## Release

- v1.0.0-rc.1 — Backend MVP Stabilization

## Objetivo

Publicar a primeira release candidate do backend MVP do JurisAI, consolidando funcionalidades jurídicas, RAG, OCR, pipelines documentais, CI, Docker runtime e hardening de deploy.

## Estado validado

- pytest local: 192 passed
- pytest container: 192 passed
- healthcheck: 200
- docker compose build: passed
- docker compose up: passed
- Redis com password: validado
- Redis sem porta pública: validado
- web/worker/flower: non-root appuser
- Flower sem porta pública direta
- production readiness checklist criada

## Funcionalidades consolidadas

### Core SaaS jurídico

- autenticação
- organizações
- multi-tenancy
- gestão de processos
- prazos
- documentos
- auditoria
- billing SaaS
- notificações

### Serviços jurídicos expandidos

- dashboard
- tarefas internas
- portal do cliente
- agenda jurídica
- templates jurídicos
- financeiro jurídico

### Knowledge Base / RAG

- KnowledgeBase por tenant
- DocumentChunk
- RetrievalQuery
- IndexingJob
- RAGSettings
- EmbeddingAuditLog
- ChunkEmbedding
- busca textual
- embeddings locais
- hybrid retrieval
- ask com sources
- confidence
- fallback textual

### OCR e pipelines documentais

- OCRJob
- OCRResult
- OCRPageResult
- OCRSettings
- OCRAuditLog
- OCR local TXT
- OCR PDF textual
- OCR DOCX
- OCR imagem PNG/JPG/JPEG
- OCR PDF escaneado
- pipeline OCR -> Document.content -> KnowledgeBase
- fallback PDF textual -> PDF escaneado
- observabilidade por página
- limites por tenant

### Infraestrutura

- GitHub Actions CI
- healthcheck /health/
- Docker runtime validado
- containers non-root
- Redis com password e sem porta pública
- Flower com basic auth e sem porta pública direta
- requirements pinado
- collectstatic fora do build obrigatório
- Tesseract e Poppler no container
- production readiness checklist

## Releases anteriores consolidadas

- v0.2.0 — Expanded Legal Services Foundation
- v0.3.0 — Tenant-Isolated Legal RAG Foundation
- v0.4.0 — Local Embeddings and Hybrid Retrieval
- v0.5.0 — OCR and Document Text Extraction Foundation
- v0.6.0 — OCR to Knowledge Base Pipeline
- v0.7.0 — Advanced OCR Governance
- v0.8.0 — Local Image OCR Engine
- v0.9.0 — Local Scanned PDF OCR Foundation
- v0.10.0 — Scanned PDF OCR to Knowledge Base Pipeline
- v0.11.0 — OCR Observability and Tenant Limits

## Segurança

- tenant isolation preservado
- providers externos desativados por padrão
- nenhum OCR/RAG externo obrigatório
- Redis protegido
- Flower protegido
- containers non-root
- healthcheck sem dados sensíveis
- secrets fora do repositório
- checklist de produção criada

## Limitações conhecidas

- frontend ainda não incluído
- produção real ainda requer reverse proxy, TLS, backups e observabilidade externa
- billing real/pagamentos ainda precisam integração final
- notificações reais por e-mail/WhatsApp ainda precisam integração final
- OCR real depende de binários nativos no ambiente
- embeddings locais ainda não são semânticos avançados
- providers externos continuam desativados/não implementados por padrão

## Próximos passos

- frontend web
- deploy real com domínio, TLS e reverse proxy
- roles/permissões avançadas
- observabilidade externa
- backups automáticos
- billing real
- notificações reais
- preparação de v1.0.0 estável
