# JurisAI Frontend MVP

## Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zustand
- React Hook Form + Zod
- Axios
- Vitest
- Playwright

## Skills usadas

- Next.js App Router para roteamento e composição do shell SaaS
- TanStack Query para cache e polling de módulos jurídicos
- Zustand para auth e organização ativa
- React Hook Form + Zod para formulários e validação local
- shadcn/ui + Tailwind para a base visual JurisAI
- TanStack Table para listas operacionais
- FullCalendar para a fundação do calendário
- Sonner para feedback de ações assíncronas

## Requisitos

- Node.js 20 LTS ou superior
- npm 10 ou superior

## Instalação

```bash
npm install
```

## Env vars

Copiar um dos exemplos:

```bash
copy .env.local.example .env.local
```

Variáveis públicas preparadas:

- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_APP_NAME`
- `NEXT_PUBLIC_ENVIRONMENT`
- `NEXT_PUBLIC_RENDER_API_URL`
- `NEXT_PUBLIC_ENABLE_MOCKS`
- `NEXT_PUBLIC_ENABLE_BILLING_UI`
- `NEXT_PUBLIC_ENABLE_AI_UI`

## Rodar local

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Testes

```bash
npm run test
npm run test:e2e
```

## Integração com backend

- O frontend consome o backend JurisAI via `NEXT_PUBLIC_API_URL`.
- O client HTTP foi preparado para DRF, JWT e paginação `count/next/previous/results`.
- Não foram inventados endpoints inexistentes do backend.
- `DATABASE_URL`, billing, OCR e RAG continuam controlados no backend; o frontend apenas consome contratos já confirmados.

## Arquitetura

- `app/`: páginas App Router
- `components/`: layout, auth, módulos e shared UI
- `lib/`: API client, query keys, validação, errors e utils
- `stores/`: auth e organização ativa
- `types/`: contratos TypeScript baseados na API atual
- `tests/`: Vitest unit/integration
- `playwright/`: smoke e2e

## Auth

- Login via `POST /api/v1/auth/token/`
- Refresh foundation via `POST /api/v1/auth/token/refresh/`
- Bootstrap do utilizador via `GET /api/v1/users/me/`
- Interceptor Axios tenta refresh uma vez antes de encerrar a sessão
- Tokens ficam em `localStorage` nesta fase

TODO hardening:

- migrar para cookies `httpOnly` quando o backend suportar esse fluxo

## Endpoints consumidos

- `GET /health/` e `GET /api/v1/health/`
- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/users/me/`
- `GET /api/v1/organizations/`
- `GET/POST /api/v1/cases/`
- `GET /api/v1/users/` para clientes e advogados
- `GET/POST /api/v1/documents/`
- `GET /api/v1/dashboard/*`
- `GET /api/v1/deadlines/`
- `GET /api/v1/calendar/events/`
- `GET /api/v1/legal-finance/*`
- `GET /api/v1/ocr/*`
- `POST /api/v1/ocr/documents/{document_id}/run/`
- `POST /api/v1/ocr/results/{id}/apply-to-document/`
- `GET /api/v1/knowledge-base/*`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `GET /api/v1/client-portal/*`
- `GET /api/v1/subscriptions/` e `GET /api/v1/invoices/`

## Multi-tenancy

- Toda a fundação foi preparada para `organizationId`.
- Query keys organizacionais carregam o identificador ativo.
- A troca de organização limpa/invalida cache para evitar mistura entre tenants.

## Cache invalidation

- O provider de organização remove queries do tenant anterior
- Queries do tenant novo são invalidadas ao trocar organização
- Jobs de OCR e indexação usam polling apenas quando ainda existem itens `pending` ou `running`

## DRF errors

- `lib/errors/drf.ts` normaliza:
  - erros de validação por campo
  - `non_field_errors`
  - mensagens amigáveis para React Hook Form

## Módulos implementados nesta fase

- Login
- Dashboard inicial
- Processos
- Clientes
- Documentos com upload foundation
- OCR com jobs, resultado, audit logs e settings
- Knowledge Base com ask e sources
- Prazos
- Calendário
- Financeiro
- Billing honesto
- Settings
- Portal do Cliente

## Módulos pendentes ou parciais

- billing comercial completo
- UX final do client portal
- fluxos avançados de IA e geração jurídica
- experiência final de onboarding e guardas de rota
- autenticação endurecida com cookies `httpOnly`

## Limitações

- O frontend MVP ainda não representa a experiência final de produto.
- O login usa storage local porque o backend atual não opera com cookies `httpOnly`.
- Billing UI permanece honesta: sem checkout ativo enquanto o backend não expuser esse fluxo real.
- A camada de IA pode continuar a depender de respostas mock no backend quando `OPENAI_API_KEY` não existir.
- `local-hash-v1` continua a ser uma fundação técnica de retrieval, não um embedding semântico jurídico completo.
- O logo foi integrado a partir do asset fornecido localmente ao workspace.

## Próximos passos

1. Refinar UX, guardas de rota e detalhes de navegação.
2. Fechar fluxos completos de detalhes, edição e ações críticas por módulo.
3. Validar o frontend contra dados reais em staging autenticado.
4. Priorizar billing mínimo e workflows de IA comercialmente úteis.
