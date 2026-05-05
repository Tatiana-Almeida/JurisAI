# Reverse Proxy and TLS

## Objetivo

Documentar uma configuração genérica de proxy reverso e TLS para staging, mantendo o backend JurisAI acessível apenas através de HTTPS e sem expor `db`, `redis` ou `flower`.

## Regras operacionais

- usar HTTPS
- configurar `DJANGO_ALLOWED_HOSTS`
- configurar `CSRF_TRUSTED_ORIGINS`
- configurar `CORS_ALLOWED_ORIGINS`
- não expor `db`, `redis` ou `flower`

## Nginx

Exemplo de princípios:

```nginx
server {
    listen 80;
    server_name staging.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name staging.example.com;

    ssl_certificate /etc/letsencrypt/live/staging.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.example.com/privkey.pem;

    client_max_body_size 25m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

TLS pode ser gerido com Certbot ou solução equivalente.

## Caddy

Exemplo de princípios:

```caddy
staging.example.com {
    reverse_proxy 127.0.0.1:8000
}
```

## Notas

- `web` pode ficar exposto apenas em `127.0.0.1:8000` quando o proxy está no mesmo host
- `db`, `redis` e `flower` devem permanecer apenas na rede interna do Docker
- headers de proxy e HTTPS são importantes para CSRF, auditoria e URLs absolutas seguras
