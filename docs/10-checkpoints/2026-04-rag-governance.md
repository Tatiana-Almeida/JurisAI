# Checkpoint — RAG governance

## Objetivo

Adicionar governanca por `organization` ao `knowledge_base`, preparando embeddings futuros com opt-in explicito, auditabilidade e fallback textual obrigatorio.

## Modelos adicionados

- `RAGSettings`
- `EmbeddingAuditLog`

## Endpoints adicionados

- `GET/PATCH /api/v1/knowledge-base/settings/`
- `GET /api/v1/knowledge-base/embedding-audit-logs/`
- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`

## Regras de seguranca

- provider externo continua desativado por defeito
- nenhum documento sai do sistema nesta fase
- `external_embeddings_enabled=True` exige opt-in explicito para envio de conteudo
- `ask` continua com `sources` obrigatorias
- fallback textual continua obrigatorio quando embeddings nao estao efetivos
- logs de embeddings nao armazenam conteudo bruto do documento

## Testes executados

- `tests/test_knowledge_base.py`
- suite completa

## Limitacoes

- sem embeddings reais
- sem provider externo
- sem banco vetorial
- sem fluxo de consentimento juridico mais profundo por tenant

## Proximos passos

Implementar uma fase futura de embeddings opcionais por tenant com integracao desativada por defeito, observabilidade completa, consentimento explicito e citacoes obrigatorias nas respostas.
