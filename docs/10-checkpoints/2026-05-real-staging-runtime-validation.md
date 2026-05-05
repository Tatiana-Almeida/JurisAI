# Checkpoint - Real Staging Runtime Validation

## Objetivo

Validar a execucao real de staging com Docker daemon ativo.

## Base

- tag/base: `v1.0.0-rc.2`
- commit: `f84692e`

## Ambiente

- OS: `Microsoft Windows NT 10.0.26200.0`
- Docker version: client/server `29.1.3`
- Docker Compose version: `v2.40.3-desktop.1`
- dominio: nao
- TLS: nao
- reverse proxy: nao

## Contexto da validacao

- [CONFIRMADO_NO_CODIGO] O runtime real foi validado localmente com `.env.staging` nao versionado e secrets efemeros gerados apenas para esta execucao.
- [CONFIRMADO_NO_CODIGO] A primeira tentativa com o projeto Compose padrao `jurisai` reutilizou um volume PostgreSQL anterior e falhou em `migrate` com erro de autenticacao.
- [CONFIRMADO_NO_CODIGO] Para evitar apagar dados locais preexistentes, a validacao final foi refeita com `docker compose -p jurisai_rc3 ...`, criando rede e volumes isolados.

## Comandos executados

- `docker version`
- `docker compose version`
- `docker info`
- `git status`
- `git log --oneline -n 5`
- `git tag --list`
- `git rev-parse HEAD`
- `git describe --tags --always`
- `docker compose -f docker-compose.staging.yml --env-file .env.staging config`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging build`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging up -d`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging ps -a`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging logs --tail=120`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging exec -T web python manage.py migrate`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging exec -T web python manage.py collectstatic --noinput`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging exec -T web python manage.py check`
- `curl.exe -f http://127.0.0.1:8000/health/`
- `powershell -ExecutionPolicy Bypass -File scripts/smoke_staging.ps1 -BaseUrl http://127.0.0.1:8000`
- `bash scripts/smoke_staging.sh http://127.0.0.1:8000`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging exec -T redis redis-cli -a <REDIS_PASSWORD> ping`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging exec -T db sh -lc 'PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > /tmp/jurisai_staging_test.sql'`
- `docker compose -p jurisai_rc3 -f docker-compose.staging.yml --env-file .env.staging exec -T db sh` com script para `dropdb`, `createdb`, `psql -f /tmp/jurisai_staging_test.sql` e verificacao de `django_migrations`

## Resultados

- compose config: passed
- build: passed
- up: passed
- healthcheck local: passed em `http://127.0.0.1:8000/health/`
- healthcheck publico: [PRECISA_VALIDAR] sem dominio/TLS neste ambiente
- smoke tests: PowerShell passed e Bash passed
- migrations: passed
- collectstatic: passed
- django check: passed
- redis auth: passed com `PONG`
- flower privado: passed; sem porta publicada no host
- network privacy: passed; `db` e `redis` sem portas publicas, `web` apenas em `127.0.0.1:8000`
- backup: passed; dump gerado em `backups/jurisai_staging_test.sql` com `252940` bytes
- restore: passed em banco temporario `jurisai_restore_test`, com `86` registos em `django_migrations`
- logs: passed; `web`, `worker`, `db`, `redis` e `flower` subiram sem erro bloqueante

## Riscos restantes

- [PRECISA_VALIDAR] TLS pendente enquanto nao existir dominio de staging e reverse proxy ativo.
- [PRECISA_VALIDAR] Healthcheck publico por HTTPS pendente.
- [PRECISA_VALIDAR] Monitoring externo continua pendente de implantacao.
- [PRECISA_VALIDAR] Backups automaticos e politica de retencao ainda nao foram ensaiados neste ambiente.

## Decisao

- Aprovado para a proxima etapa de staging.
- [INFERIDO_DO_CODIGO] A release `v1.0.0-rc.3` pode ser preparada como validacao real de runtime local com Docker daemon ativo, mantendo como pendencias explicitas dominio/TLS e monitoring externo.
