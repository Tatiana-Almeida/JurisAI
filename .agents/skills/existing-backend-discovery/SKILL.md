---
name: existing-backend-discovery
description: Analisar um backend já existente para mapear estrutura, stack, pontos de entrada, módulos, configuração e dependências. Use quando for preciso entender o projeto antes de documentar, auditar ou propor melhorias seguras.
---

# Objetivo da skill

Mapear o backend existente sem alterar seu comportamento, produzindo uma visão geral confiável do projeto.

## Quando usar

- Quando o backend já existe e precisa ser entendido antes de qualquer mudança.
- Quando for necessário gerar documentação base em `docs/00-code-discovery/`.
- Quando houver dúvida sobre stack, entrypoints, módulos, scripts ou variáveis de ambiente.

## Quando não usar

- Quando a tarefa principal já for documentar rotas, banco, segurança ou testes de forma aprofundada.
- Quando o objetivo for implementar funcionalidade nova sem fase de descoberta.

## Entradas esperadas

- Código-fonte do backend.
- Arquivos de configuração e dependências.
- Scripts de execução local, CI ou container.

## Processo passo a passo

1. Ler a raiz do projeto e identificar linguagem, framework e convenções.
2. Localizar entrypoints, módulos, middlewares, serviços, controllers, entidades e migrações.
3. Ler arquivos de dependências, Docker, scripts e settings.
4. Identificar variáveis de ambiente esperadas, diferenciando confirmadas e inferidas.
5. Registrar descobertas usando as marcações obrigatórias.
6. Gerar os documentos:
   - `docs/00-code-discovery/backend-overview.md`
   - `docs/00-code-discovery/project-structure.md`
   - `docs/00-code-discovery/technology-stack.md`
   - `docs/00-code-discovery/runtime-and-scripts.md`
7. Destacar lacunas com `[NÃO_ENCONTRADO]` ou `[PRECISA_VALIDAR]`.

## Ficheiros e pastas que deve analisar

- Raiz do projeto
- `README*`
- `requirements*`, `pyproject*`, `package*`, `Pipfile*`, `Dockerfile*`, `docker-compose*`
- Arquivos de config do framework
- Pastas de apps, módulos, controllers, services, models, repositories, middlewares
- `migrations/`
- `manage.py`, `main.*`, `app.*`, `wsgi.*`, `asgi.*`
- Scripts de setup, seed, test e build

## Documentos que deve gerar

- `docs/00-code-discovery/backend-overview.md`
- `docs/00-code-discovery/project-structure.md`
- `docs/00-code-discovery/technology-stack.md`
- `docs/00-code-discovery/runtime-and-scripts.md`

## Regras de segurança

- Nunca apagar ou reescrever código existente.
- Nunca alterar comportamento funcional nesta etapa.
- Nunca assumir secrets; documentar apenas variáveis esperadas e locais de leitura.
- Marcar claramente inferências e lacunas.

## Regras de qualidade

- Separar fatos observados de inferências.
- Citar arquivos e caminhos relevantes.
- Preferir tabelas e listas curtas para stack, módulos e scripts.
- Não inventar camadas que não existam no código.

## Formato de saída

- Markdown em `docs/00-code-discovery/`
- Usar identificadores quando aplicável:
  - `ADR-001` para decisões arquiteturais observadas
  - `RNF-001` para aspectos não funcionais confirmados
- Incluir seções de “Evidências no código” e “Pontos a validar”.

## Exemplos de documentação

- Visão geral do backend com stack, módulos e entrypoints.
- Estrutura de pastas com responsabilidade de cada diretório.
- Tabela de dependências e finalidade operacional.
- Lista de scripts com comando, objetivo e pré-condições.

## Critérios de validação

- Os quatro documentos foram criados.
- Linguagem, framework, entrypoint e dependências foram documentados.
- Variáveis de ambiente esperadas foram listadas com origem no código.
- Cada afirmação importante está marcada como confirmada, inferida ou pendente.

