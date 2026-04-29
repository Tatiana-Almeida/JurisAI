# Checkpoint — Release v0.4.0

## Release

- v0.4.0 — Local Embeddings and Hybrid Retrieval

## Commit principal

- 56c5c8f feat: add local embedding pipeline for hybrid retrieval

## Objetivo

Adicionar embeddings locais opcionais e recuperacao hibrida ao JurisAI, mantendo isolamento por tenant, sources obrigatorias, fallback textual e zero chamadas a providers externos.

## Funcionalidades incluidas

- `LocalHashEmbeddingProvider`
- `ExternalEmbeddingProviderPlaceholder`
- `get_embedding_provider`
- `generate_local_embedding`
- `cosine_similarity`
- `generate_chunk_embeddings`
- `search_chunks_by_embedding`
- `hybrid_search_chunks`
- `get_retrieval_method`
- `fallback_to_textual_search`
- `retrieve_chunks_for_query`

## Endpoints impactados

- `GET/PATCH /api/v1/knowledge-base/settings/`
- `GET /api/v1/knowledge-base/embedding-audit-logs/`
- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`
- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`

## Comportamento

- `prepare-embeddings` gera `ChunkEmbedding` local com `provider="local"` e `model="local-hash-v1"`
- `ask` pode retornar `retrieval_method="textual"`
- `ask` pode retornar `retrieval_method="local_embedding"`
- `ask` pode retornar `retrieval_method="hybrid"`
- `ask` pode retornar `retrieval_method="textual_fallback"`
- `sources` incluem `final_score`
- `sources` incluem `text_score` quando aplicavel
- `sources` incluem `embedding_score` quando aplicavel
- providers externos continuam `skipped`/`not_implemented`
- fallback textual continua obrigatorio

## Testes

- `tests/test_knowledge_base.py`: `41 passed`
- suite completa: `129 passed`

## Seguranca

- nenhum provider externo ativado
- nenhuma chamada externa feita
- tenant isolation preservado
- sources obrigatorias preservadas
- fallback textual preservado
- audit logs preservados

## Limitacoes conhecidas

- `local-hash-v1` e deterministico, mas nao e embedding semantico real
- ainda nao ha banco vetorial
- providers externos continuam nao implementados
- retrieval hibrido ainda e heuristico
- OCR ainda nao esta integrado

## Proximos passos

- embeddings locais semanticamente mais fortes
- OCR integrado
- provider externo com consentimento explicito
- banco vetorial opcional
- avaliacao de qualidade do retrieval
