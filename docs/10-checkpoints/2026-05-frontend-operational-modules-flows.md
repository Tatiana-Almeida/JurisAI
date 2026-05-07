# Checkpoint - Frontend Operational Modules Flows

## Objetivo

- [CONFIRMADO_NO_CODIGO] Integrar os modulos operacionais de Prazos, Calendario, Financeiro, Billing readiness, Settings e Portal do Cliente no Frontend MVP sem inventar contratos inexistentes.

## Endpoints integrados

- [CONFIRMADO_NO_CODIGO] `GET /api/v1/deadlines/` alimenta a tela de prazos com filtros por `completed`, `law_case_id`, `search`, `ordering` e `upcoming_days`.
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/calendar/events/` alimenta a tela de calendario com eventos juridicos reais por tenant.
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/legal-finance/summary/`, `GET /api/v1/legal-finance/invoices/` e `GET /api/v1/legal-finance/expenses/` alimentam o resumo financeiro e as listas auxiliares.
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/subscriptions/` e `GET /api/v1/invoices/` continuam a alimentar apenas o readiness de billing.
- [CONFIRMADO_NO_CODIGO] `GET /api/v1/client-portal/cases/`, `GET /api/v1/client-portal/documents/` e `GET /api/v1/client-portal/messages/` alimentam o portal do cliente.

## Multi-tenancy

- [CONFIRMADO_NO_CODIGO] Todas as query keys juridicas destes modulos incluem `organizationId`.
- [CONFIRMADO_NO_CODIGO] Nenhum hook operacional dispara requests sem `organizationId`; o frontend mostra `EmptyState` quando nao existe tenant ativo.
- [CONFIRMADO_NO_CODIGO] A troca de organizacao continua a limpar o cache do TanStack Query antes de redirecionar para `/dashboard`.

## UX e estados

- [CONFIRMADO_NO_CODIGO] Prazos receberam destaque visual para itens criticos e em atraso.
- [CONFIRMADO_NO_CODIGO] Calendario mostra estado vazio, erro e visual diferenciado por tipo e estado.
- [CONFIRMADO_NO_CODIGO] Financeiro mostra resumo com `Recharts` apenas quando existem dados reais e cai para estado parcial honesto quando o backend nao devolve informacao util.
- [CONFIRMADO_NO_CODIGO] Billing continua honesto, sem habilitar checkout, cancelamento self-serve ou portal comercial inexistentes.
- [CONFIRMADO_NO_CODIGO] Settings consolida perfil, organizacao ativa, OCR, RAG, seguranca e status de ambiente sem fingir cobertura completa do backend.
- [CONFIRMADO_NO_CODIGO] Portal do Cliente continua explicitamente marcado como foundation, mesmo consumindo endpoints reais.

## Validacao

- [CONFIRMADO_NO_CODIGO] `npm.cmd run typecheck` passou apos o ajuste da tabela de prazos.
- [CONFIRMADO_NO_CODIGO] `npm.cmd run test` passou com cobertura para prazos, calendario, financeiro/billing, settings e portal do cliente.
- [CONFIRMADO_NO_CODIGO] `npm.cmd run lint` permaneceu verde com warnings conhecidos do React Compiler sobre `useReactTable()` e `react-hook-form`, sem erros.
- [CONFIRMADO_NO_CODIGO] `npm.cmd run build` passou apos a substituicao das fontes remotas por fontes locais/system-safe.
- [CONFIRMADO_NO_CODIGO] `npm.cmd run test:e2e` passou com as rotas operacionais protegidas.
- [CONFIRMADO_NO_CODIGO] `python manage.py check` passou sem issues.
- [CONFIRMADO_NO_CODIGO] `python -m pytest` passou com `195 passed`.

## Limitacoes

- [CONFIRMADO_NO_CODIGO] Billing comercial continua parcial: nao existe checkout confirmado, cancelamento self-serve nem portal de faturacao.
- [CONFIRMADO_NO_CODIGO] O Portal do Cliente ainda nao representa uma experiencia final para clientes externos.
- [CONFIRMADO_NO_CODIGO] O build do frontend precisava deixar de depender de `next/font/google` para ser reproduzivel em ambientes sem acesso estavel ao Google Fonts.
- [CONFIRMADO_NO_CODIGO] O backend completo foi revalidado nesta sessao sem regressao funcional.

## Proximos passos

- [CONFIRMADO_NO_CODIGO] Fechar validacao final de build/e2e/backend.
- [CONFIRMADO_NO_CODIGO] Refinar criacao e filtros avancados para prazos e calendario.
- [CONFIRMADO_NO_CODIGO] Ligar financeiro e portal do cliente a cenarios autenticados de staging real.
