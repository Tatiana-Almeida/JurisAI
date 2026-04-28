---
name: route-api-documentation
description: Documentar a API real a partir de rotas, views, controllers, decorators, validações, permissões e tratamento de erros. Use quando for preciso descrever endpoints existentes sem mudar o contrato da API.
---

# Objetivo da skill

Extrair e documentar a API implementada de fato, incluindo autenticação, autorização, payloads, respostas e erros.

## Quando usar

- Quando houver necessidade de documentar endpoints existentes.
- Quando a API estiver parcialmente documentada ou divergente do código.
- Quando for preciso gerar documentação em `docs/01-api/`.

## Quando não usar

- Quando a tarefa for criar endpoints novos.
- Quando a análise principal for de banco, arquitetura ou segurança ampla.

## Entradas esperadas

- Arquivos de rotas, controllers/views, serializers/DTOs e exceptions.
- Middlewares, decorators, guards, permissions e policies.

## Processo passo a passo

1. Localizar todos os registradores de rotas e routers.
2. Mapear cada endpoint com método HTTP, path, handler e módulo.
3. Ler autenticação, permissões, decorators e validações aplicadas.
4. Extrair formatos de request, response, paginação e filtros.
5. Catalogar erros conhecidos a partir de exceptions, responses e status codes.
6. Gerar:
   - `docs/01-api/api-overview.md`
   - `docs/01-api/endpoints.md`
   - `docs/01-api/authentication.md`
   - `docs/01-api/error-catalog.md`
   - `docs/01-api/request-response-examples.md`
7. Atribuir identificadores `API-001`, `API-002`, etc.

## Ficheiros e pastas que deve analisar

- `urls.*`, routers, route registries
- Controllers, views, handlers
- DTOs, serializers, schemas, validators
- Permissions, guards, policies, decorators
- Middlewares relacionados a request/response
- Exception handlers e classes de erro

## Documentos que deve gerar

- `docs/01-api/api-overview.md`
- `docs/01-api/endpoints.md`
- `docs/01-api/authentication.md`
- `docs/01-api/error-catalog.md`
- `docs/01-api/request-response-examples.md`

## Regras de segurança

- Nunca remover ou alterar endpoints nesta fase.
- Nunca presumir proteção que não esteja explícita no código.
- Destacar endpoints públicos e exposição de dados sensíveis.

## Regras de qualidade

- Documentar apenas comportamento real observado.
- Separar autenticação de autorização.
- Indicar filtros, ordenação, paginação e formatos de erro quando existirem.
- Marcar exemplos como confirmados ou inferidos.

## Formato de saída

- Markdown em `docs/01-api/`
- Tabelas com colunas mínimas:
  - ID
  - Método
  - Rota
  - Handler
  - Autenticação
  - Permissões
  - Observações

## Exemplos de documentação

- Catálogo de endpoints `API-001`.
- Fluxo de login e refresh token.
- Catálogo de erros por status HTTP e origem no código.
- Exemplos de request/response baseados em serializers e testes.

## Critérios de validação

- Todas as rotas encontradas no código foram listadas ou marcadas como `[PRECISA_VALIDAR]`.
- Autenticação e permissões foram descritas por endpoint ou grupo.
- Há um catálogo de erros coerente com o tratamento real.
- Os exemplos não contradizem serializers nem responses do código.

