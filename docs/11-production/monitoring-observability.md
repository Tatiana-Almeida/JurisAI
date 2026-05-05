# Monitoring and Observability

## Base mínima

- healthcheck público em `/health/`
- logs Docker
- logs do `web`
- logs do `worker`
- logs do OCR pipeline
- logs de RAG retrieval
- Flower privado

## Comandos úteis

- `docker compose -f docker-compose.staging.yml logs web --tail=100`
- `docker compose -f docker-compose.staging.yml logs worker --tail=100`
- `docker compose -f docker-compose.staging.yml logs flower --tail=100`
- `docker compose -f docker-compose.staging.yml logs db --tail=100`
- `docker compose -f docker-compose.staging.yml logs redis --tail=100`

## Alertas mínimos

- app down
- db down
- redis down
- worker down
- disk usage
- failed OCR jobs
- failed IndexingJob

## Observabilidade atual

- `/health/` fornece sinal simples de disponibilidade
- OCR já possui audit logs, jobs, results e page-level observability
- RAG já possui indexing jobs e retrieval metadata

## Futuro opcional

- Sentry via `SENTRY_DSN`
- métricas de CPU, memória e disco
- agregação centralizada de logs
- dashboards operacionais por tenant ou por pipeline
