---
name: traceability-from-code
description: Criar uma matriz de rastreabilidade entre código, endpoints, requisitos, regras, entidades, testes e melhorias propostas. Use quando for preciso ligar a documentação ao backend real e apoiar mudanças seguras.
---

# Objetivo da skill

Conectar artefatos técnicos e documentais para facilitar impacto, auditoria e priorização de melhorias.

## Quando usar

- Quando já existe documentação parcial gerada pelas outras skills.
- Quando for preciso entender impacto de mudança.
- Quando for necessário gerar `docs/10-traceability/traceability-matrix.md`.

## Quando não usar

- Quando ainda não há base mínima de descoberta, API, regras ou requisitos.
- Quando a tarefa for somente explorar o projeto pela primeira vez.

## Entradas esperadas

- Código do backend
- Documentação gerada em `docs/`
- Testes existentes e recomendados

## Processo passo a passo

1. Reunir evidências de código, endpoints, entidades, requisitos, regras, testes e melhorias.
2. Normalizar identificadores:
   - `API-xxx`
   - `RF-xxx`
   - `RN-xxx`
   - `ENT-xxx`
   - `CT-xxx`
   - `REF-xxx`
3. Criar matriz com estado de cobertura e consistência.
4. Gerar `docs/10-traceability/traceability-matrix.md`.
5. Apontar linhas órfãs ou inconsistentes com `[PRECISA_VALIDAR]`.

## Ficheiros e pastas que deve analisar

- Código relevante por módulo
- Documentos em `docs/01-*` até `docs/09-*`
- Testes existentes

## Documentos que deve gerar

- `docs/10-traceability/traceability-matrix.md`

## Regras de segurança

- Não inventar rastreabilidade sem evidência.
- Quando o vínculo for apenas provável, marcar como inferido.

## Regras de qualidade

- Manter a matriz simples, útil e atualizável.
- Preferir granularidade por unidade funcional clara.
- Destacar itens sem teste ou sem requisito.

## Formato de saída

- Markdown com a tabela obrigatória:
  `| Código | Endpoint | Requisito | Regra | Entidade | Teste | Estado |`

## Exemplos de documentação

- Linha que liga serializer, endpoint, regra de negócio e teste.
- Linha que mostra endpoint sem teste.
- Linha que mostra requisito sem evidência suficiente.

## Critérios de validação

- A matriz foi gerada no formato pedido.
- Há vínculo entre código e artefatos documentais.
- Itens órfãos ou pendentes foram marcados.
- O estado de cada linha é explícito.

