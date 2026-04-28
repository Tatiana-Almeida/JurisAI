---
name: documentation-review
description: Revisar a documentação gerada a partir do backend e encontrar inconsistências entre código, endpoints, requisitos, regras, entidades, testes e melhorias. Use quando for preciso validar qualidade e coerência da documentação.
---

# Objetivo da skill

Auditar a documentação produzida para detectar lacunas, contradições e afirmações sem evidência.

## Quando usar

- Quando já houver documentação gerada em `docs/`.
- Quando a equipa quiser validar consistência antes de seguir com melhorias.
- Quando for necessário gerar `docs/11-review/documentation-review-report.md`.

## Quando não usar

- Quando ainda não existe documentação suficiente para revisar.
- Quando a tarefa for apenas criar documentação inicial.

## Entradas esperadas

- Documentação em `docs/`
- Código-fonte atual
- Testes e rastreabilidade disponíveis

## Processo passo a passo

1. Relistar endpoints, entidades, requisitos, regras, testes e melhorias a partir do código e da docs.
2. Procurar:
   - endpoint existente mas não documentado
   - endpoint documentado mas não encontrado no código
   - requisito sem evidência
   - regra sem origem
   - entidade sem uso
   - teste recomendado sem requisito
   - melhoria sem risco classificado
   - documentação desatualizada
   - inferência marcada como certeza
3. Registrar achados com severidade e evidência.
4. Gerar `docs/11-review/documentation-review-report.md`.

## Ficheiros e pastas que deve analisar

- Todos os documentos em `docs/`
- Rotas, views, services, entities, tests
- Matriz de rastreabilidade quando existir

## Documentos que deve gerar

- `docs/11-review/documentation-review-report.md`

## Regras de segurança

- Não “corrigir” o código durante a revisão documental.
- Não promover inferência a fato.
- Apontar quando a documentação recomenda mudança de alto risco sem validação humana.

## Regras de qualidade

- Tratar a revisão como auditoria, não como resumo.
- Priorizar inconsistências com maior impacto operacional ou de segurança.
- Citar origem do problema e documento afetado.

## Formato de saída

- Markdown com seções:
  - Achados
  - Severidade
  - Evidência
  - Documento afetado
  - Recomendação

## Exemplos de documentação

- Endpoint documentado mas ausente na rota real.
- Requisito sem evidência no código.
- Regra inferida apresentada como confirmada.

## Critérios de validação

- O relatório cobre código e documentação.
- Achados possuem evidência clara.
- Há separação entre inconsistência confirmada e suspeita.
- O relatório é acionável para manutenção da docs.

