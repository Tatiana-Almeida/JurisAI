# IMP-001 Tenant Validation Plan

## 1. Resumo da melhoria

- [CONFIRMADO_NO_CÓDIGO] A melhoria `IMP-001` tem como objetivo impedir associações cruzadas entre tenants durante a criação de entidades que referenciam outras entidades por foreign key.
- [CONFIRMADO_NO_CÓDIGO] O foco principal está em validar que relações como `client_id`, `lawyer_id` e `law_case_id` pertencem à mesma `organization` do utilizador autenticado.
- [INFERIDO_DO_CÓDIGO] A intenção arquitetural atual do backend é multi-tenant por organização, mas essa intenção ainda não é garantida uniformemente na validação de entrada.

## 2. Problema atual

- [CONFIRMADO_NO_CÓDIGO] As views filtram querysets por `request.user.organization`, o que protege leituras em vários endpoints.
- [CONFIRMADO_NO_CÓDIGO] Os serializers de `LawCase`, `Deadline` e `Document` resolvem `organization_id` a partir do contexto/autenticação.
- [CONFIRMADO_NO_CÓDIGO] Esses mesmos serializers não validam se os IDs relacionados recebidos pertencem à mesma organização do tenant atual.
- [CONFIRMADO_NO_CÓDIGO] Isso cria superfície para bypass por foreign keys: um utilizador pode potencialmente associar um recurso novo a um `User` ou `LawCase` de outra organização, desde que conheça o UUID.
- [INFERIDO_DO_CÓDIGO] O risco é alto porque esse tipo de falha compromete o boundary central do produto SaaS.

## 3. Evidências no código

### 3.1 Serializers com relações por ID

- [CONFIRMADO_NO_CÓDIGO] [law_cases/serializers.py](/c:/projectos/JurisAI/law_cases/serializers.py) aceita:
  - `client_id`
  - `lawyer_id`
  - `organization_id`
- [CONFIRMADO_NO_CÓDIGO] [deadlines/serializers.py](/c:/projectos/JurisAI/deadlines/serializers.py) aceita:
  - `law_case_id`
  - `organization_id`
- [CONFIRMADO_NO_CÓDIGO] [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py) aceita:
  - `law_case_id`
  - `organization_id`

### 3.2 Validações já existentes

- [CONFIRMADO_NO_CÓDIGO] [jurisai/serializers.py](/c:/projectos/JurisAI/jurisai/serializers.py) centraliza a resolução de `organization_id` via `OrganizationScopedValidationMixin`.
- [CONFIRMADO_NO_CÓDIGO] As views abaixo limitam listagens à organização do utilizador:
  - [law_cases/views.py](/c:/projectos/JurisAI/law_cases/views.py)
  - [deadlines/views.py](/c:/projectos/JurisAI/deadlines/views.py)
  - [documents/views.py](/c:/projectos/JurisAI/documents/views.py)
- [CONFIRMADO_NO_CÓDIGO] Há validações de limite por plano em criação:
  - casos
  - documentos

### 3.3 Validações ausentes

- [CONFIRMADO_NO_CÓDIGO] Não há verificação explícita de que:
  - `client_id` pertence à mesma organização do caso a ser criado
  - `lawyer_id` pertence à mesma organização do caso a ser criado
  - `law_case_id` pertence à mesma organização do prazo a ser criado
  - `law_case_id` pertence à mesma organização do documento a ser criado

## 4. Superfície de impacto

## 4.1 Endpoints afetados

| Endpoint | Método | Superfície | Estado |
|---|---|---|---|
| `API-016 /api/v1/cases/` | POST | criação com `client_id` e `lawyer_id` | [CONFIRMADO_NO_CÓDIGO] |
| `API-018 /api/v1/deadlines/` | POST | criação com `law_case_id` | [CONFIRMADO_NO_CÓDIGO] |
| `API-021 /api/v1/documents/` | POST | criação com `law_case_id` | [CONFIRMADO_NO_CÓDIGO] |

### 4.2 Entidades afetadas

| Entidade | Papel na melhoria | Estado |
|---|---|---|
| `ENT-002 User` | origem de `client_id` e `lawyer_id` | [CONFIRMADO_NO_CÓDIGO] |
| `ENT-003 LawCase` | destino da criação e origem de `law_case_id` | [CONFIRMADO_NO_CÓDIGO] |
| `ENT-004 Deadline` | destino da criação dependente de `LawCase` | [CONFIRMADO_NO_CÓDIGO] |
| `ENT-005 Document` | destino da criação dependente de `LawCase` | [CONFIRMADO_NO_CÓDIGO] |
| `ENT-001 Organization` | tenant boundary | [CONFIRMADO_NO_CÓDIGO] |

### 4.3 Ficheiros provavelmente afetados

- [law_cases/serializers.py](/c:/projectos/JurisAI/law_cases/serializers.py)
- [deadlines/serializers.py](/c:/projectos/JurisAI/deadlines/serializers.py)
- [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py)
- [tests/test_api.py](/c:/projectos/JurisAI/tests/test_api.py)
- [docs/06-security/security-audit.md](/c:/projectos/JurisAI/docs/06-security/security-audit.md)
- [docs/08-tests/recommended-test-cases.md](/c:/projectos/JurisAI/docs/08-tests/recommended-test-cases.md)
- [docs/09-improvements/change-log.md](/c:/projectos/JurisAI/docs/09-improvements/change-log.md)

- [PRECISA_VALIDAR] Pode ser útil criar um utilitário novo de validação compartilhada em `jurisai/` ou módulo comum, mas isso depende da estratégia escolhida.

## 5. Quais relações podem permitir associação cruzada entre tenants

### 5.1 `LawCaseSerializer`

- [CONFIRMADO_NO_CÓDIGO] `LawCaseSerializer.create()` grava diretamente:
  - `client_id=validated_data['client_id']`
  - `lawyer_id=validated_data['lawyer_id']`
  - `organization_id=validated_data['organization_id']`
- [CONFIRMADO_NO_CÓDIGO] Não existe validação prévia de que `client.organization_id == organization_id`.
- [CONFIRMADO_NO_CÓDIGO] Não existe validação prévia de que `lawyer.organization_id == organization_id`.
- [INFERIDO_DO_CÓDIGO] Também não existe validação explícita de papel adequado para `client` e `lawyer` no serializer de criação.

### 5.2 `DeadlineSerializer`

- [CONFIRMADO_NO_CÓDIGO] `DeadlineSerializer.create()` grava `law_case_id` e `organization_id` separadamente.
- [CONFIRMADO_NO_CÓDIGO] Não existe validação prévia de que `LawCase.organization_id == organization_id`.

### 5.3 `DocumentSerializer`

- [CONFIRMADO_NO_CÓDIGO] `DocumentSerializer.create()` grava `law_case_id` e `organization_id` separadamente.
- [CONFIRMADO_NO_CÓDIGO] Não existe validação prévia de que `LawCase.organization_id == organization_id`.
- [CONFIRMADO_NO_CÓDIGO] O versionamento consulta `Document.objects.filter(law_case_id=...)` sem validar tenant antes da criação.

## 6. Quais validações já existem

- [CONFIRMADO_NO_CÓDIGO] `OrganizationScopedValidationMixin` resolve `organization_id` a partir de `context['organization']` ou `request.user.organization_id`.
- [CONFIRMADO_NO_CÓDIGO] `IsOrganizationMember` exige utilizador autenticado com organização.
- [CONFIRMADO_NO_CÓDIGO] `get_queryset()` das views de casos, prazos e documentos filtra por organização.
- [CONFIRMADO_NO_CÓDIGO] `perform_create()` nas views de casos/documentos aplica regras de limite por plano.

## 7. Quais validações estão ausentes

- [CONFIRMADO_NO_CÓDIGO] Coerência entre `organization_id` e `client_id`.
- [CONFIRMADO_NO_CÓDIGO] Coerência entre `organization_id` e `lawyer_id`.
- [CONFIRMADO_NO_CÓDIGO] Coerência entre `organization_id` e `law_case_id` em prazo.
- [CONFIRMADO_NO_CÓDIGO] Coerência entre `organization_id` e `law_case_id` em documento.
- [PRECISA_VALIDAR] Validação de papel (`cliente` para `client_id`, `advogado` para `lawyer_id`) caso a equipa queira reforçar a integridade no mesmo ciclo.

## 8. Testes já existentes

- [CONFIRMADO_NO_CÓDIGO] [tests/test_api.py](/c:/projectos/JurisAI/tests/test_api.py) cobre:
  - login JWT
  - refresh
  - criação/listagem de caso dentro da mesma organização
  - isolamento de listagem entre organizações
  - perfil
  - histórico de IA
- [CONFIRMADO_NO_CÓDIGO] Não há testes que tentem criar caso/prazo/documento com FK de outra organização.

## 9. Testes que precisam ser criados antes da implementação

### Críticos

- [CONFIRMADO_NO_CÓDIGO] `CT-001` bloquear criação de caso com `client_id` de outra organização
- [CONFIRMADO_NO_CÓDIGO] `CT-002` bloquear criação de prazo com `law_case_id` de outra organização
- [CONFIRMADO_NO_CÓDIGO] `CT-003` bloquear criação de documento com `law_case_id` de outra organização

### Complementares recomendados

- [INFERIDO_DO_CÓDIGO] teste positivo de criação de caso com `client_id` e `lawyer_id` do mesmo tenant
- [INFERIDO_DO_CÓDIGO] teste positivo de criação de prazo com `law_case_id` do mesmo tenant
- [INFERIDO_DO_CÓDIGO] teste positivo de criação de documento com `law_case_id` do mesmo tenant
- [PRECISA_VALIDAR] teste para `lawyer_id` de outra organização separado de `client_id`
- [PRECISA_VALIDAR] teste de mensagens de erro para garantir estabilidade do contrato de API

## 10. Estratégia recomendada

### Estratégia principal

- [CONFIRMADO_NO_CÓDIGO] Manter `OrganizationScopedValidationMixin` responsável apenas por resolver `organization_id`.
- [INFERIDO_DO_CÓDIGO] Criar uma segunda camada específica para validação de relações por tenant, separada da resolução de organização.
- [INFERIDO_DO_CÓDIGO] Aplicar essa validação nos serializers afetados, de forma explícita por entidade, para preservar clareza e reduzir risco de efeitos colaterais.

### Justificativa

- [CONFIRMADO_NO_CÓDIGO] O mixin atual é genérico e foi introduzido em `IMP-006` para resolver duplicação de `organization_id`.
- [INFERIDO_DO_CÓDIGO] Estendê-lo demais com lógica de validação relacional pode misturar responsabilidades e tornar `IMP-006` mais frágil.
- [INFERIDO_DO_CÓDIGO] Um mixin separado, ou helpers explícitos nos serializers, mantém melhor separação entre:
  - resolução do tenant
  - validação de coerência de relações

## 11. Estratégias alternativas consideradas

### Alternativa A: estender `OrganizationScopedValidationMixin`

- Vantagem:
  - [INFERIDO_DO_CÓDIGO] centralização
- Desvantagem:
  - [INFERIDO_DO_CÓDIGO] mistura responsabilidade de “resolver organização” com “validar entidades relacionadas”
  - [INFERIDO_DO_CÓDIGO] risco de impactar serializers não envolvidos em `IMP-001`

### Alternativa B: validação apenas nas views

- Vantagem:
  - [INFERIDO_DO_CÓDIGO] implementação localizada por endpoint
- Desvantagem:
  - [INFERIDO_DO_CÓDIGO] a regra fica fora da camada de validação de entrada
  - [INFERIDO_DO_CÓDIGO] mais difícil de reutilizar ou testar no nível do serializer

### Alternativa C: validação no model

- Vantagem:
  - [INFERIDO_DO_CÓDIGO] integridade mais central
- Desvantagem:
  - [CONFIRMADO_NO_CÓDIGO] não há hoje uma camada de validação forte nos models para esse tipo de regra
  - [INFERIDO_DO_CÓDIGO] maior risco de alterar comportamentos fora da API ou exigir chamadas de `full_clean()`

## 12. Plano de implementação faseado

### Fase 0: preparação

1. [CONFIRMADO_NO_CÓDIGO] Confirmar com validação humana o comportamento esperado quando houver mismatch entre tenant e FK.
2. [CONFIRMADO_NO_CÓDIGO] Definir qual status code e mensagem de erro devem ser usados.
3. [PRECISA_VALIDAR] Confirmar se validação de papel (`cliente`/`advogado`) entra nesta mesma mudança ou fica fora do escopo.

### Fase 1: testes antes da mudança

1. Criar testes negativos para `LawCase`, `Deadline` e `Document`.
2. Criar testes positivos de criação válida dentro do tenant.
3. Confirmar o contrato de erro esperado antes de mexer no código.

### Fase 2: implementação mínima

1. Adicionar validação de coerência tenant->FK em `LawCaseSerializer`.
2. Adicionar validação de coerência tenant->FK em `DeadlineSerializer`.
3. Adicionar validação de coerência tenant->FK em `DocumentSerializer`.
4. Não alterar views, models, schema ou autenticação nesta fase.

### Fase 3: verificação

1. Rodar testes específicos.
2. Rodar regressão dos testes de API existentes.
3. Atualizar documentação de segurança, testes e change log.

## 13. Plano de testes antes da implementação

- [CONFIRMADO_NO_CÓDIGO] Capturar o comportamento atual com novos testes que demonstrem a lacuna.
- [PRECISA_VALIDAR] Dependendo da política da equipa, esses testes podem inicialmente falhar de propósito e depois guiar a implementação.
- Casos mínimos:
  - caso com `client_id` cross-tenant
  - caso com `lawyer_id` cross-tenant
  - prazo com `law_case_id` cross-tenant
  - documento com `law_case_id` cross-tenant

## 14. Plano de testes depois da implementação

- Reexecutar todos os testes da fase anterior.
- Reexecutar:
  - [tests/test_api.py](/c:/projectos/JurisAI/tests/test_api.py)
  - testes de serializers já existentes [PRECISA_VALIDAR]
- Confirmar:
  - bloqueio de relações cross-tenant
  - manutenção das criações válidas dentro do tenant
  - manutenção de paginação/listagem pré-existente

## 15. Critérios de aceitação

1. [CONFIRMADO_NO_CÓDIGO] Não é mais possível criar `LawCase` com `client_id` ou `lawyer_id` de outra organização.
2. [CONFIRMADO_NO_CÓDIGO] Não é mais possível criar `Deadline` com `law_case_id` de outra organização.
3. [CONFIRMADO_NO_CÓDIGO] Não é mais possível criar `Document` com `law_case_id` de outra organização.
4. [CONFIRMADO_NO_CÓDIGO] Criações válidas no mesmo tenant continuam funcionando.
5. [CONFIRMADO_NO_CÓDIGO] Não há alteração de contrato público da API além do bloqueio de casos hoje indevidos.
6. [CONFIRMADO_NO_CÓDIGO] Documentação e testes são atualizados no mesmo ciclo.

## 16. Riscos

### Riscos de implementação incorreta

- [CONFIRMADO_NO_CÓDIGO] Bloquear criações legítimas dentro do tenant.
- [CONFIRMADO_NO_CÓDIGO] Introduzir mensagens de erro inconsistentes entre endpoints.
- [INFERIDO_DO_CÓDIGO] Misturar demais a lógica com `OrganizationScopedValidationMixin` e criar regressão em serializers não relacionados.
- [INFERIDO_DO_CÓDIGO] Esquecer um dos caminhos de criação e deixar superfície parcial protegida.

### Risco geral da melhoria

- [CONFIRMADO_NO_CÓDIGO] Alto.
- Justificativa:
  - [CONFIRMADO_NO_CÓDIGO] A melhoria toca o boundary principal de tenant do sistema.
  - [INFERIDO_DO_CÓDIGO] Pode tornar inválidos requests que hoje passam, ainda que incorretamente.

## 17. Rollback plan

1. Reverter apenas a validação adicionada nos serializers afetados.
2. Manter os testes criados, marcando claramente o comportamento restaurado se o rollback for temporário.
3. Reverter atualizações documentais ligadas à implementação, preservando o plano técnico.
4. [PRECISA_VALIDAR] Se o rollout for faseado em ambiente real, considerar feature flag ou release controlado, embora isso não exista hoje no código.

## 18. Perguntas para validação humana

1. Quando ocorrer associação cross-tenant, a resposta deve ser `400 validation_error` ou `403 permission_denied`?
2. A validação de papel (`client` deve ser `cliente`, `lawyer` deve ser `advogado`) entra nesta mesma mudança?
3. O endpoint de criação de `LawCase` deve continuar aceitando qualquer `client_id/lawyer_id` do mesmo tenant, independentemente do papel, até segunda fase?
4. Devemos introduzir um mixin específico de “tenant relation validation” ou preferir validação explícita em cada serializer?
5. Há algum fluxo externo conhecido que hoje dependa, mesmo de forma incorreta, de relacionamentos cross-tenant?
6. A equipa prefere implementar em uma mudança só ou em fases separadas por entidade (`LawCase` primeiro, depois `Deadline` e `Document`)?

