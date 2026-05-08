# JurisAI

JurisAI is a multi-tenant legal SaaS backend built with Django REST Framework, designed for law firms and legal departments.

It currently provides core legal operations, initial AI support, billing foundations, auditability, and the first wave of expanded legal services, while keeping organization isolation as a central architectural rule.

Current milestone: `v1.0.0-rc.5` focuses on Render Public Staging Validation, confirming a real public HTTPS deployment for the web service while keeping worker, monitoring, scheduled backups, credential rotation and custom-domain work clearly marked as pending.

## Frontend MVP

- Branch: `feature/frontend-mvp`
- Path: `frontend/`
- Stack: Next.js, TypeScript, Tailwind, shadcn/ui, TanStack Query
- Status: auth routing and staging integration hardening
- Backend remains isolated on `main`

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

## Commercial readiness

Current status:

- Backend foundation: advanced
- Frontend: pending
- Billing: pending
- AI commercial workflows: partial
- Render staging: partial
- Ready for sale: no
- Ready for technical beta: soon

Notes:

- [CONFIRMADO_NO_CODIGO] The first functional frontend foundation now exists under `frontend/` on `feature/frontend-mvp`.
- [CONFIRMADO_NO_CODIGO] Billing currently covers tenant-scoped records plus Stripe-style webhook ingestion, not a complete self-serve checkout and cancellation flow.
- [CONFIRMADO_NO_CODIGO] AI endpoints exist, but the active provider path can still fall back to mock responses when `OPENAI_API_KEY` is not configured.
- [CONFIRMADO_NO_CODIGO] RAG uses deterministic local embeddings via `local-hash-v1`, which validate the retrieval pipeline but do not provide rich semantic legal understanding.
- [PRECISA_VALIDAR] Render staging still depends on provider-side confirmation for WhiteNoise static delivery, admin login after credential rotation, monitoring and scheduled backups.

Frontend MVP status:

- [CONFIRMADO_NO_CODIGO] Login, dashboard, cases, clients, documents, OCR, Knowledge Base, deadlines, calendar, finance, billing, settings and client portal now have initial React pages and shared layout.
- [CONFIRMADO_NO_CODIGO] The frontend respects organization-scoped query keys and clears tenant cache when the active organization changes.
- [CONFIRMADO_NO_CODIGO] Protected routes, auth bootstrap and organization bootstrap now exist in the frontend MVP foundation.
- [CONFIRMADO_NO_CODIGO] Billing UI remains intentionally honest and does not expose a fake checkout flow.
- [CONFIRMADO_NO_CODIGO] A staging environment example now targets `https://jurisai-web-wh9d.onrender.com` for frontend integration.
- [PRECISA_VALIDAR] A production-grade browser flow still depends on authenticated staging data and final UX refinement.
- [CONFIRMADO_NO_CODIGO] O frontend staging publico foi publicado em `https://frontend-phi-five-90.vercel.app`.
- [PRECISA_VALIDAR] O login real em browser ainda depende de ajustar `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` no backend Render para a origem do frontend publicado.
- [CONFIRMADO_NO_CODIGO] O parser de `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` no backend ja suporta multiplas origens separadas por virgula.

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
- `local-hash-v1` is deterministic and local, but it is not a true semantic embedding model and may miss legally similar passages expressed with different vocabulary

### Initial OCR capabilities

- Tenant-scoped OCR jobs and extraction results
- Local text extraction for `TXT`
- Local text extraction for textual `PDF` layers
- Local text extraction for `DOCX`
- Optional local image OCR foundation via Tesseract adapter when available
- Optional local scanned PDF OCR foundation when `pdf2image` and native tooling are available
- Explicit `apply-to-document` flow before changing `Document.content`
- Controlled OCR-to-Knowledge-Base pipeline with explicit `update_document_content=true`
- Zero external OCR calls in the active pipeline
- Safe failure for unsupported formats in this phase
- Supported explicit ingestion flow:
  - run OCR
  - apply extracted text to `Document.content`
  - index the document in `knowledge_base`
  - ask with mandatory `sources`

### Advanced OCR governance

- Organization-level OCR settings
- External OCR disabled by default
- Explicit opt-in required before any future external OCR provider
- Advanced OCR audit logs for image and scanned-PDF attempts
- Placeholder `advanced-run` flow with zero external calls in this phase
- No document content leaves the system in the current advanced OCR foundation

### Local image OCR engine foundation

- Optional local image OCR via a governed Tesseract adapter
- `advanced-run` can execute local OCR for `PNG`, `JPG` and `JPEG` when tenant settings explicitly allow local mode
- Safe failure when the local OCR engine or native Tesseract binary is not available
- No external OCR calls in the local image OCR path

### Local scanned PDF OCR foundation

- Optional local scanned PDF OCR via `pdf2image` plus the governed Tesseract adapter
- `advanced-run` can attempt scanned PDF OCR when tenant settings explicitly allow local mode
- Safe failure when `pdf2image`, Poppler or Tesseract are not available
- No external OCR calls in the scanned PDF OCR path
- Tests validate the adapter and flow with mocks, not with mandatory native binaries

### OCR observability and tenant limits

- `OCRSettings` now supports tenant-level limits for scanned PDF pages, OCR file size and OCR output length
- `OCRPageResult` stores page-level OCR results when the tenant keeps page observability enabled
- Scanned PDF OCR can truncate oversized output safely and records `output_truncated` metadata
- Large OCR files fail safely before processing and generate audit logs instead of crashing
- Result pages stay organization-scoped through `GET /api/v1/ocr/page-results/` and `GET /api/v1/ocr/results/{id}/pages/`

### Scanned PDF OCR to KnowledgeBase pipeline

- The OCR pipeline still tries standard textual PDF extraction first
- When textual PDF extraction is empty and the tenant enables `scanned_pdf_ocr_mode="local"`, the pipeline can fall back to governed local scanned PDF OCR
- `update_document_content=true` remains mandatory before indexing
- The pipeline now exposes whether advanced OCR was used and the related audit log reference
- No external provider is called anywhere in the fallback path

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
- `POST /api/v1/ocr/documents/{document_id}/advanced-run/`
- `GET /api/v1/ocr/jobs/`
- `GET /api/v1/ocr/results/`
- `GET /api/v1/ocr/page-results/`
- `GET /api/v1/ocr/results/{id}/pages/`
- `POST /api/v1/ocr/results/{id}/apply-to-document/`
- `POST /api/v1/ocr/pipelines/knowledge-base/`
- `GET /api/v1/ocr/pipelines/`
- `GET/PATCH /api/v1/ocr/settings/`
- `GET /api/v1/ocr/audit-logs/`
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

Notes:

- The Docker image no longer runs `collectstatic` during build.
- Static collection can run at runtime only when `RUN_COLLECTSTATIC=True`.
- The runtime image now includes native OCR binaries such as `tesseract-ocr` and `poppler-utils`.
- The application containers now run as a non-root user inside the image.
- Redis should be protected with `REDIS_PASSWORD`.
- Redis is intended to stay private on the internal Docker network and is no longer exposed publicly by default.
- Flower should be protected with `FLOWER_USER` and `FLOWER_PASSWORD` and kept behind a VPN or reverse proxy in production.

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

## Continuous Integration

The repository now includes GitHub Actions CI at `.github/workflows/ci.yml`.

The CI pipeline runs with SQLite for simplicity and stability and executes:

- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python -m pytest`

This keeps the backend validation lightweight and independent from external services.

The CI workflow currently runs with SQLite and validates:

- Django settings integrity
- migration drift
- the full automated test suite

## Healthcheck

A lightweight public healthcheck is available at:

- `GET /health/`
- `GET /api/v1/health/`

It returns a simple payload with service status and version and does not expose secrets or tenant data.

## Staging Deployment

The staging track now spans:

- `v1.0.0-rc.2`: staging compose and operational documentation
- `v1.0.0-rc.3`: real local runtime validation with Docker daemon active
- `v1.0.0-rc.4`: HTTPS, reverse proxy, monitoring and backup scheduling guidance
- `v1.0.0-rc.5`: initial public Render staging validation over HTTPS

The main staging artifacts are:

- [docker-compose.staging.yml](/c:/projectos/JurisAI/docker-compose.staging.yml)
- [.env.staging.example](/c:/projectos/JurisAI/.env.staging.example)
- [docs/11-production/staging-deployment-guide.md](/c:/projectos/JurisAI/docs/11-production/staging-deployment-guide.md)
- [docs/11-production/staging-caddy-example.md](/c:/projectos/JurisAI/docs/11-production/staging-caddy-example.md)
- [docs/11-production/production-readiness-checklist.md](/c:/projectos/JurisAI/docs/11-production/production-readiness-checklist.md)
- [docs/11-production/backup-restore.md](/c:/projectos/JurisAI/docs/11-production/backup-restore.md)
- [docs/11-production/backup-schedule.md](/c:/projectos/JurisAI/docs/11-production/backup-schedule.md)
- [docs/11-production/monitoring-observability.md](/c:/projectos/JurisAI/docs/11-production/monitoring-observability.md)
- [docs/11-production/staging-monitoring-validation.md](/c:/projectos/JurisAI/docs/11-production/staging-monitoring-validation.md)
- [docs/11-production/rollback-checklist.md](/c:/projectos/JurisAI/docs/11-production/rollback-checklist.md)
- [docs/10-checkpoints/2026-05-render-public-staging-validation.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-05-render-public-staging-validation.md)

This staging baseline keeps:

- `DEBUG=False`
- Redis private on the internal Docker network
- Flower private on the internal Docker network
- healthchecks enabled
- secrets outside the repository

Current public-layer status:

- local runtime and HTTP healthchecks were validated in `v1.0.0-rc.3`
- public HTTPS is now reachable on Render at `https://jurisai-web-wh9d.onrender.com`
- `/health/` responds publicly and `/admin/` reaches the Django Admin login flow on Render
- worker Celery, external monitoring, scheduled backups, credential rotation and custom domain are still pending
- `web` should continue to stay behind a reverse proxy or managed platform edge, without exposing Redis/PostgreSQL/Flower publicly
- Render Free does not provide an interactive Shell, so admin bootstrap currently depends on the opt-in `bootstrap_superuser` management command executed by `entrypoint.sh`
- After the first successful Render admin login, `DJANGO_CREATE_SUPERUSER` should be set back to `False` and `DJANGO_SUPERUSER_PASSWORD` should be removed from the Render environment
- Render Free does not provide Shell or pre-deploy commands, so `RUN_MIGRATIONS=True` is the supported way to run `migrate --noinput` during startup
- `DATABASE_URL` from Render Postgres has priority over `POSTGRES_HOST=db` and the other `POSTGRES_*` fallbacks
- `bootstrap_superuser` now runs after startup migrations and before the main process command
- Render/Gunicorn requires WhiteNoise to serve Django static files with `DEBUG=False`
- `RUN_COLLECTSTATIC=True` must be enabled in Render/staging deployments with `DEBUG=False`
- After deploy, `/static/admin/js/theme.js` should return JavaScript instead of `404`
- [PRECISA_VALIDAR] Public revalidation of `/static/admin/js/theme.js`, `/admin/` login POST and rotated database credentials still depends on the current Render deployment state

## Production Readiness Notes

- CI currently validates Django checks, migration drift and the full test suite using SQLite.
- The public healthcheck is intentionally simple and avoids sensitive runtime details.
- Production deployment still needs environment-specific hardening for infrastructure, monitoring, secrets rotation and native OCR dependencies.
- Runtime containers now run as non-root by default, reducing the blast radius of process compromise.
- Optional local OCR paths for image and scanned PDF continue to rely on native tooling such as Tesseract and Poppler in the runtime environment.
- Redis and Flower credentials in `.env.example` are placeholders only and must be replaced with real secrets outside the repository.
- Redis should remain internal to the Docker network unless there is an explicit operational need to expose it.
- `pytest` no longer uses `--reuse-db` by default; that flag can still be used manually in local debugging when desired.
- The production rollout checklist is documented in [docs/11-production/production-readiness-checklist.md](/c:/projectos/JurisAI/docs/11-production/production-readiness-checklist.md).
- The release candidate checklist for `v1.0.0-rc.1` is documented in [docs/11-production/release-candidate-checklist.md](/c:/projectos/JurisAI/docs/11-production/release-candidate-checklist.md).
- The staging deployment guide for `v1.0.0-rc.2` is documented in [docs/11-production/staging-deployment-guide.md](/c:/projectos/JurisAI/docs/11-production/staging-deployment-guide.md).
- Reverse proxy and TLS notes are documented in [docs/11-production/reverse-proxy-tls.md](/c:/projectos/JurisAI/docs/11-production/reverse-proxy-tls.md).
- A concrete Caddy example for staging is documented in [docs/11-production/staging-caddy-example.md](/c:/projectos/JurisAI/docs/11-production/staging-caddy-example.md).
- Backup and restore notes are documented in [docs/11-production/backup-restore.md](/c:/projectos/JurisAI/docs/11-production/backup-restore.md).
- Backup scheduling guidance is documented in [docs/11-production/backup-schedule.md](/c:/projectos/JurisAI/docs/11-production/backup-schedule.md).
- Monitoring validation guidance is documented in [docs/11-production/staging-monitoring-validation.md](/c:/projectos/JurisAI/docs/11-production/staging-monitoring-validation.md).
- Rollback steps are documented in [docs/11-production/rollback-checklist.md](/c:/projectos/JurisAI/docs/11-production/rollback-checklist.md).
- Render bootstrap and credential-rotation notes are documented in [docs/10-checkpoints/2026-05-render-superuser-bootstrap.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-05-render-superuser-bootstrap.md).
- Render database URL and startup migration notes are documented in [docs/10-checkpoints/2026-05-render-database-url-and-migrations.md](/c:/projectos/JurisAI/docs/10-checkpoints/2026-05-render-database-url-and-migrations.md).

## Tests

Run the full suite with:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The repository currently includes coverage for:

- full backend regression validation for the `v1.0.0-rc.2` candidate with `192 passed`
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
- OCR-to-Knowledge-Base pipeline requires explicit `update_document_content=true` before indexing
- No document is sent to external OCR providers in the current phase
- Advanced OCR settings are organization-scoped and default to a fully disabled external OCR posture
- Image/scanned-PDF advanced OCR attempts are audited without storing raw extracted content
- Local image OCR can use an optional Tesseract adapter entirely inside the backend when the tenant enables local mode
- If Tesseract or the optional Python bindings are unavailable, the backend returns a controlled failure and records an audit log instead of crashing
- Scanned PDF advanced OCR can attempt local rasterization and OCR when the tenant enables local mode
- If `pdf2image` or Poppler are unavailable, scanned PDF OCR returns a controlled failure and records an audit log instead of crashing
- The OCR-to-KnowledgeBase pipeline now falls back to governed scanned PDF OCR only when standard textual PDF extraction is not useful and tenant settings explicitly allow local scanned PDF OCR
- Tenant OCR settings can cap scanned PDF pages, OCR file size and OCR output size to avoid uncontrolled resource usage
- Page-level scanned PDF OCR observability is optional per tenant and remains organization-scoped

Remaining production hardening areas include:

- stronger production secret management and key length hygiene
- deeper binary or malware scanning for uploaded files
- broader validation coverage for legacy document formats
- future provider-backed RAG controls, including embeddings governance, consent and retrieval observability
- operational hardening around infrastructure, monitoring and secrets rotation

## Roadmap

- Production hardening
- Embedding-based RAG with stronger local semantics and optional per-tenant external providers
- Stronger local OCR quality and observability for scanned PDFs
- Controlled scanned PDF OCR-to-KnowledgeBase automation and observability
- Advanced CRM workflows
- E-signature provider integration
- BI dashboards
- Compliance workflows
- Marketplace workflows
- Advanced document analysis and extraction pipelines

## Additional Notes

- WhatsApp notification behavior is still mock-oriented.
- Some foundation modules expose safe placeholders and are intentionally not presented as complete features yet.
