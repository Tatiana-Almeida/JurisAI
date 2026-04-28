---
name: security-audit-backend
description: Auditar a segurança de um backend existente verificando autenticação, autorização, validações, exposição de dados, uploads, secrets e endpoints públicos. Use quando for preciso encontrar riscos sem alterar o sistema de imediato.
---

# Objetivo da skill

Identificar riscos de segurança técnicos e de desenho no backend existente e documentá-los com priorização.

## Quando usar

- Quando for necessária uma auditoria de segurança do código.
- Quando houver dúvidas sobre permissões, endpoints públicos, tokens ou isolamento de dados.
- Quando for preciso gerar `docs/06-security/security-audit.md`.

## Quando não usar

- Quando a tarefa for só documentar funcionalidades.
- Quando a análise for puramente de estilo de código sem foco em risco.

## Entradas esperadas

- Código do backend
- Configurações de autenticação e secrets
- Rotas públicas e privadas
- Dependências e upload handlers

## Processo passo a passo

1. Mapear autenticação, autorização e endpoints públicos.
2. Revisar validação de entrada, serialização e exposição de dados sensíveis.
3. Verificar passwords, tokens, secrets, logs, uploads, CORS, rate limiting e variáveis de ambiente.
4. Revisar riscos de injeção, permissões incorretas e isolamento de tenant.
5. Catalogar riscos com `SEC-001`, severidade e evidência.
6. Gerar `docs/06-security/security-audit.md`.
7. Separar claramente:
   - risco confirmado
   - risco inferido
   - ponto que precisa validação manual

## Ficheiros e pastas que deve analisar

- Auth, permissions, guards, policies
- Views/controllers e endpoints públicos
- Serializers/validators
- Configuração do framework e middlewares
- Uploads, storage, logging e exception handlers
- Dependências e arquivos de ambiente

## Documentos que deve gerar

- `docs/06-security/security-audit.md`

## Regras de segurança

- Nunca corrigir automaticamente risco alto sem validação humana.
- Nunca expor secrets em documentação.
- Nunca alterar autenticação/autorização nesta etapa.

## Regras de qualidade

- Cada risco deve ter ID, severidade, evidência e recomendação.
- Diferenciar ausência de evidência de evidência de ausência.
- Priorizar riscos que afetem dados, tenants, identidade e cobrança.

## Formato de saída

- Markdown com tabela:
  - ID
  - Risco
  - Severidade
  - Evidência
  - Impacto
  - Recomendação
  - Estado

## Exemplos de documentação

- `SEC-001`: endpoint público sem validação de assinatura.
- `SEC-002`: ausência de rate limiting observável.
- `SEC-003`: falta de validação cruzada entre tenant e foreign key.

## Critérios de validação

- Autenticação, autorização e endpoints públicos foram revisados.
- Há classificação por severidade.
- Riscos de dados sensíveis e isolamento foram cobertos.
- Recomendações não alteram o sistema sem autorização.

