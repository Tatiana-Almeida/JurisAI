# Checkpoint - Frontend Staging Deployment Validation

## Objetivo

Validar a preparacao do deploy publico do Frontend MVP em staging e a comunicacao esperada com o backend Render.

## Ambiente

- Backend: `https://jurisai-web-wh9d.onrender.com`
- Frontend: `https://frontend-phi-five-90.vercel.app`
- Provider: `Vercel`
- Branch: `main`
- Frontend path: `frontend/`

## Configuracao

- [CONFIRMADO_NO_CODIGO] `frontend/.env.staging.example` aponta para `https://jurisai-web-wh9d.onrender.com`
- [CONFIRMADO_NO_CODIGO] `frontend/README.md` agora documenta deploy de staging, `NEXT_PUBLIC_API_URL` e a dependencia de env vars no build
- [CONFIRMADO_NO_CODIGO] O backend aceita `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` por env vars
- [CONFIRMADO_NO_CODIGO] `jurisai/settings.py` ja faz parsing de multiplas origens por virgula e remove espacos laterais
- [CONFIRMADO_NO_CODIGO] O frontend foi publicado em Vercel com build bem-sucedido a partir de `frontend/`
- [PRECISA_VALIDAR] A URL `https://frontend-phi-five-90.vercel.app` ainda precisa ser inserida em `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` no Render

## Validacoes

- [CONFIRMADO_NO_CODIGO] Frontend build local: passed
- [CONFIRMADO_NO_CODIGO] Frontend tests locais: passed
- [CONFIRMADO_NO_CODIGO] Frontend e2e local: passed
- [CONFIRMADO_NO_CODIGO] Backend `manage.py check`: passed
- [CONFIRMADO_NO_CODIGO] Backend `pytest`: `195 passed`
- [CONFIRMADO_NO_CODIGO] Backend health publico `GET /api/v1/health/`: passed
- [CONFIRMADO_NO_CODIGO] Auth token endpoint publico com payload vazio retorna `400`, coerente com validacao DRF
- [CONFIRMADO_NO_CODIGO] Frontend deploy publico: passed
- [CONFIRMADO_NO_CODIGO] Login page publica do frontend: passed
- [CONFIRMADO_NO_CODIGO] Dashboard protected publico: passed para redirecionamento ao login sem sessao
- [CONFIRMADO_NO_CODIGO] E2E staging sem credenciais: passed contra `https://frontend-phi-five-90.vercel.app`
- [PRECISA_VALIDAR] API communication browser -> backend: failed nesta sessao por CORS ainda nao ajustado no backend Render
- [PRECISA_VALIDAR] Clients flow: depende de deploy publico + credenciais de staging
- [PRECISA_VALIDAR] Cases flow: depende de deploy publico + credenciais de staging
- [PRECISA_VALIDAR] Documents flow: depende de deploy publico + credenciais de staging
- [PRECISA_VALIDAR] OCR flow: depende de deploy publico + credenciais de staging + worker disponivel
- [PRECISA_VALIDAR] Knowledge Base flow: depende de deploy publico + credenciais de staging

## Observacoes operacionais

- [CONFIRMADO_NO_CODIGO] `NEXT_PUBLIC_*` em Next.js deve ser configurado no ambiente de build do provider escolhido
- [CONFIRMADO_NO_CODIGO] Foi criado `frontend/playwright/staging.spec.ts` para smoke de staging via `E2E_STAGING_BASE_URL`, sem commitar credenciais
- [CONFIRMADO_NO_CODIGO] `npx vercel deploy --yes` autenticou por device flow, publicou o frontend e retornou a URL final `https://frontend-phi-five-90.vercel.app`
- [CONFIRMADO_NO_CODIGO] `GET /admin/` no backend staging voltou a responder `302` para `/admin/login/?next=/admin/`, em vez de `500`, nesta sessao
- [CONFIRMADO_NO_CODIGO] Um `fetch` real em browser a partir do frontend publico para `POST /api/v1/auth/token/` falhou com `TypeError: Failed to fetch`, consistente com bloqueio de CORS
- [CONFIRMADO_NO_CODIGO] O preflight `OPTIONS` para `POST /api/v1/auth/token/` respondeu sem `Access-Control-Allow-Origin`, reforcando que o backend ainda nao aceita a origem do frontend publicado
- [PRECISA_VALIDAR] A atualizacao de `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` no painel do Render nao foi executada nesta sessao porque nao ha acesso operacional ao ambiente Render a partir deste terminal

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
- [CONFIRMADO_NO_CODIGO] O frontend staging publico foi publicado com sucesso em `https://frontend-phi-five-90.vercel.app`
- [PRECISA_VALIDAR] A validacao ponta a ponta browser -> frontend -> backend continua bloqueada ate atualizar `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` no Render com a origem `https://frontend-phi-five-90.vercel.app`
- [PRECISA_VALIDAR] Esta fase nao deve ser marcada como release comercial nem como producao pronta
