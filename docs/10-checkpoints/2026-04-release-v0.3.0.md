# Checkpoint — Release v0.3.0

## Release

- `v0.3.0` — Tenant-Isolated Legal RAG Foundation

## Commits principais

- `a2c2e4f` feat: add initial tenant-isolated knowledge base retrieval
- `d4818f3` feat: improve knowledge base retrieval observability
- `f2d3661` feat: add rag governance and embedding controls

## Objetivo

Consolidar a primeira fundacao funcional de RAG juridico do JurisAI, mantendo isolamento por tenant, `sources` obrigatorias, observabilidade e governanca para embeddings futuros.

## Funcionalidades incluidas

### Knowledge Base funcional

- `KnowledgeBase` por `organization`
- `KnowledgeDocument`
- `DocumentChunk`
- `RetrievalQuery`
- indexacao textual de documentos
- busca textual local
- `ask` com resposta fundamentada
- `sources` obrigatorias
- `sources_count`
- `confidence`
- `effective_retrieval_mode`
- `fallback_used`
- `fallback_reason`

### Observabilidade

- `IndexingJob`
- status `pending/running/completed/failed`
- `chunks_created`
- `chunks_deleted`
- `stats` por `knowledge base`
- reindexacao segura

### Governanca RAG

- `RAGSettings` por `organization`
- `EmbeddingAuditLog`
- opt-in explicito para embeddings externos
- external embeddings desativados por padrao
- `prepare-embeddings` seguro
- nenhum provider externo chamado nesta fase

## Endpoints principais

- `GET/POST /api/v1/knowledge-base/`
- `GET/POST /api/v1/knowledge-base/documents/`
- `GET /api/v1/knowledge-base/queries/`
- `GET /api/v1/knowledge-base/indexing-jobs/`
- `GET /api/v1/knowledge-base/indexing-jobs/{id}/`
- `GET/PATCH /api/v1/knowledge-base/settings/`
- `GET /api/v1/knowledge-base/embedding-audit-logs/`
- `POST /api/v1/knowledge-base/{id}/index-document/`
- `POST /api/v1/knowledge-base/{id}/reindex-document/`
- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`
- `GET /api/v1/knowledge-base/{id}/stats/`

## Testes

- `tests/test_knowledge_base.py`: `33 passed`
- suite completa: `121 passed`

## Seguranca

- tenant isolation validado
- nenhum provider externo ativado
- nenhum documento enviado para terceiros
- fallback textual obrigatorio
- fontes obrigatorias preservadas
- audit logs para pipeline de embeddings

## Limitacoes conhecidas

- retrieval ainda e textual
- embeddings reais ainda nao estao ativos
- nao ha banco vetorial
- OCR ainda nao esta integrado
- resposta ainda nao usa sintese juridica avancada por LLM
- `ChunkEmbedding` continua como fundacao
- provider externo continua desativado

## Proximos passos

- embeddings locais opcionais
- `hybrid retrieval`
- fallback textual com score combinado
- provider externo com consentimento explicito
- OCR integrado
- resposta com sintese juridica controlada e fontes
