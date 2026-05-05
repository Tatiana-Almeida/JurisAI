# Checkpoint - Render DATABASE_URL and Startup Migrations

## Objetivo

Corrigir deploy Render Free para usar `DATABASE_URL` e permitir migrations no startup.

## Problema

Logs do Render indicaram tentativa de resolver host `db`, que so existe no Docker Compose.

## Correcao

- `DATABASE_URL` passa a ter prioridade sobre `POSTGRES_*` quando definida.
- `RUN_MIGRATIONS=True` executa `migrate --noinput` no startup.
- Migrations rodam antes de `bootstrap_superuser`.

## Seguranca

- `RUN_MIGRATIONS` e explicito.
- `RUN_MIGRATIONS=False` por padrao.
- Secrets continuam em variaveis de ambiente.
- Nenhum secret foi commitado.

## Validacao

- `manage.py check`
- `pytest tests/test_bootstrap_superuser.py`
- `pytest`
- redeploy Render esperado com `RUN_MIGRATIONS=True`
