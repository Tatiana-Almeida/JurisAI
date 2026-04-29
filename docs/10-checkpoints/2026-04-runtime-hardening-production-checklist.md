# Checkpoint — Runtime Hardening Production Checklist

## Objetivo
Fechar o hardening final de runtime para preparar a release `v1.0.0-rc.1`.

## Alterações feitas
- containers `web`, `worker` e `flower` passaram a correr como utilizador nao-root
- Redis deixou de ter exposicao publica por porta no host
- foi criada uma checklist final de producao para secrets, rede, TLS, backups, storage e observabilidade

## Validações Docker
- `docker compose config`
- `docker compose build`
- `docker compose up -d`
- `GET /health/`
- `docker compose exec web python manage.py check`
- `docker compose exec web python -m pytest tests/test_healthcheck.py`
- `docker compose exec redis redis-cli -a redis_password ping`
- `docker compose logs worker --tail=100`
- `docker compose down`

## Testes
- `.\.venv\Scripts\python.exe manage.py check`
- `.\.venv\Scripts\python.exe -m pytest`
- smoke test Docker validado

## Riscos restantes
- producao real ainda requer reverse proxy, TLS, backups e observabilidade externa
- Flower deve permanecer privado
- secrets reais devem vir do ambiente
- Redis continua autenticado, mas qualquer exposicao futura deve ser explicitamente justificada

## Proximos passos
- preparar a checklist final da release `v1.0.0-rc.1`
- validar deploy com proxy/TLS no ambiente alvo
- documentar rollback operacional
