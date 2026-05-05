# Checkpoint - Render Superuser Bootstrap

## Objetivo

Adicionar um caminho seguro e opt-in para criar o primeiro superuser no Render Free, onde o Shell interativo nao esta disponivel.

## Implementacao

- [CONFIRMADO_NO_CODIGO] Foi criado `accounts.management.commands.bootstrap_superuser`.
- [CONFIRMADO_NO_CODIGO] O `entrypoint.sh` agora executa `python manage.py bootstrap_superuser` antes do `exec "$@"`.
- [CONFIRMADO_NO_CODIGO] `.env.example` e `.env.staging.example` agora documentam `DJANGO_CREATE_SUPERUSER`, `DJANGO_SUPERUSER_EMAIL` e `DJANGO_SUPERUSER_PASSWORD`.
- [CONFIRMADO_NO_CODIGO] O comando e idempotente: cria ou atualiza o admin, nao imprime a password e nao faz nada quando o flag esta desligado.

## Fluxo operacional no Render

1. Definir `DJANGO_CREATE_SUPERUSER=True`
2. Definir `DJANGO_SUPERUSER_EMAIL=<email admin>`
3. Definir `DJANGO_SUPERUSER_PASSWORD=<senha forte>`
4. Fazer deploy manual com cache limpo
5. Confirmar login em `/admin/`
6. Voltar `DJANGO_CREATE_SUPERUSER=False`
7. Remover `DJANGO_SUPERUSER_PASSWORD`
8. Fazer novo deploy

## Validacoes locais

- `manage.py check`
- `pytest tests/test_bootstrap_superuser.py`
- `pytest`

## Riscos restantes

- [PRECISA_VALIDAR] O painel Render ainda precisa ser atualizado manualmente para ligar e desligar o bootstrap.
- [PRECISA_VALIDAR] A `DATABASE_URL` exposta anteriormente ainda precisa de rotacao manual no Render.
- [PRECISA_VALIDAR] Depois da rotacao, `/health/` e `/admin/` precisam ser revalidados publicamente.
