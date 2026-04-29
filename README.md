# JurisAI

JurisAI is a multi-tenant legal SaaS backend built with Django REST Framework, designed for law firms and legal departments.

It currently provides core legal operations, initial AI support, SaaS billing, auditability, and the first wave of expanded legal services, while keeping organization isolation as a central architectural rule.

Current milestone: `v0.4.0` extends the tenant-isolated legal RAG foundation with optional local embeddings, hybrid retrieval, explicit source scores and zero external provider calls by default.

Work in progress toward `v0.5.0`: local OCR and document text extraction for `TXT`, textual `PDF` and `DOCX`, still without any external OCR provider.

## Features

### Core legal management

- Organizations and multi-tenancy
- User management and JWT authentication
- Legal cases
- Deadlines
- Documents with upload hardening
- SaaS billing and webhook processing
- Audit logs
- Notifications

### Expanded legal services

- Tasks
- Dashboard
- Client portal
- Legal calendar
- Legal templates
- Legal finance

### AI and automation foundations

- AI assistant
- Knowledge base / RAG with textual retrieval and local embeddings foundation
- OCR and local document text extraction foundation
- Document analysis foundation

### Business foundations

- CRM foundation
- E-signature foundation
- BI foundation
- Compliance foundation
- Marketplace foundation

## Implementation Status

### Implemented modules

- `accounts`
- `organizations`
- `law_cases`
- `deadlines`
- `documents`
- `ai_assistant`
- `billing`
- `notifications`
- `audit_logs`
- `tasks`
- `dashboard`
- `client_portal`
- `calendar_events`
- `legal_templates`
- `legal_finance`
- `knowledge_base`
- `ocr`

### Foundation modules

These apps are present in the codebase with initial models and safe base routes, but are not positioned as complete business features yet:

- `crm`
- `e_signature`
- `business_intelligence`
- `compliance`
- `marketplace`
- `document_analysis`

### Initial RAG capabilities

- Tenant-isolated knowledge bases
- Document indexing into textual chunks
- Local textual retrieval with explicit sources
- Optional deterministic local embeddings via `local-hash-v1`
- Hybrid retrieval foundation combining textual and local embedding scores
- Zero external calls in the active embedding pipeline
- Retrieval ranking improved with exact phrase, term frequency and title hits
- Indexing observability through indexing jobs
- Knowledge base stats and safe document reindexing
- Grounded answers without external provider calls
- `ask` responses with `retrieval_method`, `sources_count`, `confidence`, `effective_retrieval_mode`, `fallback_used` and `fallback_reason`
- `ask` sources with `final_score` and optional `text_score` / `embedding_score`
- Local embedding preparation through `prepare-embeddings`
- Organization-level RAG governance and opt-in controls for future external embeddings
- Mandatory textual fallback when embeddings are not effective
- External providers still disabled by default and not implemented in this phase

### Initial OCR capabilities

- Tenant-scoped OCR jobs and extraction results
- Local text extraction for `TXT`
- Local text extraction for textual `PDF` layers
- Local text extraction for `DOCX`
- Explicit `apply-to-document` flow before changing `Document.content`
- Zero external OCR calls in the active pipeline
- Safe failure for unsupported formats in this phase
- Intended follow-up flow with the knowledge base:
  - run OCR
  - apply extracted text to `Document.content`
  - index the document in `knowledge_base`

### Future functional expansion

- Richer semantic retrieval and vector-backed ranking
- OCR provider integration
- Advanced document comparison and deadline extraction
- Provider-backed electronic signature flows
- Rich BI dashboards and analytics
- Compliance workflows and automation
- Marketplace workflows and purchases

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker
- Pytest
- Swagger
- Redoc

## Project Structure

Main apps currently present in the repository:

- `accounts/`: user accounts, roles, authentication and profile endpoints
- `organizations/`: law firm organizations and plan controls
- `law_cases/`: legal case management
- `deadlines/`: deadline tracking
- `documents/`: document records, uploads and versioning
- `ai_assistant/`: legal AI assistant and related services
- `billing/`: SaaS billing, payments and webhook processing
- `notifications/`: notification flows
- `audit_logs/`: audit trail
- `tasks/`: internal tasks, comments and checklist items
- `dashboard/`: tenant-scoped read-only aggregations
- `client_portal/`: explicit case/document visibility and messaging
- `calendar_events/`: legal calendar and event scheduling
- `legal_templates/`: template management and generated documents
- `legal_finance/`: invoices, fees, expenses and payment records
- `crm/`: lead and consultation foundation
- `e_signature/`: signature request foundation
- `business_intelligence/`: report and metric foundation
- `compliance/`: consent and compliance foundation
- `marketplace/`: marketplace foundation
- `knowledge_base/`: initial tenant-scoped retrieval and source-backed answers
- `ocr/`: local OCR jobs and text extraction foundation
- `document_analysis/`: comparison and extraction foundation
- `jurisai/`: Django settings, permissions, middleware and shared utilities

## Main API Endpoints

Current primary routes include:

- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/users/`
- `GET /api/v1/users/profile/`
- `GET /api/v1/cases/`
- `GET /api/v1/deadlines/`
- `GET /api/v1/documents/`
- `GET /api/v1/payments/`
- `GET /api/v1/audit-logs/`
- `GET /api/v1/tasks/`
- `GET /api/v1/dashboard/summary/`
- `GET /api/v1/client-portal/cases/`
- `GET /api/v1/client-portal/documents/`
- `GET /api/v1/calendar/events/`
- `GET /api/v1/legal-templates/`
- `GET /api/v1/generated-documents/`
- `GET /api/v1/legal-finance/summary/`
- `GET /api/v1/knowledge-base/`
- `POST /api/v1/knowledge-base/{id}/index-document/`
- `POST /api/v1/knowledge-base/{id}/reindex-document/`
- `POST /api/v1/knowledge-base/{id}/search/`
- `POST /api/v1/knowledge-base/{id}/ask/`
- `GET /api/v1/knowledge-base/{id}/stats/`
- `GET /api/v1/knowledge-base/indexing-jobs/`
- `GET/PATCH /api/v1/knowledge-base/settings/`
- `GET /api/v1/knowledge-base/embedding-audit-logs/`
- `POST /api/v1/knowledge-base/{id}/prepare-embeddings/`
- `GET /api/v1/knowledge-base/chunks/`
- `POST /api/v1/ocr/documents/{document_id}/run/`
- `GET /api/v1/ocr/jobs/`
- `GET /api/v1/ocr/results/`
- `POST /api/v1/ocr/results/{id}/apply-to-document/`
- `POST /api/v1/ai/generate-petition/`
- `POST /api/v1/ai/summarize-document/`
- `POST /api/v1/ai/analyze-risk/`
- `POST /api/v1/ai/search-jurisprudence/`

## Getting Started

### Installation

1. Clone the repository.
2. Create a local environment file from the example:

```bash
copy .env.example .env
```

3. Choose one of the supported runtime flows below:
- Docker with PostgreSQL
- Local lightweight mode with SQLite

## Running with Docker

Use this flow when you want the stack closer to the intended deployment shape.

1. Create `.env` from `.env.example`:

```bash
copy .env.example .env
```

2. Start the services:

```bash
docker compose up --build
```

3. Or run the database and supporting services first:

```bash
docker compose up -d db redis
```

4. Apply migrations and load demo data if needed:

```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_demo
```

5. Optional helper command:

```bash
docker compose run --rm web python manage.py setup_local
```

Notes:

- In this flow, the PostgreSQL host `db` is expected to exist via Docker Compose.
- Swagger and Redoc are available only when `DEBUG=True`.

## Running Locally with SQLite

Use this flow for lightweight local development outside Docker.

1. Create `.env` from `.env.example`:

```bash
copy .env.example .env
```

2. Enable SQLite explicitly:

```env
DJANGO_USE_SQLITE=True
```

3. Apply migrations:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py migrate
```

4. Optional demo seed:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py seed_demo
```

5. Run the server:

```powershell
DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py runserver
```

Notes:

- `DJANGO_USE_SQLITE=True` is intentionally explicit and is not an automatic fallback.
- It should not be used for production environments.

## API Docs

- Swagger: `http://localhost:8000/swagger/` when `DEBUG=True`
- Redoc: `http://localhost:8000/redoc/` when `DEBUG=True`

## Tests

Run the full suite with:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The repository currently includes coverage for:

- tenant isolation regressions
- billing webhook security and orchestration
- document upload hardening
- OCR extraction and cross-tenant protections
- expanded legal services phase 1

## Security Notes

The current backend already includes important safety measures:

- Tenant isolation by `organization` across authenticated business queries
- Validation of cross-tenant foreign key relations in serializers
- JWT-based authentication
- Billing webhook signature validation, timestamp validation and idempotency
- Audit logging support
- Upload validation for extension, content type and file size
- Filename sanitization for uploaded documents
- Lightweight binary signature validation for PDF, PNG, JPEG and structural validation for DOCX
- Tenant-isolated knowledge retrieval with explicit source payloads
- No external provider calls for knowledge base retrieval in the current phase
- Indexing jobs and retrieval history stay organization-scoped
- Deterministic local embeddings run fully inside the backend and do not send content to third parties
- Local embeddings are a pipeline foundation and not a semantic/legal model replacement
- Chunk embedding records and audit logs stay organization-scoped
- External embeddings remain disabled by default and require explicit organization opt-in
- Even with external configuration present, provider-backed embeddings remain blocked and fall back safely to textual retrieval
- Textual fallback remains mandatory when retrieval is configured as `hybrid` or `embeddings` but external embeddings are not effective
- OCR extraction is currently fully local for `TXT`, textual `PDF` and `DOCX`
- OCR jobs and OCR results remain organization-scoped
- OCR does not overwrite `Document.content` unless the caller explicitly requests it or applies a stored result
- No document is sent to external OCR providers in the current phase

Remaining production hardening areas include:

- stronger production secret management and key length hygiene
- deeper binary or malware scanning for uploaded files
- broader validation coverage for legacy document formats
- future provider-backed RAG controls, including embeddings governance, consent and retrieval observability
- operational hardening around infrastructure, monitoring and secrets rotation

## Roadmap

- Production hardening
- Embedding-based RAG with stronger local semantics and optional per-tenant external providers
- OCR provider integration for image-based documents
- Advanced CRM workflows
- E-signature provider integration
- BI dashboards
- Compliance workflows
- Marketplace workflows
- Advanced document analysis and extraction pipelines

## Additional Notes

- WhatsApp notification behavior is still mock-oriented.
- Some foundation modules expose safe placeholders and are intentionally not presented as complete features yet.
