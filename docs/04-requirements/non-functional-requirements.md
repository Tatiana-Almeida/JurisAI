# Non Functional Requirements

## RNF-001 Autenticação padrão obrigatória

- [CONFIRMADO_NO_CÓDIGO] O DRF usa `IsAuthenticated` por padrão.

## RNF-002 Paginação padrão da API

- [CONFIRMADO_NO_CÓDIGO] A API usa `StandardPagination` com `PAGE_SIZE = 20`.

## RNF-003 Filtros e ordenação

- [CONFIRMADO_NO_CÓDIGO] A API suporta filtros, busca e ordenação em vários recursos.

## RNF-004 Execução assíncrona

- [CONFIRMADO_NO_CÓDIGO] O backend utiliza Celery e Redis para tarefas assíncronas.

## RNF-005 Compatibilidade com PostgreSQL e SQLite

- [CONFIRMADO_NO_CÓDIGO] O sistema alterna entre PostgreSQL e SQLite por configuração/contexto de testes.

## RNF-006 Armazenamento de mídia e estáticos

- [CONFIRMADO_NO_CÓDIGO] Há configuração de `MEDIA_ROOT` e `STATIC_ROOT`.

## RNF-007 Documentação interativa da API

- [CONFIRMADO_NO_CÓDIGO] Há Swagger e ReDoc configurados.

## RNF-008 Auditoria de alterações

- [CONFIRMADO_NO_CÓDIGO] O sistema registra create/update/delete em `AuditLog`.

## RNF-009 Isolamento por organização

- [INFERIDO_DO_CÓDIGO] O sistema pretende isolar dados por tenant via `organization`.
- [PRECISA_VALIDAR] O isolamento não é garantido de forma uniforme em todos os caminhos de criação/relacionamento.

## RNF-010 Operação em containers

- [CONFIRMADO_NO_CÓDIGO] O projeto inclui `Dockerfile` e `docker-compose.yml`.

