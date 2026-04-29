# Checkpoint — Deployment Security Hardening

## Objetivo

Corrigir riscos críticos de infraestrutura, segurança e deploy antes da preparação da futura `v1.0.0-rc.1`, sem alterar funcionalidades de negócio nem quebrar endpoints existentes.

## Problemas corrigidos

- `collectstatic` deixava de ser obrigatório no build Docker
- Redis sem password
- Flower sem autenticação
- dependências Python sem pins exatos
- falta de binários nativos para OCR no container
- ausência de healthchecks suficientes no `docker-compose`
- `pytest` com `--reuse-db` por default
- ficheiro com nome problemático no repositório

## Arquivos alterados

- `Dockerfile`
- `entrypoint.sh`
- `docker-compose.yml`
- `.dockerignore`
- `.env.example`
- `requirements.txt`
- `pytest.ini`
- `jurisai/settings.py`
- `README.md`
- `docs/06-security/security-audit.md`
- `docs/08-tests/recommended-test-cases.md`
- `docs/09-improvements/change-log.md`
- `docs/00-project/JURISAI_MASTER_PROMPT.md`

## Testes

- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python -m pytest`
- `docker compose config`
- `docker compose build` quando Docker estiver disponivel

## Riscos restantes

- Docker ainda depende de segredos reais fora do repositório para produção
- Flower deve continuar atrás de VPN ou reverse proxy privado
- healthchecks de worker/Flower precisam validação operacional em ambiente mais próximo de produção
- OCR nativo continua dependente do runtime do host/container

## Próximos passos

- validar `docker compose up` completo com smoke operacional
- preparar checklist de deploy para `v1.0.0-rc.1`
- endurecer observabilidade e monitorização de produção
