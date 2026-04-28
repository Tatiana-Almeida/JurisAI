# JurisAI Backend

Backend SaaS jurídico pronto para produção com Django, DRF, PostgreSQL, Redis, Celery e integração de IA.

## Recursos

- Multi-tenant por organização
- Autenticação JWT com refresh
- Gestão de usuários, casos, prazos, documentos, pagamentos e auditoria
- Assistente de IA com geração de petições, resumo de documentos, análise de risco e pesquisa de jurisprudência
- Tarefas assíncronas com Celery
- Documentação Swagger e Redoc

## Estrutura de pastas

- `accounts/`: usuários e controle de acesso
- `organizations/`: dados de escritórios jurídicos e planos
- `law_cases/`: processos jurídicos e fluxo de casos
- `deadlines/`: prazos processuais e alertas
- `documents/`: uploads, versionamento e modelos de documentos
- `ai_assistant/`: integração OpenAI e RAG-ready
- `billing/`: pagamentos e faturamento
- `notifications/`: envio de email e WhatsApp mock
- `audit_logs/`: trilha completa de auditoria
- `jurisai/`: configuração Django, middleware, permissões e Celery

## Como rodar com Docker

1. Copie o arquivo `.env.example` para `.env` e configure as variáveis.
2. Construa e suba os serviços:
   ```bash
docker compose up --build
```
3. Acesse:
   - API: `http://localhost:8000/api/v1/`
   - Swagger: `http://localhost:8000/swagger/`
   - Flower: `http://localhost:5555`

## Fluxo Docker / Compose

1. Crie o arquivo `.env` a partir do `.env.example`:

```bash
copy .env.example .env
```

2. Suba PostgreSQL e Redis:

```bash
docker compose up -d db redis
```

3. Execute migrações e seed:

```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_demo
```

4. Alternativa tudo em um passo com o comando customizado:

```bash
docker compose run --rm web python manage.py setup_local
```

Observação:
- O host `db` é esperado neste fluxo porque ele existe dentro do `docker-compose`.

## Fluxo local leve com SQLite

Use este fluxo apenas para desenvolvimento local fora do Docker/Compose.

1. Crie o arquivo `.env` a partir do `.env.example` e ative SQLite explicitamente:

```bash
copy .env.example .env
```

Edite o `.env` e defina:

```env
DJANGO_USE_SQLITE=True
```

2. Rode as migrações localmente:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py migrate
```

3. Se quiser carregar dados de demonstração:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py seed_demo
```

4. Rode os testes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Observações:
- `DJANGO_USE_SQLITE=True` deve continuar sendo explícito; ele não é fallback automático.
- Não use `DJANGO_USE_SQLITE=True` em produção.

## Endpoints principais

- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/users/`
- `GET /api/v1/cases/`
- `GET /api/v1/deadlines/`
- `GET /api/v1/documents/`
- `GET /api/v1/payments/`
- `GET /api/v1/audit-logs/`
- `POST /api/v1/ai/generate-petition/`
- `POST /api/v1/ai/summarize-document/`
- `POST /api/v1/ai/analyze-risk/`
- `POST /api/v1/ai/search-jurisprudence/`

## Testes

```bash
pytest
```

## Observações

- O serviço de WhatsApp é mock, mas estruturado para integração real futura.
- O módulo de IA está preparado para RAG com `ai_assistant.services.vector_store.VectorStore`.
