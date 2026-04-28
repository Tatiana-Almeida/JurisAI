---
name: business-rules-from-code
description: Extrair regras de negócio escondidas em services, controllers, validações, middlewares, jobs e condições de código. Use quando for preciso transformar comportamento implícito em regras documentadas.
---

# Objetivo da skill

Descobrir e documentar regras de negócio embutidas no código, especialmente as que não estão descritas em requisitos formais.

## Quando usar

- Quando o backend possui lógica relevante espalhada em várias camadas.
- Quando for necessário gerar `docs/03-business-rules/business-rules-from-code.md`.
- Quando a equipa precisar entender regras antes de mexer no comportamento.

## Quando não usar

- Quando a tarefa for apenas mapear rotas ou banco.
- Quando ainda não houve descoberta mínima da estrutura do projeto.

## Entradas esperadas

- Services, views/controllers, serializers, validators, middlewares, guards, helpers, jobs, tasks, signals

## Processo passo a passo

1. Localizar pontos com `if/else`, validações, limitações, transições de estado e regras de permissão.
2. Extrair regras explícitas e implícitas.
3. Dar um identificador `RN-001`, `RN-002`, etc.
4. Para cada regra, registrar:
   - descrição
   - origem no código
   - trigger
   - impacto
   - entidades afetadas
   - status da evidência
5. Consolidar tudo em `docs/03-business-rules/business-rules-from-code.md`.

## Ficheiros e pastas que deve analisar

- Services
- Controllers/views
- Validators/serializers
- Middlewares, guards, permissions, policies
- Helpers e utils
- Jobs, tasks, signals
- Código de pagamento, cancelamento, cálculo, aprovação e estados

## Documentos que deve gerar

- `docs/03-business-rules/business-rules-from-code.md`

## Regras de segurança

- Não alterar regras nesta etapa.
- Não tratar inferência como regra confirmada.
- Destacar regras que afetam autenticação, autorização, cobrança e isolamento de tenant.

## Regras de qualidade

- Uma regra por bloco identificável.
- Evitar linguagem vaga; descrever condição e efeito.
- Distinguir regra de negócio de detalhe técnico.

## Formato de saída

- Markdown com tabela ou blocos por `RN-xxx`
- Campos recomendados:
  - ID
  - Regra
  - Evidência
  - Local no código
  - Impacto
  - Observações

## Exemplos de documentação

- Limite de usuários por plano.
- Regra de criação de casos por organização.
- Regra de quota mensal de IA.
- Regra de acesso por papel.

## Critérios de validação

- Regras importantes foram extraídas das camadas certas.
- Cada regra tem origem no código.
- Regras confirmadas e inferidas estão separadas.
- Há cobertura para estados, permissões e limites relevantes.

