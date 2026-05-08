# Checkpoint - Frontend Staging Deployment Validation

## Objetivo

Validar a preparacao do deploy publico do Frontend MVP em staging e a comunicacao esperada com o backend Render.

## Ambiente

- Backend: `https://jurisai-web-wh9d.onrender.com`
- Frontend: [PRECISA_VALIDAR] URL publica do frontend nao foi disponibilizada nesta sessao
- Branch: `main`
- Frontend path: `frontend/`

## Configuracao

- [CONFIRMADO_NO_CODIGO] `frontend/.env.staging.example` aponta para `https://jurisai-web-wh9d.onrender.com`
- [CONFIRMADO_NO_CODIGO] `frontend/README.md` agora documenta deploy de staging, `NEXT_PUBLIC_API_URL` e a dependencia de env vars no build
- [CONFIRMADO_NO_CODIGO] O backend aceita `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` por env vars
- [PRECISA_VALIDAR] A URL publica final do frontend ainda precisa ser inserida em `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` no Render

## Validacoes

- [CONFIRMADO_NO_CODIGO] Frontend build local: passed
- [CONFIRMADO_NO_CODIGO] Frontend tests locais: passed
- [CONFIRMADO_NO_CODIGO] Frontend e2e local: passed
- [CONFIRMADO_NO_CODIGO] Backend `manage.py check`: passed
- [CONFIRMADO_NO_CODIGO] Backend `pytest`: `195 passed`
- [CONFIRMADO_NO_CODIGO] Backend health publico `GET /api/v1/health/`: passed
- [CONFIRMADO_NO_CODIGO] Auth token endpoint publico com payload vazio retorna `400`, coerente com validacao DRF
- [PRECISA_VALIDAR] Frontend deploy publico: nao executado nesta sessao por falta de acesso operacional ao provider de deploy
- [PRECISA_VALIDAR] Login page publica do frontend: depende da URL publica do frontend
- [PRECISA_VALIDAR] Dashboard protected publico: depende da URL publica do frontend e de login autenticado real
- [PRECISA_VALIDAR] API communication browser -> backend: depende de CORS/CSRF ajustados apos existir a URL publica do frontend
- [PRECISA_VALIDAR] Clients flow: depende de deploy publico + credenciais de staging
- [PRECISA_VALIDAR] Cases flow: depende de deploy publico + credenciais de staging
- [PRECISA_VALIDAR] Documents flow: depende de deploy publico + credenciais de staging
- [PRECISA_VALIDAR] OCR flow: depende de deploy publico + credenciais de staging + worker disponivel
- [PRECISA_VALIDAR] Knowledge Base flow: depende de deploy publico + credenciais de staging

## Observacoes operacionais

- [CONFIRMADO_NO_CODIGO] `NEXT_PUBLIC_*` em Next.js deve ser configurado no ambiente de build do provider escolhido
- [CONFIRMADO_NO_CODIGO] Foi criado `frontend/playwright/staging.spec.ts` para smoke de staging via `E2E_STAGING_BASE_URL`, sem commitar credenciais
- [PRECISA_VALIDAR] O backend publico respondeu `200` em `/health/`, mas `/admin/` devolveu `500` nesta sessao, o que indica que o staging autenticado ainda nao esta totalmente saudavel
- [PRECISA_VALIDAR] `npx vercel` e `npx netlify` nao puderam ser usados de forma conclusiva nesta sessao porque ficaram dependentes de autenticacao/interacao fora do repositrio

## Limitacoes

- Auth ainda usa `localStorage`
- Worker Celery pendente no Render Free
- Billing comercial pendente
- Storage persistente para uploads pendente
- IA/RAG ainda MVP tecnico
- Monitoring externo pendente
- Backups agendados pendentes

## Decisao

- [CONFIRMADO_NO_CODIGO] O frontend esta tecnicamente preparado para staging e continua verde localmente em `main`
- [PRECISA_VALIDAR] O deploy publico do frontend e a validacao ponta a ponta continuam pendentes por falta de acesso operacional ao provider de deploy e por o backend de staging ainda apresentar instabilidade em `/admin/`
- [PRECISA_VALIDAR] Esta fase nao deve ser marcada como release comercial nem como producao pronta
