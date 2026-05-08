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

## Requisitos

- Node.js 20 LTS ou superior
- npm 10 ou superior

## Instalacao

```bash
npm install
```

## Variaveis de ambiente

Arquivos de exemplo:

- `.env.example`
- `.env.local.example`
- `.env.staging.example`

Regras operacionais:

- local usa `http://localhost:8000`
- staging usa `https://jurisai-web-wh9d.onrender.com`
- nao commitar `.env.local`
- nao commitar tokens

Variaveis publicas principais:

- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_APP_NAME`
- `NEXT_PUBLIC_ENVIRONMENT`
- `NEXT_PUBLIC_RENDER_API_URL`
- `NEXT_PUBLIC_ENABLE_MOCKS`
- `NEXT_PUBLIC_ENABLE_BILLING_UI`
- `NEXT_PUBLIC_ENABLE_AI_UI`

## Rodar localmente

```bash
npm run dev
```

## Testing against Render staging

1. Copie `.env.staging.example` para `.env.local`.
2. Confirme `NEXT_PUBLIC_API_URL=https://jurisai-web-wh9d.onrender.com`.
3. Rode `npm run dev`.
4. Abra `http://localhost:3000`.
5. Entre com um utilizador criado no Django Admin do staging.
6. Valide dashboard, organizacao ativa, clientes, processos, documentos, OCR e Knowledge Base.

Nao commite `.env.local` nem tokens de autenticacao.

## Frontend staging deployment

Opcao recomendada para esta fase:

- Vercel com `Root Directory=frontend/` e framework `Next.js`

URL publica atual de staging:

- `https://frontend-phi-five-90.vercel.app`

Variaveis publicas esperadas no deploy:

- `NEXT_PUBLIC_API_URL=https://jurisai-web-wh9d.onrender.com`
- `NEXT_PUBLIC_APP_NAME=JurisAI`
- `NEXT_PUBLIC_ENVIRONMENT=staging`
- `NEXT_PUBLIC_ENABLE_MOCKS=false`
- `NEXT_PUBLIC_ENABLE_BILLING_UI=false`
- `NEXT_PUBLIC_ENABLE_AI_UI=true`

Notas operacionais:

- `NEXT_PUBLIC_*` em Next.js influencia o build e deve estar presente no ambiente de build do provider.
- Depois de existir uma URL publica do frontend, o backend de staging deve incluir essa origem em `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS`.
- Nesta sessao, o frontend publico foi publicado com sucesso no Vercel, mas o backend Render ainda nao aceitava a origem `https://frontend-phi-five-90.vercel.app` para o fluxo de login em browser.
- Esta fase continua a ser validacao tecnica de staging, nao uma release de producao.

## Build e testes

```bash
npm run typecheck
npm run lint
npm run test
npm run build
npm run test:e2e
```

Smoke opcional contra staging publicado:

```bash
E2E_STAGING_BASE_URL=https://frontend-phi-five-90.vercel.app npm run test:e2e
```

## Arquitetura

- `app/`: paginas App Router
- `components/`: layout, auth, modulos e shared UI
- `hooks/`: hooks de dados e integracao com React Query
- `lib/`: API client, query keys, validacao, errors e utils
- `stores/`: auth e organizacao ativa
- `types/`: contratos TypeScript baseados na API atual
- `tests/`: Vitest unit/integration
- `playwright/`: smoke e2e

## Auth e route guards

- Login via `POST /api/v1/auth/token/`
- Refresh foundation via `POST /api/v1/auth/token/refresh/`
- Bootstrap do utilizador via `GET /api/v1/users/me/`
- Interceptor Axios tenta refresh uma vez antes de encerrar a sessao
- Rotas publicas:
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
- O `ProtectedRoute` faz a protecao real no cliente enquanto os tokens ainda ficam fora de cookies `httpOnly`

## Multi-tenancy

- Todas as query keys juridicas carregam `organizationId`
- Hooks dependentes de tenant usam `enabled: Boolean(organizationId)`
- Ao trocar organizacao, o frontend limpa o cache do TanStack Query e redireciona para `/dashboard`
- O frontend nao deve manter dados do tenant anterior visiveis apos a troca

## DRF errors

- `lib/errors/drf.ts` normaliza:
  - erros de validacao por campo
  - `non_field_errors`
  - mensagens amigaveis para React Hook Form

## Endpoints consumidos

- `GET /health/` e `GET /api/v1/health/`
- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/users/me/`
- `GET /api/v1/organizations/`
- `GET/POST /api/v1/cases/`
- `GET/PATCH /api/v1/cases/{id}/`
- `GET /api/v1/users/` para clientes e advogados
- `POST /api/v1/users/` para criacao de clientes quando o utilizador autenticado tem permissao
- `GET/POST /api/v1/documents/`
- `GET /api/v1/documents/{id}/`
- `GET /api/v1/dashboard/*`
- `GET /api/v1/deadlines/`
- `GET /api/v1/calendar/events/`
- `GET /api/v1/legal-finance/*`
- `GET /api/v1/ocr/jobs/`
- `GET /api/v1/ocr/results/`
- `GET /api/v1/ocr/page-results/`
- `GET /api/v1/ocr/results/{id}/pages/`
- `GET /api/v1/ocr/audit-logs/`
- `GET/PATCH /api/v1/ocr/settings/`
- `GET /api/v1/ocr/pipelines/`
- `POST /api/v1/ocr/documents/{document_id}/run/`
- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- `POST /api/v1/ocr/results/{id}/apply-to-document/`
- `POST /api/v1/ocr/pipelines/knowledge-base/`
- `GET /api/v1/knowledge-base/`
- `GET /api/v1/knowledge-base/{id}/stats/`
- `GET /api/v1/knowledge-base/documents/`
- `GET /api/v1/knowledge-base/queries/`
- `GET /api/v1/knowledge-base/indexing-jobs/`
- `GET /api/v1/knowledge-base/embedding-audit-logs/`
- `GET/PATCH /api/v1/knowledge-base/settings/`
- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`
- `GET /api/v1/client-portal/*`
- `GET /api/v1/subscriptions/` e `GET /api/v1/invoices/`

## Modulos implementados nesta fase

- Login
- Dashboard inicial com awareness de staging
- Processos com listagem, criacao, detalhe e edicao basica de metadados
- Clientes com listagem e criacao via endpoint real de utilizadores
- Documentos com listagem, detalhe, upload multipart e acoes de OCR
- OCR com jobs, resultado, page results, audit logs, settings, pipeline e polling
- Knowledge Base com list/detail, search, ask, stats, settings, audit logs e sources
- Prazos
- Calendario
- Financeiro
- Billing honesto
- Settings
- Portal do Cliente

## Fluxos operacionais integrados

- `Prazos`: consome `GET /api/v1/deadlines/` com filtros por estado, `upcoming_days`, destaque visual para itens criticos e bloqueio quando nao existe organizacao ativa.
- `Calendario`: consome `GET /api/v1/calendar/events/` e apresenta eventos juridicos por tipo e estado, com fallback visual elegante quando nao ha eventos.
- `Financeiro`: consome `GET /api/v1/legal-finance/summary/`, `GET /api/v1/legal-finance/invoices/` e `GET /api/v1/legal-finance/expenses/`, com resumo honesto e graficos apenas quando ha dados reais.
- `Billing`: permanece em modo readiness, lendo `subscriptions` e `invoices` reais sem expor checkout, portal self-serve ou cancelamento inexistentes.
- `Settings`: consolida perfil, organizacao ativa, OCR settings, RAG settings, seguranca e estado do ambiente, sem fingir configuracoes ainda nao expostas pelo backend.
- `Portal do Cliente`: usa os endpoints reais `/api/v1/client-portal/cases/`, `/api/v1/client-portal/documents/` e `/api/v1/client-portal/messages/`, mas continua marcado como foundation.

## OCR flows

- A tela `/ocr` cobre jobs, results, page results, audit logs, settings e pipelines.
- O detalhe do documento liga o fluxo real `documento -> OCR -> resultado -> Document.content -> Knowledge Base`.
- Polling fica ativo apenas enquanto existirem jobs `pending` ou `running`.
- `PATCH /api/v1/ocr/settings/` respeita os campos reais do backend e continua a mapear erros DRF para o formulario.
- O pipeline OCR -> Knowledge Base exige confirmacao explicita para atualizar `Document.content`.

## Knowledge Base flows

- A lista de bases mostra estado geral, stats resumidos e indexing jobs.
- O detalhe de base suporta tabs para overview, search, ask, documents, indexing jobs, settings e audit logs.
- `search` e `ask` mostram `sources`, `confidence`, `retrieval_method`, `fallback_used` e `fallback_reason` quando o backend devolve esses campos.
- `PATCH /api/v1/knowledge-base/settings/` continua alinhado ao contrato real de `RAGSettings`.
- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/` permanece documentado como foundation tecnica, nao como IA semantica comercial pronta.

## Modulos pendentes ou parciais

- billing comercial completo
- UX final do client portal
- fluxos avancados de IA e geracao juridica
- endurecimento final de autenticacao com cookies `httpOnly`
- smoke autenticado real contra staging
- paginacao navegavel completa para listas longas

## Limitacoes conhecidas

- O frontend MVP ainda nao representa a experiencia final de produto
- O login usa `localStorage` porque o backend atual nao opera com cookies `httpOnly`
- O `middleware.ts` nao le `localStorage`; por isso usa apenas um cookie de sessao auxiliar para o redirecionamento inicial
- O deploy publico do frontend depende de acesso ao provider escolhido e de variaveis `NEXT_PUBLIC_*` configuradas no momento do build
- O frontend staging publico atual esta em `https://frontend-phi-five-90.vercel.app`
- O login em browser continua dependente de atualizar `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` no backend Render para essa origem
- O modulo "Clientes" usa o endpoint real `/api/v1/users/` com filtro por papel `cliente`; o backend nao expoe um `/api/v1/clients/` dedicado
- O modulo "Processos" usa o endpoint real `/api/v1/cases/`; o backend atual nao expoe `/api/v1/law-cases/`
- Billing UI permanece honesta: sem checkout ativo enquanto o backend nao expuser esse fluxo real
- Billing readiness continua parcial:
  - checkout ainda nao configurado
  - webhooks comerciais ainda pendentes de integracao end-to-end
  - bloqueio por plano ainda pendente
- A camada de IA pode continuar a depender de respostas mock no backend quando `OPENAI_API_KEY` nao existir
- `local-hash-v1` continua a ser uma fundacao tecnica de retrieval, nao um embedding semantico juridico completo
- No Render Free, OCR e indexing podem continuar limitados se o worker Celery nao estiver ativo
- No Render Free, o worker Celery continua um bloqueador para OCR/indexacao totalmente reais em background
- O backend publico de staging ainda precisa manter `/admin/` e os fluxos autenticados saudaveis para validacao ponta a ponta do frontend
- O build de producao foi ajustado para usar fontes locais/system-safe em vez de depender de `next/font/google`, evitando falhas de rede em CI e ambientes restritos
- O logo foi integrado a partir do asset fornecido localmente ao workspace

## Checklist manual de UX

- Login mostra erro por campo e erro global sem expor tokens.
- Troca de organizacao limpa o cache e atualiza a navegacao.
- Modulos juridicos nao fazem queries sem tenant ativo.
- Billing continua honesto, sem botoes de pagamento ativos.
- Knowledge Base destaca baixa confianca, fallback e limitacao do `local-hash-v1`.
- Dashboard informa que o worker Celery continua pendente no Render Free.

## Proximos passos

1. Refinar UX, guardas de rota e detalhes de navegacao
2. Refinar OCR e Knowledge Base com dados autenticados de staging
3. Validar o frontend com credenciais reais em staging autenticado
4. Priorizar billing minimo e workflows de IA comercialmente uteis
