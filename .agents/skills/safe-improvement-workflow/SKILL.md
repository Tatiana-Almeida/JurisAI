---
name: safe-improvement-workflow
description: Guiar melhorias seguras em um backend existente seguindo análise, documentação, classificação de risco, implementação mínima e atualização de docs. Use quando a tarefa envolver mudar código sem perder rastreabilidade.
---

# Objetivo da skill

Garantir que qualquer melhoria no backend siga um fluxo seguro, incremental e documentado.

## Quando usar

- Quando a tarefa envolver modificar código existente.
- Quando for necessário gerar ou atualizar `docs/09-improvements/`.
- Quando houver risco de alterar comportamento sem documentação prévia.

## Quando não usar

- Quando a tarefa for apenas análise sem mudança de código.
- Quando a alteração for proibida ou ainda carecer de validação humana.

## Entradas esperadas

- Problema a resolver
- Código relevante
- Documentação existente
- Testes disponíveis

## Processo passo a passo

1. Ler o código.
2. Documentar comportamento atual.
3. Identificar problema.
4. Classificar risco em baixo, médio ou alto.
5. Propor melhoria.
6. Criar plano de alteração.
7. Alterar apenas arquivos necessários.
8. Rodar testes, lint e build quando disponíveis.
9. Atualizar documentação.
10. Explicar o que mudou.

## Ficheiros e pastas que deve analisar

- Arquivos diretamente impactados pela mudança
- Testes relacionados
- Documentos em `docs/` que ficarão desatualizados

## Documentos que deve gerar

- `docs/09-improvements/improvement-plan.md` quando solicitado
- `docs/09-improvements/change-log.md` quando houver alteração implementada

## Regras de segurança

- Nunca implementar alteração de alto risco sem validação humana.
- Nunca alterar autenticação/autorização sem análise e aprovação.
- Nunca mudar schema sem plano de migração.
- Nunca mudar contrato de API sem documentar impacto.

## Regras de qualidade

- Fazer mudanças pequenas e reversíveis.
- Preservar comportamento atual até que a mudança esteja documentada.
- Atualizar a rastreabilidade e documentação relacionadas.

## Formato de saída

- Plano com:
  - problema
  - comportamento atual
  - proposta
  - risco
  - arquivos afetados
  - validação
- Change log com resumo do que mudou e documentos atualizados

## Exemplos de documentação

- Plano para corrigir validação multi-tenant.
- Registro de mudança segura em webhook.
- Checklist de validação pós-alteração.

## Critérios de validação

- O fluxo de 10 passos foi seguido.
- O risco foi classificado.
- Houve atualização documental quando código mudou.
- Testes/lint/build foram rodados ou a limitação foi registrada.

