# Relationships

| Relação | Cardinalidade observada | Estado |
|---|---|---|
| `Organization -> User` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> LawCase` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> Deadline` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> Document` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> AIRequest` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> Payment` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> Subscription` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> Invoice` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `Organization -> Notification` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `User(client) -> LawCase` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `User(lawyer) -> LawCase` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `LawCase -> Deadline` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `LawCase -> Document` | 1:N | [CONFIRMADO_NO_CÓDIGO] |
| `User -> AIRequest` | 1:N opcional | [CONFIRMADO_NO_CÓDIGO] |
| `User -> AuditLog` | 1:N opcional | [CONFIRMADO_NO_CÓDIGO] |

## Integridade referencial

- [CONFIRMADO_NO_CÓDIGO] `organization` usa `PROTECT` na maioria das entidades.
- [CONFIRMADO_NO_CÓDIGO] `law_case` usa `CASCADE` em `Deadline` e `Document`.
- [CONFIRMADO_NO_CÓDIGO] `client` e `lawyer` usam `PROTECT` em `LawCase`.
- [CONFIRMADO_NO_CÓDIGO] `AIRequest.user` e `AuditLog.user` usam `SET_NULL`.

## Observações

- [PRECISA_VALIDAR] A existência das FKs por si só não garante validação cruzada de tenant nas criações via API.

