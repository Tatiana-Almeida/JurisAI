# Error Catalog

## Formato padrão

- [CONFIRMADO_NO_CÓDIGO] O handler `custom_exception_handler` devolve payloads no formato `{error, details}` para erros tratados pelo DRF.

## Catálogo

| Código | Situação | Resposta observada | Estado |
|---|---|---|---|
| 400 | ValidationError | `error: validation_error` | [CONFIRMADO_NO_CÓDIGO] |
| 401 | AuthenticationFailed/NotAuthenticated | `error: authentication_failed` | [CONFIRMADO_NO_CÓDIGO] |
| 403 | PermissionDenied | `error: permission_denied` | [CONFIRMADO_NO_CÓDIGO] |
| 429 | Quota IA excedida | Exceção `Throttled` com detalhe textual | [CONFIRMADO_NO_CÓDIGO] |
| 500 | Exceção não tratada | `error: server_error` | [CONFIRMADO_NO_CÓDIGO] |

## Erros funcionais específicos

- [CONFIRMADO_NO_CÓDIGO] `RegisterView` retorna 400 se `organization_name` não for enviado.
- [CONFIRMADO_NO_CÓDIGO] `ChangePasswordView` retorna 400 quando a senha antiga está incorreta.
- [CONFIRMADO_NO_CÓDIGO] `UserViewSet.perform_create` pode lançar `PermissionDenied` para usuário não admin.
- [CONFIRMADO_NO_CÓDIGO] `UserViewSet.perform_create` pode lançar `PermissionDenied` se o limite de usuários do plano foi atingido.
- [CONFIRMADO_NO_CÓDIGO] `LawCaseViewSet.perform_create` pode lançar `PermissionDenied` se o limite de casos do plano foi atingido.
- [CONFIRMADO_NO_CÓDIGO] `DocumentViewSet.perform_create` pode lançar `PermissionDenied` se o limite de documentos do plano foi atingido.
- [CONFIRMADO_NO_CÓDIGO] `AIService._ensure_ai_quota` lança `Throttled` quando o limite mensal de IA é excedido.

## Lacunas

- [NÃO_ENCONTRADO] Catálogo formal de códigos de erro por endpoint.
- [NÃO_ENCONTRADO] Exceções customizadas por domínio além do handler global.

