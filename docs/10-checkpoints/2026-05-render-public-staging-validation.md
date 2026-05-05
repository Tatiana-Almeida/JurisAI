# Checkpoint - Render Public Staging Validation

## Objetivo

Registar a validacao inicial do JurisAI em staging publico no Render.

## Ambiente

- Plataforma: Render
- Servico web: `jurisai-web`
- URL publica: `https://jurisai-web-wh9d.onrender.com`
- Banco: Render PostgreSQL
- Redis/Valkey: Render Key Value
- Plano web: Free
- Worker Celery: pending por limitacao de plano

## Validacoes

- HTTPS publico: passed
- `/health/`: passed
- `/admin/`: passed
- Postgres configurado: configured
- Redis configurado: configured
- Worker Celery: pending
- Shell: unavailable on Free plan
- Superuser: pending bootstrap
- Monitoring externo: pending
- Backup agendado: pending
- Custom domain: pending

## Evidencia

- [CONFIRMADO_NO_CODIGO] `https://jurisai-web-wh9d.onrender.com/health/` respondeu `200 OK` com `{"status": "ok", "service": "jurisai", "version": "v0.11.0"}`.
- [CONFIRMADO_NO_CODIGO] `https://jurisai-web-wh9d.onrender.com/admin/` respondeu com redirecionamento para `/admin/login/?next=/admin/`.
- [CONFIRMADO_NO_CODIGO] A pagina `https://jurisai-web-wh9d.onrender.com/admin/login/?next=/admin/` carregou o formulario de login do Django Admin.
- [CONFIRMADO_NO_CODIGO] `powershell -ExecutionPolicy Bypass -File scripts/smoke_staging.ps1 -BaseUrl https://jurisai-web-wh9d.onrender.com` passou.
- [CONFIRMADO_NO_CODIGO] `bash scripts/smoke_staging.sh https://jurisai-web-wh9d.onrender.com` passou.
- [INFERIDO_DO_CODIGO] A stack publica no Render confirma deploy web HTTPS funcional, mas nao prova por si so a execucao do worker Celery porque o plano atual nao suporta Background Worker gratuito.

## Seguranca

- Secrets configurados via Render Environment
- `.env.staging` nao commitado
- Redis nao exposto externamente
- Postgres usa conexao interna no Render
- `DATABASE_URL` exposta anteriormente deve ser rotacionada
- bootstrap admin deve ser desligado apos uso

## Decisao

O bloqueio anterior baseado em ausencia total de HTTPS publico foi parcialmente resolvido pelo dominio Render.
Ainda nao ha evidencia suficiente para uma `v1.0.0` estavel.
A `v1.0.0-rc.5` pode ser publicada apenas como `Render Public Staging Validation`, mantendo todas as pendencias operacionais explicitas.

## Pendencias

- rotacionar `DATABASE_URL` e credenciais PostgreSQL
- criar superuser via bootstrap seguro
- desligar bootstrap apos login
- configurar monitoring externo
- configurar backup agendado
- decidir sobre worker Celery pago ou alternativa
- opcional: dominio personalizado
