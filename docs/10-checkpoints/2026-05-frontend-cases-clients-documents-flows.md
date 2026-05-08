# Checkpoint — Frontend Cases, Clients and Documents Flows

## Objetivo

Integrar fluxos reais de Processos, Clientes e Documentos no Frontend MVP com autenticação, organização ativa, formulários validados e backend real do JurisAI.

## Endpoints integrados

- [CONFIRMADO_NO_CODIGO] Clientes usam `GET/POST /api/v1/users/` com papel `cliente`.
- [CONFIRMADO_NO_CODIGO] Processos usam `GET/POST /api/v1/cases/`, `GET /api/v1/cases/{id}/` e `PATCH /api/v1/cases/{id}/`.
- [CONFIRMADO_NO_CODIGO] Documentos usam `GET/POST /api/v1/documents/` e `GET /api/v1/documents/{id}/`.
- [CONFIRMADO_NO_CODIGO] Ações de OCR usam `POST /api/v1/ocr/documents/{document_id}/run/` e `POST /api/v1/ocr/documents/{document_id}/advanced-run/`.

## Multi-tenancy

- [CONFIRMADO_NO_CODIGO] Todas as queries jurídicas continuam com `organizationId` nas query keys.
- [CONFIRMADO_NO_CODIGO] Queries dependentes de tenant continuam desativadas quando não existe organização ativa.
- [CONFIRMADO_NO_CODIGO] As páginas mostram um estado explícito de “Selecione uma organização” em vez de manter dados antigos ou disparar consultas indevidas.
- [CONFIRMADO_NO_CODIGO] A troca de organização continua a limpar cache do TanStack Query.

## Formulários

- [CONFIRMADO_NO_CODIGO] Clientes usam React Hook Form + Zod e mapeamento de erros DRF por campo.
- [CONFIRMADO_NO_CODIGO] Processos usam React Hook Form + Zod para criação e edição básica.
- [CONFIRMADO_NO_CODIGO] O frontend não inventa campos como tribunal, número de processo ou deadline porque esses campos não existem no serializer atual de `LawCase`.

## Upload

- [CONFIRMADO_NO_CODIGO] O upload de documentos usa `multipart/form-data`.
- [CONFIRMADO_NO_CODIGO] A UI valida extensões compatíveis com o backend: PDF, DOCX, TXT, PNG, JPG e JPEG.
- [CONFIRMADO_NO_CODIGO] A UI apresenta progresso de upload e mensagens específicas para falhas de tamanho/formato quando disponíveis.

## OCR actions

- [CONFIRMADO_NO_CODIGO] O detalhe de documento já permite iniciar OCR normal e OCR avançado.
- [CONFIRMADO_NO_CODIGO] A UI explica que OCR externo continua desativado por padrão.
- [CONFIRMADO_NO_CODIGO] Após iniciar OCR, o fluxo redireciona para `/ocr`.

## Testes

- [CONFIRMADO_NO_CODIGO] `npm run test` cobre clientes, processos, upload e ações de OCR.
- [CONFIRMADO_NO_CODIGO] `npm run build` continua a passar.
- [CONFIRMADO_NO_CODIGO] `npm run test:e2e` continua a validar proteção de rotas privadas.

## Limitações

- [CONFIRMADO_NO_CODIGO] O módulo “Clientes” depende das permissões do endpoint de utilizadores; utilizadores não admin podem receber `403` ao tentar criar clientes.
- [CONFIRMADO_NO_CODIGO] A paginação DRF é suportada na camada de cliente HTTP, mas a navegação visual completa de páginas longas ainda pode ser expandida.
- [PRECISA_VALIDAR] O fluxo autenticado real contra staging continua dependente de credenciais fora do repositório.
- [CONFIRMADO_NO_CODIGO] O worker Celery pode continuar indisponível em staging público Render Free, afetando execução real de OCR.

## Próximos passos

1. Validar os fluxos autenticados com credenciais reais de staging.
2. Expandir paginação navegável e filtros avançados.
3. Refinar edição detalhada de processos e observabilidade de documentos/OCR.
4. Avançar para fluxos reais de Knowledge Base, deadlines e finance.
