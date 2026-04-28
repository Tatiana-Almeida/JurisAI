---
name: database-schema-reverse-engineering
description: Documentar o esquema de banco a partir de models, entities, migrations, ORM e constraints existentes. Use quando for preciso entender a estrutura real de dados sem alterar o schema atual.
---

# Objetivo da skill

Reconstruir o esquema de dados a partir do código e documentar entidades, campos, relacionamentos, constraints e migrações.

## Quando usar

- Quando o banco precisa ser documentado a partir do backend.
- Quando for necessário entender entidades e relacionamentos antes de refatorações.
- Quando houver demanda por documentação em `docs/02-database/`.

## Quando não usar

- Quando o objetivo for desenhar um schema novo.
- Quando a tarefa for apenas documentar a API ou testes.

## Entradas esperadas

- Models/entities
- Migrações
- Schemas/ORM configs
- Sinais de índices, soft delete, auditoria e timestamps

## Processo passo a passo

1. Identificar ORM e convenções de persistência.
2. Ler todas as entidades/modelos relevantes.
3. Ler migrações para confirmar evolução do schema.
4. Mapear:
   - entidades `ENT-001`
   - campos e tipos
   - constraints e enums
   - relacionamentos
   - índices observáveis
   - soft delete, timestamps e auditoria
5. Registrar divergências entre modelo atual e migrações quando houver.
6. Gerar:
   - `docs/02-database/database-overview.md`
   - `docs/02-database/entities.md`
   - `docs/02-database/relationships.md`
   - `docs/02-database/data-dictionary.md`
   - `docs/02-database/migrations-analysis.md`

## Ficheiros e pastas que deve analisar

- Models, entities, schemas
- `migrations/`
- Configuração do ORM
- Repositories ou queries que revelem índices e filtros importantes
- Código de auditoria, soft delete e versionamento

## Documentos que deve gerar

- `docs/02-database/database-overview.md`
- `docs/02-database/entities.md`
- `docs/02-database/relationships.md`
- `docs/02-database/data-dictionary.md`
- `docs/02-database/migrations-analysis.md`

## Regras de segurança

- Nunca alterar schema nesta fase.
- Nunca criar migrações sem pedido explícito.
- Sinalizar qualquer proposta futura de mudança estrutural como dependente de plano de migração.

## Regras de qualidade

- Diferenciar o que está no modelo atual do que está apenas nas migrações.
- Indicar lacunas sobre índices e constraints não explícitos.
- Não inferir cardinalidades sem evidência.

## Formato de saída

- Markdown em `docs/02-database/`
- Tabelas por entidade com:
  - Campo
  - Tipo
  - Obrigatório
  - Default
  - Constraint
  - Evidência

## Exemplos de documentação

- Dicionário de dados por entidade.
- Mapa de relacionamentos com cardinalidade.
- Análise de soft delete e versionamento.
- Resumo de migrações iniciais e suas limitações.

## Critérios de validação

- Todas as entidades principais foram catalogadas.
- Relações e constraints relevantes estão documentadas.
- Migrações foram analisadas e comparadas com o estado atual.
- Campos críticos possuem evidência no código.

