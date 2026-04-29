# Production Readiness Checklist

## Secrets
- `DJANGO_SECRET_KEY` definido por variável de ambiente
- `JWT_SIGNING_KEY` definido por variável de ambiente
- `POSTGRES_PASSWORD` forte
- `REDIS_PASSWORD` forte
- `FLOWER_PASSWORD` forte
- `DEBUG=False` em produção

## Network
- Redis sem exposição pública
- Flower atrás de VPN/reverse proxy privado
- Admin protegido
- `CORS_ALLOWED_ORIGINS` explícito
- `CSRF_TRUSTED_ORIGINS` explícito

## Runtime
- containers non-root
- healthcheck ativo
- logs centralizados
- migrations executadas antes do deploy
- `collectstatic` executado apenas em runtime controlado

## TLS / Reverse Proxy
- HTTPS obrigatório
- TLS terminado em proxy confiável
- headers seguros
- domínio configurado
- HSTS avaliado

## Database
- backups automáticos
- restore testado
- migrações testadas
- conexão segura
- retenção definida

## Storage
- media persistente
- permissões corretas
- política de retenção de documentos
- backups de documentos

## OCR/RAG
- Tesseract instalado se usar OCR local real
- Poppler instalado se usar PDF escaneado
- limites por tenant definidos
- providers externos desativados por padrão
- audit logs revisados

## Monitoring
- healthcheck monitorado
- alertas de erro
- métricas de CPU/memória/disco
- logs de Celery
- logs de OCR pipeline
- logs de RAG retrieval

## Release
- pytest completo passou
- docker compose build passou
- smoke tests passaram
- tag criada
- rollback documentado
