# Checkpoint - HTTPS and Monitoring Validation

## Objetivo

Validar dominio, TLS, reverse proxy, smoke tests HTTPS, monitoring e backup agendado.

## Base

- tag anterior: `v1.0.0-rc.3`
- commit anterior: `2506d1a`

## Validacoes

- dominio: pending
- reverse proxy: documented
- TLS: documented, pending validacao publica
- HTTPS `/health/`: pending
- smoke HTTPS: pending
- monitoring: documented, pending configuracao externa
- backup schedule: documented
- rollback: documented por referencia

## Resultados

- [CONFIRMADO_NO_CODIGO] Foi criado o exemplo de Caddy em [docs/11-production/staging-caddy-example.md](/c:/projectos/JurisAI/docs/11-production/staging-caddy-example.md) para manter `web` atras de reverse proxy.
- [CONFIRMADO_NO_CODIGO] Foi criada a documentacao de monitorizacao em [docs/11-production/staging-monitoring-validation.md](/c:/projectos/JurisAI/docs/11-production/staging-monitoring-validation.md).
- [CONFIRMADO_NO_CODIGO] Foi criada a documentacao de agenda de backups em [docs/11-production/backup-schedule.md](/c:/projectos/JurisAI/docs/11-production/backup-schedule.md).
- [CONFIRMADO_NO_CODIGO] Foi criado o script [scripts/backup_postgres.sh](/c:/projectos/JurisAI/scripts/backup_postgres.sh) sem secrets hardcoded e dependente de `.env.staging`.
- [CONFIRMADO_NO_CODIGO] `manage.py check` e `pytest` continuam a ser a validacao local minima da release e passaram nesta fase com `192 passed`.
- [CONFIRMADO_NO_CODIGO] `bash -n scripts/backup_postgres.sh` e `bash -n scripts/smoke_staging.sh` passaram nesta fase.
- [PRECISA_VALIDAR] Nao foi possivel validar HTTPS publico nem smoke tests sobre dominio real porque este ambiente nao dispoe de subdominio/TLS configurados.
- [PRECISA_VALIDAR] O smoke PowerShell local para `http://127.0.0.1:8000` falhou nesta fase apenas porque nao havia aplicacao ativa no momento da execucao.
- [PRECISA_VALIDAR] Nao foi possivel confirmar redirecionamento HTTP -> HTTPS sem reverse proxy publico em funcionamento.

## Pendencias

- configurar subdominio real de staging
- atualizar `.env.staging` no host com `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS` HTTPS reais
- ativar Caddy ou Nginx no host de staging
- validar `curl -f https://staging.seudominio.com/health/`
- validar smoke tests PowerShell e Bash via HTTPS
- configurar monitor externo real e testar alertas
