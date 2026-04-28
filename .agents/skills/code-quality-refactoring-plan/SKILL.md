---
name: code-quality-refactoring-plan
description: Avaliar qualidade do código e criar um plano de refatoração seguro, incremental e rastreável. Use quando for preciso melhorar manutenibilidade sem reescrever o backend inteiro.
---

# Objetivo da skill

Produzir um diagnóstico de qualidade e um plano de refatoração com baixo risco e alto valor incremental.

## Quando usar

- Quando o backend já funciona, mas há sinais de dívida técnica.
- Quando for necessário gerar `docs/07-quality/`.
- Quando a equipa quiser priorizar melhorias sem quebrar comportamento.

## Quando não usar

- Quando o pedido for corrigir um bug pontual sem análise mais ampla.
- Quando a intenção for reescrever o projeto do zero.

## Entradas esperadas

- Código-fonte
- Testes existentes
- Configurações e scripts operacionais

## Processo passo a passo

1. Mapear duplicações, acoplamentos, complexidade e distribuição de responsabilidades.
2. Identificar controllers/views com regra de negócio e services grandes.
3. Verificar tratamento de erro, logs, queries repetidas, dependências desnecessárias e código morto.
4. Classificar oportunidades com `REF-001` e risco baixo, médio ou alto.
5. Gerar:
   - `docs/07-quality/refactoring-plan.md`
   - `docs/07-quality/technical-debt.md`
6. Relacionar cada proposta com evidência e testes necessários.

## Ficheiros e pastas que deve analisar

- Views/controllers
- Services
- Models/entities
- Serializers/validators
- Tasks/jobs
- Configurações e dependências
- Testes existentes

## Documentos que deve gerar

- `docs/07-quality/refactoring-plan.md`
- `docs/07-quality/technical-debt.md`

## Regras de segurança

- Nunca propor refatoração grande sem classificação de risco.
- Alterações de alto risco exigem validação humana.
- Não mudar contrato funcional sem documentação prévia do comportamento atual.

## Regras de qualidade

- Priorizar refatorações incrementais.
- Distinguir problema estrutural de preferência de estilo.
- Relacionar cada melhoria a benefícios concretos.

## Formato de saída

- Markdown com seções:
  - Dívida técnica
  - Propostas
  - Risco
  - Dependências
  - Testes necessários

## Exemplos de documentação

- `REF-001`: centralizar validação multi-tenant.
- `REF-002`: separar lógica de webhook em service dedicado.
- `REF-003`: reduzir duplicação de filtros por organização.

## Critérios de validação

- Há diagnóstico e plano, não apenas opinião.
- Cada proposta possui evidência, risco e impacto.
- O plano evita reescrita ampla.
- A recomendação de testes acompanha mudanças mais sensíveis.

