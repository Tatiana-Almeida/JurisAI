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
- TanStack Query para cache, invalidação por tenant e polling de módulos jurídicos
- Zustand para auth, bootstrap da sessão e organização ativa
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

## Variáveis de ambiente

Copiar um dos exemplos:

```bash
copy .env.local.example .env.local
```

Arquivos de exemplo:

- `.env.example`
- `.env.local.example`
- `.env.staging.example`

Variáveis públicas preparadas:

- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_APP_NAME`
- `NEXT_PUBLIC_ENVIRONMENT`
- `NEXT_PUBLIC_RENDER_API_URL`
- `NEXT_PUBLIC_ENABLE_MOCKS`
- `NEXT_PUBLIC_ENABLE_BILLING_UI`
- `NEXT_PUBLIC_ENABLE_AI_UI`

Regras operacionais:

- local usa `http://localhost:8000`
- staging usa `https://jurisai-web-wh9d.onrender.com`
- não commitar `.env.local`
- não commitar tokens

## Rodar localmente

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
- O endpoint público de health em staging continua em `GET /health/`.
- A UI de billing permanece desativada para cobrança real enquanto checkout e webhooks comerciais não estiverem concluídos no backend.

## Arquitetura

- `app/`: páginas App Router
- `components/`: layout, auth, módulos e shared UI
- `lib/`: API client, query keys, validação, errors e utils
- `stores/`: auth e organização ativa
- `types/`: contratos TypeScript baseados na API atual
- `tests/`: Vitest unit/integration
- `playwright/`: smoke e2e

## Auth e route guards

- Login via `POST /api/v1/auth/token/`
- Refresh foundation via `POST /api/v1/auth/token/refresh/`
- Bootstrap do utilizador via `GET /api/v1/users/me/`
- Interceptor Axios tenta refresh uma vez antes de encerrar a sessão
- Rotas públicas:
  - `/`
  - `/login`
- Rotas privadas:
  - `/dashboard`
  - `/cases`
  - `/clients`
  - `/documents`
  - `/ocr`
  - `/knowledge-base`
  - `/deadlines`
  - `/calendar`
  - `/finance`
  - `/billing`
  - `/settings`
- O portal `/client-portal` usa guard dedicado com `portalOnly`
- O `middleware.ts` usa apenas um session hint cookie para redirecionamento inicial
- O `ProtectedRoute` faz a proteção real no cliente enquanto os tokens ainda ficam fora de cookies `httpOnly`

## Staging API

- Base URL de staging: `https://jurisai-web-wh9d.onrender.com`
- Validação pública confirmada nesta fase:
  - `GET /health/` responde `200 OK`
  - `POST /api/v1/auth/token/` responde `400` com erros DRF quando enviado payload vazio
- O smoke autenticado com credenciais reais continua dependente de credenciais de staging fora do repositório

## Multi-tenancy

- Toda a fundação foi preparada para `organizationId`
- Query keys organizacionais carregam o identificador ativo
- Ao trocar organização, o frontend limpa o cache do TanStack Query e redireciona para `/dashboard`
- O frontend não deve manter dados do tenant anterior visíveis após a troca

## Cache invalidation

- O provider de organização limpa cache ao trocar tenant
- Queries do tenant novo são invalidadas após a troca
- Jobs de OCR e indexação usam polling apenas quando ainda existem itens `pending` ou `running`

## DRF errors

- `lib/errors/drf.ts` normaliza:
  - erros de validação por campo
  - `non_field_errors`
  - mensagens amigáveis para React Hook Form

## Endpoints consumidos

- `GET /health/` e `GET /api/v1/health/`
- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/users/me/`
- `GET /api/v1/organizations/`
- `GET/POST /api/v1/cases/`
- `GET/PATCH /api/v1/cases/{id}/`
- `GET /api/v1/users/` para clientes e advogados
- `POST /api/v1/users/` para criação de clientes quando o utilizador autenticado tem permissão
- `GET/POST /api/v1/documents/`
- `GET /api/v1/documents/{id}/`
- `GET /api/v1/dashboard/*`
- `GET /api/v1/deadlines/`
- `GET /api/v1/calendar/events/`
- `GET /api/v1/legal-finance/*`
- `GET /api/v1/ocr/*`
- `POST /api/v1/ocr/documents/{document_id}/run/`
- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- `POST /api/v1/ocr/results/{id}/apply-to-document/`
- `GET /api/v1/knowledge-base/*`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `GET /api/v1/client-portal/*`
- `GET /api/v1/subscriptions/` e `GET /api/v1/invoices/`

## Módulos implementados nesta fase

- Login
- Dashboard inicial com awareness de staging
- Processos com listagem, criação, detalhe e edição básica de metadados
- Clientes com listagem e criação via endpoint real de utilizadores
- Documentos com listagem, detalhe, upload multipart e ações de OCR
- OCR com jobs, resultado, audit logs, settings e polling
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
- endurecimento final de autenticação com cookies `httpOnly`
- smoke autenticado real contra staging
- paginação navegável completa para listas longas

## Limitações conhecidas

- O frontend MVP ainda não representa a experiência final de produto
- O login usa `localStorage` porque o backend atual não opera com cookies `httpOnly`
- O `middleware.ts` não lê `localStorage`; por isso usa apenas um cookie de sessão auxiliar para o redirecionamento inicial
- O módulo “Clientes” usa o endpoint real `/api/v1/users/` com filtro por papel `cliente`; o backend não expõe um `/api/v1/clients/` dedicado
- O módulo “Processos” usa o endpoint real `/api/v1/cases/`; o backend atual não expõe `/api/v1/law-cases/`
- Billing UI permanece honesta: sem checkout ativo enquanto o backend não expuser esse fluxo real
- A camada de IA pode continuar a depender de respostas mock no backend quando `OPENAI_API_KEY` não existir
- `local-hash-v1` continua a ser uma fundação técnica de retrieval, não um embedding semântico jurídico completo
- O logo foi integrado a partir do asset fornecido localmente ao workspace

## Próximos passos

1. Refinar UX, guardas de rota e detalhes de navegação
2. Fechar fluxos completos de detalhes, edição e ações críticas por módulo
3. Validar o frontend com credenciais reais em staging autenticado
4. Priorizar billing mínimo e workflows de IA comercialmente úteis
