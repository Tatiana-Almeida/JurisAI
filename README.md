# JurisAI Backend

Backend SaaS juridico com Django, Django REST Framework, PostgreSQL, Redis, Celery e integracao de IA.

## Recursos

- Multi-tenant por organizacao
- Autenticacao JWT com refresh
- Gestao de usuarios, casos, prazos, documentos, pagamentos e auditoria
- Assistente de IA com geracao de peticoes, resumo de documentos, analise de risco e pesquisa de jurisprudencia
- Tarefas assincronas com Celery
- Documentacao Swagger e Redoc

## Expanded Legal Services

- Dashboard juridico
- Portal do cliente
- Tarefas internas
- Agenda juridica
- Templates juridicos
- Financeiro de honorarios
- CRM juridico
- Base de conhecimento / RAG
- IA com fontes
- OCR
- Comparacao de documentos
- Extracao automatica de prazos
- Assinatura eletronica
- BI juridico
- Compliance
- Marketplace

## Estrutura de pastas

- `accounts/`: usuarios e controle de acesso
- `organizations/`: dados de escritorios juridicos e planos
- `law_cases/`: processos juridicos e fluxo de casos
- `deadlines/`: prazos processuais e alertas
- `documents/`: uploads, versionamento e modelos de documentos
- `ai_assistant/`: integracao OpenAI e RAG-ready
- `billing/`: pagamentos e faturamento
- `notifications/`: envio de email e WhatsApp mock
- `audit_logs/`: trilha completa de auditoria
- `tasks/`: tarefas internas, checklist e comentarios
- `dashboard/`: agregacoes read-only por tenant
- `client_portal/`: visibilidade controlada de casos, documentos e mensagens
- `calendar_events/`: agenda juridica e eventos futuros
- `legal_templates/`: templates dinamicos e documentos gerados
- `legal_finance/`: invoices, honorarios, despesas e pagamentos
- `crm/`: fundacao comercial para leads e consultas
- `knowledge_base/`: fundacao RAG por organizacao
- `document_analysis/`: fundacao para comparacao e extracao de prazos
- `ocr/`: fundacao para OCR
- `e_signature/`: fundacao para assinatura eletronica
- `business_intelligence/`: fundacao para relatorios e snapshots
- `compliance/`: fundacao para consentimento, retencao e pedidos LGPD
- `marketplace/`: fundacao para marketplace de modelos
- `jurisai/`: configuracao Django, middleware, permissoes e Celery

## Como rodar com Docker

1. Copie o arquivo `.env.example` para `.env` e configure as variaveis.
2. Construa e suba os servicos:

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

3. Execute migracoes e seed:

```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_demo
```

4. Alternativa tudo em um passo com o comando customizado:

```bash
docker compose run --rm web python manage.py setup_local
```

Observacao:
- O host `db` e esperado neste fluxo porque ele existe dentro do `docker-compose`.

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

2. Rode as migracoes localmente:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py migrate
```

3. Se quiser carregar dados de demonstracao:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py seed_demo
```

4. Rode os testes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Observacoes:
- `DJANGO_USE_SQLITE=True` deve continuar sendo explicito; ele nao e fallback automatico.
- Nao use `DJANGO_USE_SQLITE=True` em producao.

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
- `GET /api/v1/dashboard/summary/`
- `GET /api/v1/client-portal/cases/`
- `GET /api/v1/client-portal/documents/`
- `GET /api/v1/tasks/`
- `GET /api/v1/calendar/events/`
- `GET /api/v1/legal-templates/`
- `GET /api/v1/legal-finance/summary/`

## Testes

```bash
pytest
```

## Observacoes

- O servico de WhatsApp e mock, mas estruturado para integracao real futura.
- O modulo de IA esta preparado para RAG com `ai_assistant.services.vector_store.VectorStore`.
