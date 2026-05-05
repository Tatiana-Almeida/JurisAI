# Checkpoint - Release v1.0.0-rc.4

## Release

- v1.0.0-rc.4 - HTTPS and Monitoring Validation

## Objetivo

Validar camada publica segura de staging.

## Entregas

- reverse proxy/TLS guide/example
- HTTPS smoke validation flow
- monitoring validation documentation
- backup scheduling documentation
- PostgreSQL backup script
- updated production docs

## Testes

- pytest local: `192 passed`
- `manage.py check`: passed
- `bash -n scripts/backup_postgres.sh`: passed
- `bash -n scripts/smoke_staging.sh`: passed
- smoke HTTPS: pending
- monitoring: pending
- backup schedule: documented

## Seguranca

- Redis/PostgreSQL/Flower privados
- web atras de reverse proxy
- secrets fora do repositorio
- HTTPS documentado e pendente de validacao em dominio real

## Limitacoes

- dominio publico real ainda nao esta configurado neste ambiente
- TLS/HTTPS publico ainda nao foi validado ponta a ponta
- monitoring externo ainda nao foi configurado
- backup automatico ainda nao foi ativado no host
