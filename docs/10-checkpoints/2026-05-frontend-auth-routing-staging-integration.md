# Checkpoint — Frontend Auth Routing and Staging Integration

## Objetivo

Endurecer autenticação, proteção de rotas, integração com staging e UX inicial do Frontend MVP usando o backend real do JurisAI.

## Alterações

- [CONFIRMADO_NO_CODIGO] Foi criado `frontend/middleware.ts` com redirecionamento inicial baseado em session hint cookie para `/login` e `/dashboard`.
- [CONFIRMADO_NO_CODIGO] Foi criado `frontend/components/auth/protected-route.tsx` para proteção client-side de rotas privadas e do portal.
- [CONFIRMADO_NO_CODIGO] `auth-store` passou a suportar `bootstrapAuth()`, estados `idle/loading/authenticated/unauthenticated` e `logout()` com limpeza de sessão e cache.
- [CONFIRMADO_NO_CODIGO] `organization-store` passou a bootstrapar organizações, auto-selecionar tenant único e limpar seleção persistida inválida.
- [CONFIRMADO_NO_CODIGO] O provider de organização passou a limpar cache e redirecionar para `/dashboard` ao trocar tenant.
- [CONFIRMADO_NO_CODIGO] Foi criado `frontend/.env.staging.example` apontando para `https://jurisai-web-wh9d.onrender.com`.
- [CONFIRMADO_NO_CODIGO] Dashboard, cases, clients, documents, OCR, Knowledge Base e billing foram alinhados com estados de erro/indisponibilidade mais robustos.
- [CONFIRMADO_NO_CODIGO] A documentação do frontend passou a explicar route guards, token storage, staging API e limitações atuais.

## Validação

- [CONFIRMADO_NO_CODIGO] `python manage.py check`: passou.
- [CONFIRMADO_NO_CODIGO] `python -m pytest`: passou.
- [CONFIRMADO_NO_CODIGO] `npm run typecheck`: passou.
- [CONFIRMADO_NO_CODIGO] `npm run lint`: passou com warnings conhecidos de React Compiler, sem erros.
- [CONFIRMADO_NO_CODIGO] `npm run test`: passou.
- [CONFIRMADO_NO_CODIGO] `npm run build`: passou.
- [CONFIRMADO_NO_CODIGO] `npm run test:e2e`: passou.
- [CONFIRMADO_NO_CODIGO] `curl -I https://jurisai-web-wh9d.onrender.com/health/`: respondeu `200 OK`.
- [CONFIRMADO_NO_CODIGO] `curl -i -X POST https://jurisai-web-wh9d.onrender.com/api/v1/auth/token/ -d {}`: respondeu `400 Bad Request` com payload de erro DRF para `email` e `password`.

## Limitações

- [CONFIRMADO_NO_CODIGO] Os tokens ainda ficam em `localStorage`, por isso o `middleware` não consegue validar autenticação real sozinho.
- [CONFIRMADO_NO_CODIGO] O `middleware` usa apenas um cookie de sessão auxiliar para evitar parte dos acessos indevidos e melhorar UX de redirecionamento.
- [PRECISA_VALIDAR] O login completo com credenciais reais de staging não foi automatizado no repositório porque não podem existir credenciais commitadas.
- [CONFIRMADO_NO_CODIGO] Billing continua sem checkout real, webhook comercial completo e enforcement de subscrição.

## Próximos passos

1. Validar login completo com credenciais reais fora do repositório.
2. Evoluir para cookies `httpOnly` quando o backend suportar esse fluxo.
3. Refinar UX autenticada por módulo com dados reais de staging.
4. Avançar para edição/detalhe completo dos principais fluxos jurídicos.
