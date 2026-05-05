# Checkpoint - Release v1.0.0-rc.2

## Release

- v1.0.0-rc.2 - Staging Deployment Validation

## Objetivo

Preparar a validacao de staging do JurisAI, incluindo compose especifico de staging, template de environment, documentacao de reverse proxy/TLS, backups, restore, monitoring, rollback e smoke tests.

## Entregas

- `docker-compose.staging.yml`
- `.env.staging.example`
- `docs/11-production/staging-deployment-guide.md`
- `docs/11-production/reverse-proxy-tls.md`
- `docs/11-production/backup-restore.md`
- `docs/11-production/monitoring-observability.md`
- `docs/11-production/rollback-checklist.md`
- `scripts/smoke_staging.ps1`
- `scripts/smoke_staging.sh`

## Seguranca

- secrets fora do repositorio
- `DEBUG=False` em staging
- Redis sem exposicao publica
- Flower sem exposicao publica
- db sem exposicao publica
- reverse proxy/TLS documentado
- backup/restore documentado
- rollback documentado

## Validacoes

- `manage.py check`: passed
- `makemigrations --check --dry-run`: passed
- `pytest`: `192 passed`
- `docker compose config`: passed
- `docker compose -f docker-compose.staging.yml config`: passed

## Limitacoes

- build/up staging real depende de Docker daemon ativo
- TLS real depende do servidor/reverse proxy
- backups reais dependem do ambiente de staging
- monitoring externo ainda precisa implantacao

## Proximos passos

- executar staging real num servidor
- validar TLS
- validar backups/restores reais
- validar monitoring externo
- preparar `v1.0.0` estavel ou frontend MVP
