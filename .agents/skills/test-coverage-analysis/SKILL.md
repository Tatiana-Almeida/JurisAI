---
name: test-coverage-analysis
description: Analisar testes existentes, lacunas de cobertura e casos recomendados para um backend já implementado. Use quando for preciso decidir onde testar antes de refatorar ou corrigir riscos.
---

# Objetivo da skill

Entender o nível real de confiança do projeto e recomendar testes faltantes com prioridade e rastreabilidade.

## Quando usar

- Quando há refatorações planejadas ou riscos identificados.
- Quando a equipa quer saber o que já é testado e o que está descoberto.
- Quando for preciso gerar `docs/08-tests/`.

## Quando não usar

- Quando a tarefa for criar diretamente uma suíte de testes sem fase analítica.
- Quando o backend ainda não foi minimamente mapeado.

## Entradas esperadas

- Arquivos de teste
- Configuração de test runner
- Código de endpoints, serviços e regras

## Processo passo a passo

1. Localizar testes unitários, integração e e2e.
2. Mapear o que cada teste cobre.
3. Comparar cobertura observada com endpoints, regras, permissões e integrações.
4. Criar casos recomendados com IDs `CT-001`, `CT-002`, etc.
5. Gerar:
   - `docs/08-tests/test-coverage-analysis.md`
   - `docs/08-tests/recommended-test-cases.md`
6. Indicar risco de cada lacuna de cobertura.

## Ficheiros e pastas que deve analisar

- `tests/`, `test_*`, `*_test*`
- Configuração de pytest ou outro runner
- Endpoints e services críticos
- Regras de negócio, auth e permissions

## Documentos que deve gerar

- `docs/08-tests/test-coverage-analysis.md`
- `docs/08-tests/recommended-test-cases.md`

## Regras de segurança

- Não assumir cobertura real sem evidência em testes executáveis.
- Se não for possível rodar testes, registrar a limitação explicitamente.

## Regras de qualidade

- Diferenciar “tem teste” de “tem teste suficiente”.
- Priorizar gaps em segurança, tenant isolation, billing e regras críticas.
- Relacionar casos de teste recomendados a requisitos e riscos.

## Formato de saída

- Markdown com tabelas por área:
  - Área
  - Cobertura atual
  - Lacuna
  - Risco
  - Testes recomendados

## Exemplos de documentação

- Cobertura atual de JWT e perfil.
- Falta de testes de webhook, tasks e auditoria.
- `CT-001`: impedir criação cross-tenant por foreign key.

## Critérios de validação

- Testes existentes foram identificados por tipo.
- Endpoints e regras sem teste foram listados.
- Há recomendação priorizada de novos testes.
- Limitações de execução foram documentadas quando existirem.
