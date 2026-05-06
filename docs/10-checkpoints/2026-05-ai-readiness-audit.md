# Checkpoint - AI Readiness Audit

## Objetivo

Avaliar o estado real dos fluxos de IA do JurisAI e distinguir o que esta implementado, parcial, mock ou ausente.

## Classificacao por fluxo

- Ask com fontes: implemented
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/knowledge-base/{id}/ask/` existe em `knowledge_base/urls.py`.
  - [CONFIRMADO_NO_CODIGO] O resultado inclui `sources`, `confidence`, `retrieval_method`, `effective_retrieval_mode`, `fallback_used` e `fallback_reason`.
  - [CONFIRMADO_NO_CODIGO] Ha cobertura extensa em `tests/test_knowledge_base.py`.

- Resumo de documento: partial
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/ai/summarize-document/` existe em `ai_assistant/urls.py`.
  - [CONFIRMADO_NO_CODIGO] O endpoint delega para `AIService.resumir_documento(...)`.
  - [PRECISA_VALIDAR] Nao foi encontrada suite dedicada que prove comportamento funcional real com provider configurado.

- Revisao de contrato/documento: partial
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/ai/review-document/` existe.
  - [CONFIRMADO_NO_CODIGO] O output atual e apenas `{'review': text}` vindo de um prompt generico.
  - [INFERIDO_DO_CODIGO] Ainda nao ha sinais de rubricacao juridica estruturada, score, anotacoes por clausula ou fluxo comercial completo.

- Geracao de contrato: partial
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/ai/draft-contract/` existe.
  - [CONFIRMADO_NO_CODIGO] O service usa prompt generico e devolve texto livre.
  - [INFERIDO_DO_CODIGO] Ainda nao ha pipeline de validacao juridica, template engine controlada ou montagem de clausulas por dominio.

- Analise de risco: partial
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/ai/analyze-risk/` existe.
  - [CONFIRMADO_NO_CODIGO] O retorno atual e `{'risk_analysis': text}`.
  - [INFERIDO_DO_CODIGO] Ainda nao ha modelo de scoring estruturado, explicabilidade juridica forte ou validacao comercial.

- Minuta juridica / peticao: partial
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/ai/generate-petition/` existe.
  - [CONFIRMADO_NO_CODIGO] O endpoint usa prompt generico em `AIService.gerar_peticao(...)`.
  - [INFERIDO_DO_CODIGO] Ainda nao ha biblioteca de tipos de minuta, referencias normativas ou validacao por area do direito.

- Pesquisa de jurisprudencia: partial
  - [CONFIRMADO_NO_CODIGO] `POST /api/v1/ai/search-jurisprudence/` existe.
  - [CONFIRMADO_NO_CODIGO] O retorno atual e `{'search_results': text}`.
  - [NAO_ENCONTRADO] Nao foi encontrado conector real para base juridica externa ou indice proprio de jurisprudencia.

## Provider externo

- OpenAI provider path: partial
  - [CONFIRMADO_NO_CODIGO] `ai_assistant/services/ai_service.py` tenta usar `openai.ChatCompletion.create(...)` quando `OPENAI_API_KEY` e SDK estao disponiveis.
  - [CONFIRMADO_NO_CODIGO] Quando isso nao ocorre, o service devolve `Resposta de mock: chave OpenAI nao configurada.`
  - [CONFIRMADO_NO_CODIGO] O fluxo grava `AIRequest` por organizacao para quota e historico.

## Modo local/mock

- AI mock fallback: implemented
  - [CONFIRMADO_NO_CODIGO] O fallback mock esta embutido no `AIService`.
- RAG local foundation: implemented
  - [CONFIRMADO_NO_CODIGO] `local-hash-v1` gera embeddings locais deterministas sem envio de dados para fora do backend.

## Limitacoes do `local-hash-v1`

- [CONFIRMADO_NO_CODIGO] `local-hash-v1` serve para validar pipeline, persistencia de embeddings, retrieval local e fallback controlado.
- [CONFIRMADO_NO_CODIGO] Ele nao e um embedding semantico real.
- [INFERIDO_DO_CODIGO] Documentos juridicamente equivalentes com vocabulario diferente podem nao ser bem aproximados por esse modelo.
- [INFERIDO_DO_CODIGO] A evolucao comercial natural seria embeddings locais mais semanticos ou provider externo com opt-in por tenant e governanca forte.

## Decisao

- [CONFIRMADO_NO_CODIGO] O JurisAI ja possui uma fundacao de IA demonstravel.
- [CONFIRMADO_NO_CODIGO] Os fluxos de IA comercial ainda sao parciais.
- [CONFIRMADO_NO_CODIGO] O valor mais maduro hoje esta em RAG com fontes e OCR governado, nao em automacao juridica premium pronta para venda.
