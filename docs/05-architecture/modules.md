# Modules

| Módulo | Entradas | Saídas/Dependências | Observações | Estado |
|---|---|---|---|---|
| `accounts` | rotas de usuários | `organizations`, auth Django | centraliza usuário customizado | [CONFIRMADO_NO_CÓDIGO] |
| `organizations` | CRUD de organização | usado por quase todo o sistema | tenant principal | [CONFIRMADO_NO_CÓDIGO] |
| `law_cases` | CRUD de casos | depende de `accounts` e `organizations` | soft delete | [CONFIRMADO_NO_CÓDIGO] |
| `deadlines` | CRUD e task | depende de `law_cases`, `notifications` | lembretes por email | [CONFIRMADO_NO_CÓDIGO] |
| `documents` | CRUD de documentos | depende de `law_cases`, `jurisai.utils` | versionamento | [CONFIRMADO_NO_CÓDIGO] |
| `ai_assistant` | endpoints IA | `AIService`, `AIRequest`, OpenAI | quota por plano | [CONFIRMADO_NO_CÓDIGO] |
| `billing` | CRUD + webhook | `organizations`, `notifications` | webhook público | [CONFIRMADO_NO_CÓDIGO] |
| `notifications` | CRUD + tasks | SMTP e mock WhatsApp | envio assíncrono | [CONFIRMADO_NO_CÓDIGO] |
| `audit_logs` | leitura + signals | depende de `jurisai.middleware` | auditoria transversal | [CONFIRMADO_NO_CÓDIGO] |

