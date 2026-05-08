# Checkpoint - Frontend MVP Initial Build

## Objetivo

Construir a primeira versao funcional do frontend do JurisAI sobre a fundacao previamente instalada em `feature/frontend-mvp`, respeitando os endpoints e a logica real do backend.

## Paginas criadas

- [CONFIRMADO_NO_CODIGO] `app/dashboard/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/cases/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/cases/new/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/cases/[id]/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/clients/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/documents/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/documents/[id]/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/ocr/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/knowledge-base/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/knowledge-base/[id]/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/deadlines/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/calendar/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/finance/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/billing/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/settings/page.tsx`
- [CONFIRMADO_NO_CODIGO] `app/client-portal/page.tsx`

## Modulos base

- [CONFIRMADO_NO_CODIGO] Auth foundation com login JWT, refresh foundation e bootstrap do utilizador.
- [CONFIRMADO_NO_CODIGO] Contexto de organizacao ativa com invalidacao/limpeza de cache por tenant.
- [CONFIRMADO_NO_CODIGO] Dashboard com healthcheck, metricas, prazos e atividade recente.
- [CONFIRMADO_NO_CODIGO] Cases UI com listagem, detalhe e criacao.
- [CONFIRMADO_NO_CODIGO] Clients UI sobre o backend de `users`, filtrando `role=cliente`.
- [CONFIRMADO_NO_CODIGO] Documents UI com upload foundation, listagem, detalhe e botao de OCR.
- [CONFIRMADO_NO_CODIGO] OCR UI com jobs, resultados, page results, audit logs e settings.
- [CONFIRMADO_NO_CODIGO] Knowledge Base UI com bases, ask, fontes, jobs de indexacao e settings RAG.
- [CONFIRMADO_NO_CODIGO] Billing UI honesta, sem fingir checkout ou cancelamento prontos.

## Integracao com API

- [CONFIRMADO_NO_CODIGO] O frontend foi alinhado aos endpoints reais do backend, como `/api/v1/cases/`, `/api/v1/users/`, `/api/v1/documents/`, `/api/v1/ocr/*`, `/api/v1/knowledge-base/*` e `/api/v1/legal-finance/*`.
- [CONFIRMADO_NO_CODIGO] Nenhum endpoint ficticio foi promovido como funcional.
- [CONFIRMADO_NO_CODIGO] Billing permaneceu em modo de leitura/parcial, sem ativar checkout inexistente.

## Auth foundation

- [CONFIRMADO_NO_CODIGO] `Authorization: Bearer` via Axios interceptor.
- [CONFIRMADO_NO_CODIGO] Tentativa unica de refresh token antes de forcar logout.
- [CONFIRMADO_NO_CODIGO] `localStorage` continua como medida temporaria nesta fase.

## Organization context

- [CONFIRMADO_NO_CODIGO] Toda query juridica relevante carrega `organizationId` na query key.
- [CONFIRMADO_NO_CODIGO] A troca de organizacao remove cache do tenant anterior e invalida dados do tenant novo.
- [CONFIRMADO_NO_CODIGO] O frontend evita mistura de dados entre organizacoes desde a fundacao.

## OCR foundation

- [CONFIRMADO_NO_CODIGO] Polling para jobs OCR em `pending` ou `running`.
- [CONFIRMADO_NO_CODIGO] Exibicao de `OCRSettings`, `OCRAuditLog`, `OCRPageResult` e aplicacao de resultado ao documento.

## Knowledge Base foundation

- [CONFIRMADO_NO_CODIGO] `ask` com resposta, confianca e fontes.
- [CONFIRMADO_NO_CODIGO] `RAGSettings` com alerta honesto sobre `local-hash-v1`.
- [CONFIRMADO_NO_CODIGO] Jobs de indexacao preparados com polling.

## Billing honesto

- [CONFIRMADO_NO_CODIGO] A UI nao declara checkout, cancelamento nem portal comercial como prontos.
- [CONFIRMADO_NO_CODIGO] O modulo apenas apresenta estado atual e dependencias pendentes do backend.

## Testes

- [CONFIRMADO_NO_CODIGO] `npm run typecheck`: passed
- [CONFIRMADO_NO_CODIGO] `npm run lint`: passed com warnings conhecidos do React Compiler sobre bibliotecas externas
- [CONFIRMADO_NO_CODIGO] `npm run test`: passed
- [CONFIRMADO_NO_CODIGO] `npm run build`: passed

## Limitacoes

- [PRECISA_VALIDAR] Fluxos completos de navegacao autenticada ainda dependem de dados reais em staging.
- [PRECISA_VALIDAR] Billing comercial continua bloqueado pela ausencia de checkout e cancelamento confirmados no backend.
- [PRECISA_VALIDAR] A camada de IA continua dependente do estado real do backend e pode devolver respostas mock sem provider configurado.

## Proximos passos

1. Refinar UX e guardas de rota.
2. Validar a experiencia com dados reais em staging autenticado.
3. Priorizar frontend final para processos, documentos e Knowledge Base.
4. Fechar billing minimo e workflows de IA de maior valor comercial.
