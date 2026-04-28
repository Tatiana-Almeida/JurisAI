# Authentication

## Modelo de autenticação

- [CONFIRMADO_NO_CÓDIGO] A autenticação padrão da API é JWT via `rest_framework_simplejwt.authentication.JWTAuthentication`.
- [CONFIRMADO_NO_CÓDIGO] O header esperado é `Authorization: Bearer <token>`.
- [CONFIRMADO_NO_CÓDIGO] O `access token` dura 30 minutos.
- [CONFIRMADO_NO_CÓDIGO] O `refresh token` dura 7 dias.
- [CONFIRMADO_NO_CÓDIGO] O refresh é rotativo e o token anterior entra em blacklist após rotação.

## Endpoints de autenticação

- [CONFIRMADO_NO_CÓDIGO] `POST /api/v1/auth/token/`
- [CONFIRMADO_NO_CÓDIGO] `POST /api/v1/auth/token/refresh/`
- [CONFIRMADO_NO_CÓDIGO] `POST /api/v1/auth/token/verify/`

## Autorização e permissões

| Permissão | Comportamento observado | Estado |
|---|---|---|
| `IsOrganizationMember` | Exige utilizador autenticado com `organization` | [CONFIRMADO_NO_CÓDIGO] |
| `IsOrganizationMember.has_object_permission` | Permite acesso quando `obj.organization` é nulo ou coincide com a do usuário | [CONFIRMADO_NO_CÓDIGO] |
| `IsAdmin` | Exige `request.user.role == 'admin'` | [CONFIRMADO_NO_CÓDIGO] |
| `IsLawyer` | Exige papel `advogado` | [CONFIRMADO_NO_CÓDIGO] |
| `IsClient` | Exige papel `cliente` | [CONFIRMADO_NO_CÓDIGO] |

## Endpoints públicos observados

- [CONFIRMADO_NO_CÓDIGO] `/api/v1/auth/token/`
- [CONFIRMADO_NO_CÓDIGO] `/api/v1/auth/token/refresh/`
- [CONFIRMADO_NO_CÓDIGO] `/api/v1/auth/token/verify/`
- [CONFIRMADO_NO_CÓDIGO] `/api/v1/users/register/`
- [CONFIRMADO_NO_CÓDIGO] `/api/v1/webhook/`
- [CONFIRMADO_NO_CÓDIGO] `/api/v1/health/`
- [CONFIRMADO_NO_CÓDIGO] `/swagger/`
- [CONFIRMADO_NO_CÓDIGO] `/redoc/`

## Observações importantes

- [CONFIRMADO_NO_CÓDIGO] A filtragem por tenant acontece sobretudo nas views, não exclusivamente na camada de permissão.
- [PRECISA_VALIDAR] Alguns serializers aceitam IDs de relações sem validação explícita de tenant, o que pode comprometer o isolamento esperado.

