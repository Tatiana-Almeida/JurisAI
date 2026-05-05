# Staging Deployment Guide

## 1. Objetivo do staging

Validar o deploy do backend JurisAI num ambiente o mais próximo possível de produção, sem ainda amarrar o projeto a um provedor específico de cloud.

## 2. Pré-requisitos

- Docker
- Docker Compose
- domínio ou subdomínio de staging
- reverse proxy
- TLS
- backups

## 3. Arquivos usados

- `docker-compose.staging.yml`
- `.env.staging`
- `docs/11-production/reverse-proxy-tls.md`
- `docs/11-production/backup-restore.md`
- `docs/11-production/monitoring-observability.md`
- `docs/11-production/rollback-checklist.md`

## 4. Setup inicial

1. Copiar o template de ambiente:

```powershell
copy .env.staging.example .env.staging
```

2. Preencher secrets e hosts reais do ambiente.

3. Validar a configuração:

```powershell
docker compose -f docker-compose.staging.yml config
```

4. Construir a imagem:

```powershell
docker compose -f docker-compose.staging.yml build
```

5. Subir a stack:

```powershell
docker compose -f docker-compose.staging.yml up -d
```

## 5. Migrações

Executar migrações antes de abrir o tráfego:

```powershell
docker compose -f docker-compose.staging.yml exec web python manage.py migrate
```

## 6. Static files

- `RUN_COLLECTSTATIC=True` pode ser usado para recolher ficheiros estáticos no arranque controlado.
- Em ambientes com mais controlo operacional, também pode ser executado explicitamente:

```powershell
docker compose -f docker-compose.staging.yml exec web python manage.py collectstatic --noinput
```

## 7. Healthcheck

Após o deploy:

```powershell
curl https://staging.example.com/health/
```

O endpoint deve continuar público, simples e sem dados sensíveis.

## 8. Smoke tests

Usar o script:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/smoke_staging.ps1 -BaseUrl https://staging.example.com
```

Se o host tiver Bash disponivel, tambem pode ser usado:

```bash
bash scripts/smoke_staging.sh https://staging.example.com
```

## 9. Logs

- `docker compose -f docker-compose.staging.yml logs web --tail=100`
- `docker compose -f docker-compose.staging.yml logs worker --tail=100`
- `docker compose -f docker-compose.staging.yml logs flower --tail=100`
- `docker compose -f docker-compose.staging.yml logs db --tail=100`
- `docker compose -f docker-compose.staging.yml logs redis --tail=100`

## 10. Backup

Antes de mudanças sensíveis:

- criar backup PostgreSQL
- validar persistência de `media_data`
- confirmar retenção e localização dos backups

Ver também [backup-restore.md](/c:/projectos/JurisAI/docs/11-production/backup-restore.md).

## 11. Restore

O procedimento de restore deve ser testado antes de depender do staging como ensaio de produção.

Ver também [backup-restore.md](/c:/projectos/JurisAI/docs/11-production/backup-restore.md).

## 12. Rollback

Sempre documentar:

- release atual
- release anterior
- backup associado
- motivo do rollback
- comandos executados

Ver também [rollback-checklist.md](/c:/projectos/JurisAI/docs/11-production/rollback-checklist.md).

## 13. Segurança

- `DEBUG=False`
- secrets apenas por variáveis de ambiente
- Redis sem exposição pública
- Flower sem exposição pública
- TLS obrigatório no reverse proxy
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` e `CORS_ALLOWED_ORIGINS` explícitos
- providers externos continuam desativados por padrão
