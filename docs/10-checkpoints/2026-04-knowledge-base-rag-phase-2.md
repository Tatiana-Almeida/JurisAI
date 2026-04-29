# Checkpoint — Knowledge Base / RAG fase 2

## Objetivo

Melhorar a primeira versao funcional do `knowledge_base` com observabilidade de indexacao, ranking textual mais seguro, estatisticas por base e fundacao para embeddings opcionais por tenant.

## Endpoints novos

- `GET /api/v1/knowledge-base/indexing-jobs/`
- `GET /api/v1/knowledge-base/indexing-jobs/{id}/`
- `GET /api/v1/knowledge-base/{id}/stats/`
- `POST /api/v1/knowledge-base/{id}/reindex-document/`

## Endpoints melhorados

- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`

## Modelos novos

- `IndexingJob`
- `ChunkEmbedding`

## Modelos alterados

- `DocumentChunk`
- `RetrievalQuery`

## Cobertura principal

- `IndexingJob` em sucesso e erro controlado
- ranking por frase exata, relevancia e limite
- `ask` com `retrieval_method`, `sources_count` e `confidence`
- `stats` por base sem mistura entre tenants
- `reindex-document` com `chunks_deleted` e `chunks_created`
- fundacao de embeddings opcionais com validacao por tenant

## Limitacoes atuais

- ainda sem embeddings reais
- ainda sem banco vetorial
- ainda sem provider externo
- ainda sem OCR integrado
- ranking textual continua local e heuristico

## Proximo passo recomendado

Implementar uma fase 3 opcional com embeddings por tenant e estrategia de recuperacao hibrida, mantendo fontes obrigatorias, configuracao explicita por organizacao e nenhum envio externo por defeito.
