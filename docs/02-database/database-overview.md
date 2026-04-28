# Database Overview

## Tecnologia de persistência

- [CONFIRMADO_NO_CÓDIGO] O backend usa o ORM do Django.
- [CONFIRMADO_NO_CÓDIGO] O banco principal previsto é PostgreSQL.
- [CONFIRMADO_NO_CÓDIGO] O projeto pode usar SQLite em testes ou quando configurado por variável de ambiente.

## Estratégia de modelagem

- [CONFIRMADO_NO_CÓDIGO] As entidades de negócio usam UUID como chave primária.
- [CONFIRMADO_NO_CÓDIGO] A maioria das entidades inclui `created_at` e, frequentemente, `updated_at`.
- [CONFIRMADO_NO_CÓDIGO] O tenant principal é `Organization`, referenciado por várias entidades.
- [CONFIRMADO_NO_CÓDIGO] Há soft delete explícito em `LawCase.deleted`.

## Observações estruturais

- [CONFIRMADO_NO_CÓDIGO] `AuditLog` não possui FK para `Organization`.
- [CONFIRMADO_NO_CÓDIGO] `Document` implementa versionamento por `unique_together (law_case, version)`.
- [CONFIRMADO_NO_CÓDIGO] `AIRequest` armazena prompt, resposta, tokens e custo.
- [PRECISA_VALIDAR] O schema lógico esperado pelo código diverge da migration inicial de `Organization.plan`.

