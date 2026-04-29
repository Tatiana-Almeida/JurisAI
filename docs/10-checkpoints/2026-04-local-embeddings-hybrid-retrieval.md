# Checkpoint — Local Embeddings and Hybrid Retrieval

## Objetivo

Adicionar uma fundacao local de embeddings ao `knowledge_base` para permitir retrieval por similaridade e modo hibrido, sem internet, sem provider externo real e sem quebrar o fallback textual por tenant.

## Provider local

- `provider`: `local`
- `model`: `local-hash-v1`
- deterministico
- totalmente local
- sem envio de conteudo para terceiros
- adequado para validar pipeline e governanca, mas nao equivale a embedding semantico real

## Endpoints impactados

- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`
- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `GET/PATCH /api/v1/knowledge-base/settings/`
- `GET /api/v1/knowledge-base/embedding-audit-logs/`

## Retrieval method

O `ask` e a busca do `knowledge_base` agora podem expor:

- `retrieval_method="textual"`
- `retrieval_method="local_embedding"`
- `retrieval_method="hybrid"`
- `retrieval_method="textual_fallback"`

As fontes continuam obrigatorias e agora podem incluir:

- `final_score`
- `text_score`
- `embedding_score`

## Testes

- `tests/test_knowledge_base.py`: `41 passed`

Cobertura principal:

- configuracao segura do provider local
- opt-in externo preservado
- geracao local de `ChunkEmbedding`
- nao duplicacao de embeddings existentes
- placeholder externo como `skipped`
- retrieval `local_embedding`
- retrieval `hybrid`
- fallback textual quando embeddings nao existem
- tenant isolation preservado em prepare, busca e ask

## Limitacoes

- `local-hash-v1` nao e embedding semantico real
- ainda nao existe banco vetorial
- providers externos continuam sem implementacao real
- `ChunkEmbedding` continua simples, com um embedding por chunk
- OCR ainda nao participa do pipeline de indexacao

## Proximos passos

- avaliar embeddings locais semanticamente mais fortes sem internet
- preparar ranking hibrido com sinais adicionais de documento e recencia
- definir estrategia opcional para banco vetorial local ou persistencia otimizada
- manter opt-in e auditoria antes de qualquer provider externo futuro
