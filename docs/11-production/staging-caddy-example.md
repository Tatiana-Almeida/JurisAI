# Staging Caddy Example

## Objetivo

Documentar um exemplo minimo de Caddy para expor o JurisAI em staging por HTTPS, mantendo o backend Django acessivel apenas via `127.0.0.1:8000`.

## Exemplo

```caddy
staging.seudominio.com {
    encode gzip

    reverse_proxy 127.0.0.1:8000

    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
}
```

## Notas operacionais

- [CONFIRMADO_NO_CODIGO] O `docker-compose.staging.yml` ja expõe `web` apenas em `127.0.0.1:8000`.
- [CONFIRMADO_NO_CODIGO] `db`, `redis` e `flower` permanecem sem exposicao publica no compose de staging.
- [PRECISA_VALIDAR] O dominio real `staging.seudominio.com` e a emissao automatica de certificados dependem da infra do host.
- [PRECISA_VALIDAR] Se houver uploads grandes de documentos, validar tambem limites de request no proxy e timeouts adequados.

## Variaveis de ambiente esperadas no host

- `DJANGO_ALLOWED_HOSTS=staging.seudominio.com`
- `CORS_ALLOWED_ORIGINS=https://staging.seudominio.com`
- `CSRF_TRUSTED_ORIGINS=https://staging.seudominio.com`
- `DJANGO_DEBUG=False`
