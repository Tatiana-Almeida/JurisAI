# Checkpoint — Backend Stabilization, CI and Healthcheck

## Objetivo

Adicionar uma primeira camada de estabilização backend ao JurisAI com CI em GitHub Actions, healthcheck público simples, verificação de drift de migrations e smoke tests mínimos para preparar futuras releases candidatas a `v1.0.0`.

## Workflow CI

- ficheiro: `.github/workflows/ci.yml`
- gatilhos:
  - `push` em `main`
  - `pull_request` para `main`
- ambiente:
  - Python `3.11`
  - SQLite via `DJANGO_USE_SQLITE=True`
- passos:
  - instalar dependências
  - `python manage.py check`
  - `python manage.py makemigrations --check --dry-run`
  - `python -m pytest`

## Healthcheck

- endpoints:
  - `GET /health/`
  - `GET /api/v1/health/`
- resposta:
  - `status`
  - `service`
  - `version`
- características:
  - público
  - sem autenticação
  - sem exposição de secrets ou dados de tenant

## Testes

- `tests/test_healthcheck.py`
- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- `pytest`

## Limitações

- CI usa SQLite, não replica a stack completa de produção
- healthcheck continua propositalmente simples e não mede componentes externos
- readiness operacional real ainda depende de infraestrutura, observabilidade e runtime nativo de OCR

## Próximos passos

- adicionar smoke tests HTTP adicionais de documentação e rotas públicas seguras
- preparar workflow separado para lint/format quando houver padrão consolidado
- adicionar notas operacionais para deploy e monitorização antes da `v1.0.0-rc.1`
