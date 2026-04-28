# AGENTS.md

Este projeto contém um backend já existente.

O objetivo principal do Codex neste repositório é:
1. Entender o backend atual.
2. Criar documentação em volta do código existente.
3. Extrair requisitos, regras de negócio, endpoints, entidades e arquitetura a partir do código.
4. Identificar problemas técnicos, falhas de segurança e oportunidades de melhoria.
5. Propor melhorias seguras sem apagar nem reescrever o projeto.

## Regras obrigatórias

- Não apagar código existente sem autorização explícita.
- Não reescrever o backend inteiro.
- Não substituir a arquitetura atual sem análise e validação.
- Não alterar comportamento funcional sem antes documentar o comportamento atual.
- Não alterar schema de banco de dados sem plano de migração.
- Não alterar autenticação/autorização sem validação humana.
- Não remover endpoints existentes sem autorização.
- Não mudar contratos de API sem documentar impacto.

## Processo padrão

Antes de qualquer melhoria no código:

1. Analisar o código existente.
2. Identificar os arquivos envolvidos.
3. Documentar o comportamento atual.
4. Criar ou atualizar documentação em `docs/`.
5. Propor melhoria.
6. Classificar risco:
   - baixo
   - médio
   - alto
7. Implementar apenas se for seguro ou se houver autorização.
8. Rodar testes, lint ou build quando disponíveis.
9. Atualizar documentação depois da alteração.

## Marcação de informação

Usar sempre:

- [CONFIRMADO_NO_CÓDIGO]
- [INFERIDO_DO_CÓDIGO]
- [PRECISA_VALIDAR]
- [NÃO_ENCONTRADO]

## Skills

Sempre que a tarefa envolver documentação, auditoria, análise ou melhoria do backend, verificar as skills em:

`.agents/skills/`

Skills principais:

- existing-backend-discovery
- route-api-documentation
- database-schema-reverse-engineering
- business-rules-from-code
- requirements-from-existing-backend
- architecture-from-existing-code
- security-audit-backend
- code-quality-refactoring-plan
- test-coverage-analysis
- safe-improvement-workflow
- traceability-from-code
- documentation-review

## Regras globais das skills

- Primeiro analisar o código.
- Depois documentar o comportamento atual.
- Depois propor melhorias.
- Só depois implementar alterações pequenas e seguras, se for solicitado.
- Separar sempre informação confirmada de informação inferida.
- Criar documentação em Markdown dentro da pasta `docs/`.
- Usar identificadores padronizados:
  - `RF-001` para requisitos funcionais
  - `RNF-001` para requisitos não funcionais
  - `RN-001` para regras de negócio
  - `API-001` para endpoints
  - `ENT-001` para entidades
  - `SEC-001` para riscos de segurança
  - `REF-001` para propostas de refatoração
  - `CT-001` para casos de teste
  - `ADR-001` para decisões arquiteturais
- Criar rastreabilidade entre código, endpoints, requisitos, regras de negócio, entidades, testes e melhorias propostas.
- Classificar melhorias por risco: baixo, médio, alto.
- Alterações de alto risco exigem validação humana antes da implementação.
- Sempre que modificar código, atualizar a documentação relacionada.
- Sempre que possível, rodar testes, lint e build antes de concluir.
- Se não existirem testes, recomendar testes antes de grandes refatorações.

