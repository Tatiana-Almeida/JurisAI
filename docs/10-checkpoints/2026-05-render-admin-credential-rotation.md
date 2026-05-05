# Checkpoint - Render Admin and Credential Rotation

## Objetivo

Registar o fecho operacional apos o bootstrap inicial do admin no Render.

## Estado deste checkpoint

- [PRECISA_VALIDAR] Este passo depende de acesso manual ao painel do Render e nao pode ser concluido apenas a partir do repositrio local.

## Passos operacionais

1. Confirmar login administrativo em `https://jurisai-web-wh9d.onrender.com/admin/`
2. Alterar `DJANGO_CREATE_SUPERUSER=False`
3. Remover `DJANGO_SUPERUSER_PASSWORD`
4. Fazer novo deploy
5. Rotacionar as credenciais do PostgreSQL/`DATABASE_URL`
6. Atualizar o `DATABASE_URL` no `jurisai-web`
7. Fazer novo deploy
8. Revalidar `/health/` e `/admin/`

## Evidencia esperada

- `/health/` continua `200 OK`
- `/admin/` continua acessivel
- bootstrap ficou desligado
- `DJANGO_SUPERUSER_PASSWORD` deixou de existir no ambiente
- `DATABASE_URL` passou a usar credencial nova
