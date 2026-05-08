# Checkpoint - Frontend Environment Setup

## Objetivo

Preparar 100% do ambiente tecnico do Frontend MVP do JurisAI numa branch separada, sem ainda construir todas as telas finais.

## Branch criada

- [CONFIRMADO_NO_CODIGO] `feature/frontend-mvp`

## Stack instalada

- [CONFIRMADO_NO_CODIGO] Next.js App Router
- [CONFIRMADO_NO_CODIGO] TypeScript
- [CONFIRMADO_NO_CODIGO] Tailwind CSS
- [CONFIRMADO_NO_CODIGO] shadcn/ui
- [CONFIRMADO_NO_CODIGO] Axios
- [CONFIRMADO_NO_CODIGO] TanStack Query
- [CONFIRMADO_NO_CODIGO] Zustand
- [CONFIRMADO_NO_CODIGO] React Hook Form + Zod
- [CONFIRMADO_NO_CODIGO] TanStack Table
- [CONFIRMADO_NO_CODIGO] Sonner
- [CONFIRMADO_NO_CODIGO] Lucide React
- [CONFIRMADO_NO_CODIGO] Recharts
- [CONFIRMADO_NO_CODIGO] react-dropzone
- [CONFIRMADO_NO_CODIGO] react-pdf
- [CONFIRMADO_NO_CODIGO] FullCalendar
- [CONFIRMADO_NO_CODIGO] Stripe.js
- [CONFIRMADO_NO_CODIGO] Vitest
- [CONFIRMADO_NO_CODIGO] React Testing Library
- [CONFIRMADO_NO_CODIGO] Playwright

## Estrutura criada

- [CONFIRMADO_NO_CODIGO] `frontend/` foi criado e isolado do backend.
- [CONFIRMADO_NO_CODIGO] Pastas base de `app/`, `components/`, `lib/`, `stores/`, `types/`, `tests/`, `playwright/` e `public/brand/` foram preparadas.

## Tooling configurado

- [CONFIRMADO_NO_CODIGO] Providers globais com QueryClient, ThemeProvider, Sonner e provider de organizacao.
- [CONFIRMADO_NO_CODIGO] Query keys organizacionais e limpeza de cache por tenant.
- [CONFIRMADO_NO_CODIGO] API client Axios com interceptors preparados para JWT/DRF.
- [CONFIRMADO_NO_CODIGO] Mapper de erros DRF para React Hook Form.
- [CONFIRMADO_NO_CODIGO] Vitest e Playwright configurados.
- [CONFIRMADO_NO_CODIGO] Dockerfile frontend e `docker-compose.frontend.yml` criados.
- [CONFIRMADO_NO_CODIGO] Workflow dedicado em `.github/workflows/frontend-ci.yml`.

## Logo integrado

- [CONFIRMADO_NO_CODIGO] O logo fornecido foi copiado para `frontend/public/brand/jurisai-logo.png`.
- [CONFIRMADO_NO_CODIGO] Foram criadas copias `jurisai-logo-dark.png` e `jurisai-logo-light.png` sem alterar o asset original.

## Limitacoes

- [CONFIRMADO_NO_CODIGO] Esta fase nao implementa o frontend final completo.
- [CONFIRMADO_NO_CODIGO] O login usa storage local porque o backend atual nao opera com cookies `httpOnly`.
- [CONFIRMADO_NO_CODIGO] Billing UI permanece honesta e nao finge checkout pronto.
- [PRECISA_VALIDAR] O componente `form` do shadcn nao foi exigido para a fundacao atual, porque a base do login ja opera com RHF/Zod/Input/Label.

## Proximos passos

1. Construir as telas completas do MVP.
2. Ligar queries reais por modulo.
3. Fechar guardas de rota e refresh token.
4. Integrar estados vazios/loading/error por fluxo final.
