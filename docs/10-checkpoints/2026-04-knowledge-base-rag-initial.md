# Checkpoint — Knowledge Base / RAG inicial

## Objetivo

Tornar o app `knowledge_base` funcional sem dependencias externas, com indexacao textual por tenant, recuperacao segura e respostas fundamentadas em fontes explicitas.

## Endpoints

- `GET/POST /api/v1/knowledge-base/`
- `GET/POST /api/v1/knowledge-base/documents/`
- `POST /api/v1/knowledge-base/{id}/index-document/`
- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `GET /api/v1/knowledge-base/queries/`

## Escopo entregue

- bases de conhecimento por `organization`
- indexacao de `Document` em chunks textuais
- busca textual local sem provider externo
- resposta fundamentada com `sources`
- historico de consultas em `RetrievalQuery`
- bloqueio cross-tenant por filtros e validacao de relacoes

## Limitacoes atuais

- sem embeddings externos
- sem banco vetorial
- sem reranking por LLM
- sem OCR integrado
- sem parse binario profundo de documentos
- ranking textual inicial simples por ocorrencias de termos

## Testes

- Suite focal: [tests/test_knowledge_base.py](/c:/projectos/JurisAI/tests/test_knowledge_base.py)
- Coberturas principais:
  - criacao por tenant
  - indexacao de documento proprio
  - bloqueio de documento de outro tenant
  - criacao de chunks
  - busca sem mistura entre tenants
  - `ask` com fontes
  - `ask` com `no_sources`

## Proximo passo recomendado

Adicionar uma segunda fase de recuperacao com embeddings opcionais, mantendo isolamento por `organization`, observabilidade do processo de indexacao e citacoes obrigatorias nas respostas.
