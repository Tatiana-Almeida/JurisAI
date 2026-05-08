# Pull Request - Frontend MVP

## Summary

This PR adds the initial JurisAI Frontend MVP in `frontend/`, built with Next.js, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, Axios, Zustand, React Hook Form and Zod.

It introduces a SaaS-style legal interface aligned with the backend architecture and preserves backend stability.

## Included

- JurisAI responsive layout
- Auth foundation
- Protected routes
- Organization context
- Tenant-aware query keys
- Cache invalidation on organization switch
- Dashboard
- Clients
- Cases
- Documents and upload
- OCR flows
- OCR settings/audit/page results
- OCR to Knowledge Base foundation
- Knowledge Base search/ask/sources
- Deadlines
- Calendar
- Finance
- Billing readiness
- Settings
- Client Portal
- Frontend tests and E2E smoke tests

## Validation

Backend:

- `python manage.py check`
- `python -m pytest`

Frontend:

- `npm run typecheck`
- `npm run lint`
- `npm run test`
- `npm run build`
- `npm run test:e2e`

## Known limitations

- Billing checkout is not production-ready.
- AI commercial workflows still depend on backend/provider readiness.
- Worker Celery is pending on Render Free.
- Frontend auth still needs `HttpOnly` cookie hardening before production.
- Upload persistence requires external storage for production/staging stability.
- Next.js middleware should be migrated to `proxy.ts` before stable production.

## Review focus

- API endpoint alignment
- Tenant isolation
- Auth flow
- DRF error mapping
- Billing honesty
- OCR/Knowledge Base UX
- Build/test reliability
