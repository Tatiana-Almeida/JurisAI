---
name: architecture-from-existing-code
description: Documentar a arquitetura real do backend a partir do código, módulos, integrações, jobs e fluxos de execução. Use quando for preciso registrar a arquitetura atual antes de discutir mudanças maiores.
---

# Objetivo da skill

Descrever a arquitetura realmente implementada, suas camadas, dependências, decisões e integrações.

## Quando usar

- Quando a equipa precisa de uma visão arquitetural baseada em evidência.
- Quando for necessário gerar `docs/05-architecture/`.
- Quando houver risco de propostas de reescrita sem entendimento do sistema atual.

## Quando não usar

- Quando a tarefa for apenas documentar endpoints ou entidades.
- Quando não houver tempo para leitura transversal do backend.

## Entradas esperadas

- Estrutura de módulos
- Configurações principais
- Código de autenticação, filas, storage, logs, cache, erros e integrações

## Processo passo a passo

1. Identificar o padrão arquitetural dominante e suas exceções.
2. Mapear módulos, dependências internas e fluxos principais.
3. Registrar mecanismos de autenticação, autorização, jobs, eventos, filas, cache, storage e observabilidade.
4. Identificar decisões arquiteturais já visíveis no código.
5. Gerar:
   - `docs/05-architecture/current-architecture.md`
   - `docs/05-architecture/modules.md`
   - `docs/05-architecture/dependencies.md`
   - `docs/05-architecture/integrations.md`
   - `docs/05-architecture/architecture-decisions.md`
   - `docs/05-architecture/decisions/ADR-001-current-architecture.md`

## Ficheiros e pastas que deve analisar

- Configuração do framework
- Módulos/apps
- Services e tarefas assíncronas
- Integrações externas
- Middleware, permissions, exception handler
- Docker, compose e scripts de runtime

## Documentos que deve gerar

- `docs/05-architecture/current-architecture.md`
- `docs/05-architecture/modules.md`
- `docs/05-architecture/dependencies.md`
- `docs/05-architecture/integrations.md`
- `docs/05-architecture/architecture-decisions.md`
- `docs/05-architecture/decisions/ADR-001-current-architecture.md`

## Regras de segurança

- Não propor troca de arquitetura como fato consumado.
- Diferenciar arquitetura atual de melhorias desejáveis.
- Marcar integrações críticas e pontos únicos de falha.

## Regras de qualidade

- Descrever a arquitetura real, não a ideal.
- Evitar jargão sem evidência prática no código.
- Explicitar acoplamentos, boundaries e dependências externas.

## Formato de saída

- Markdown com diagramas textuais quando útil
- Tabelas de módulos e integrações
- ADR inicial com contexto, decisão observada e consequências

## Exemplos de documentação

- Mapa de apps e suas responsabilidades.
- Dependências entre módulos de domínio e infraestrutura.
- Fluxo request -> permission -> serializer -> model -> task.
- ADR do monólito modular atual.

## Critérios de validação

- Os documentos de arquitetura foram gerados.
- Há descrição de módulos, integrações e decisões observadas.
- O ADR reflete o estado atual do código.
- Afirmações arquiteturais possuem evidência ou marcação de inferência.

