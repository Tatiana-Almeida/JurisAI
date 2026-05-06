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

## Arquitetura

- `app/`: páginas App Router
- `components/`: layout, auth, módulos e shared UI
- `lib/`: API client, query keys, validação, errors e utils
- `stores/`: auth e organização ativa
- `types/`: contratos TypeScript baseados na API atual
- `tests/`: Vitest unit/integration
- `playwright/`: smoke e2e

## Multi-tenancy

- Toda a fundação foi preparada para `organizationId`.
- Query keys organizacionais carregam o identificador ativo.
- A troca de organização limpa/invalida cache para evitar mistura entre tenants.

## DRF errors

- `lib/errors/drf.ts` normaliza:
  - erros de validação por campo
  - `non_field_errors`
  - mensagens amigáveis para React Hook Form

## Limitações

- O frontend MVP ainda não implementa as telas finais.
- O login usa storage local porque o backend atual não opera com cookies `httpOnly`.
- Billing UI permanece honesta: sem checkout ativo enquanto o backend não expuser esse fluxo real.
- O logo foi integrado a partir do asset fornecido localmente ao workspace.

## Próximos passos

1. Construir as telas finais do MVP.
2. Ligar cada módulo aos endpoints reais do backend.
3. Fechar os fluxos de tenant switching, auth refresh e estados vazios/erro por módulo.
