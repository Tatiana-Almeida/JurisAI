# Checkpoint — Docker Runtime Validation

## Objetivo
Validar build, runtime, healthchecks e smoke tests Docker depois do hardening de deploy.

## Commit base
- `c2f7c6c security: harden deployment configuration`

## Comandos executados
- `docker compose config`
- `docker compose build`
- `docker compose up -d`
- `GET /health/`
- `docker compose exec web python manage.py check`
- `docker compose exec web python manage.py makemigrations --check --dry-run`
- `docker compose exec web python -m pytest tests/test_healthcheck.py`
- `docker compose exec web python -m pytest`
- `docker compose exec redis redis-cli -a redis_password ping`
- `docker compose down`

## Resultado
- O daemon Docker Desktop foi iniciado e a validacao passou a executar integralmente.
- O `.env` local foi alinhado com valores minimos de desenvolvimento para PostgreSQL, Redis, Flower e secrets locais.
- `docker compose config` passou com as variaveis corretas e Flower sem exposicao publica por porta direta.
- O primeiro `docker compose build` real revelou uma colisao do buildx ao exportar imagens separadas para `web`, `worker` e `flower` a partir do mesmo `Dockerfile`.
- A correcao minima foi reutilizar uma imagem unica `jurisai-app:latest` no `docker-compose`, deixando apenas `web` com `build`.
- A primeira subida da stack revelou que o comando `celery flower` nao existia no container; a correcao minima foi pinagem de `flower==2.0.1` em `requirements.txt`.
- Depois dessas correcoes, `docker compose build` passou, `docker compose up -d` subiu a stack, `/health/` respondeu `200` e os healthchecks de `web`, `db`, `redis` e `flower` ficaram saudaveis.
- O `worker` tambem ficou saudavel apos o arranque completo; os primeiros pings falharam apenas durante o bootstrap do Celery.
- Dentro do container `web`, `manage.py check`, `makemigrations --check --dry-run`, `tests/test_healthcheck.py` e a suite completa (`192 passed`) passaram.
- O Redis respondeu `PONG` apenas com autenticacao por password.

## Riscos restantes
- O worker continua a arrancar como `root`, o que gera `SecurityWarning` do Celery; isso nao bloqueou a validacao, mas deve ser endurecido antes de producao.
- O PostgreSQL do Compose continua com autenticacao local permissiva no bootstrap padrao da imagem oficial; para producao real, isso deve ser combinado com rede privada e parametros adicionais.
- O ambiente real de producao ainda requer reverse proxy, TLS, backups e observabilidade externa.
- O Flower deve permanecer privado.
- Secrets reais devem vir do ambiente.

## Proximos passos
- Executar o `worker` com utilizador nao-root no container.
- Fechar a exposicao publica do Redis se nao for necessaria fora da rede Docker.
- Adicionar checklist final de runtime para preparar a `v1.0.0-rc.1`.
