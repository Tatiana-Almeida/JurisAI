# Checkpoint - Frontend MVP Polish and Staging Validation

## Objetivo

- [CONFIRMADO_NO_CODIGO] Polir os fluxos principais do Frontend MVP e preparar validacao manual contra staging Render.

## Areas refinadas

- [CONFIRMADO_NO_CODIGO] Login com mensagens mais claras para credenciais invalidas, API offline e erro interno.
- [CONFIRMADO_NO_CODIGO] Organizacao ativa com estado vazio, erro amigavel e nome visivel no topo.
- [CONFIRMADO_NO_CODIGO] Navegacao com melhor foco, responsividade, labels mais claras e breadcrumb simples.
- [CONFIRMADO_NO_CODIGO] Clientes, Processos e Documentos mantidos com estados sem tenant mais claros.
- [CONFIRMADO_NO_CODIGO] Knowledge Base com avisos explicitos para baixa confianca, ausencia de fontes, fallback e limite do `local-hash-v1`.
- [CONFIRMADO_NO_CODIGO] Billing readiness mantido honesto, sem checkout, portal nem enforcement comercial falsos.

## Validacao

- [CONFIRMADO_NO_CODIGO] Backend `manage.py check`.
- [CONFIRMADO_NO_CODIGO] Backend `pytest`.
- [CONFIRMADO_NO_CODIGO] Frontend `npm run typecheck`.
- [CONFIRMADO_NO_CODIGO] Frontend `npm run lint`.
- [CONFIRMADO_NO_CODIGO] Frontend `npm run test`.
- [CONFIRMADO_NO_CODIGO] Frontend `npm run build`.
- [CONFIRMADO_NO_CODIGO] Frontend `npm run test:e2e`.

## Testing against Render staging

- [CONFIRMADO_NO_CODIGO] A branch documenta o fluxo manual via `.env.staging.example -> .env.local`.
- [PRECISA_VALIDAR] O login autenticado real contra `https://jurisai-web-wh9d.onrender.com` ainda depende de credenciais de staging fora do repositorio.

## Limitacoes

- [CONFIRMADO_NO_CODIGO] Billing checkout ainda pendente.
- [CONFIRMADO_NO_CODIGO] Worker Celery no Render Free ainda pendente.
- [PRECISA_VALIDAR] Dominio customizado ainda pendente no staging publico.
- [PRECISA_VALIDAR] Monitoramento externo ainda pendente.
- [PRECISA_VALIDAR] Backup agendado ainda pendente.
