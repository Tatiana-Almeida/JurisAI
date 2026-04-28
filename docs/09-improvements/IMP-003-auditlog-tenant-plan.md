# IMP-003 AuditLog Tenant Plan

## 1. Resumo da melhoria

- [CONFIRMADO_NO_CÓDIGO] A melhoria `IMP-003` tem como objetivo garantir isolamento multi-tenant no módulo de auditoria.
- [CONFIRMADO_NO_CÓDIGO] O problema central é que `AuditLog` não possui referência explícita a `organization`, enquanto a API de leitura expõe logs globalmente para qualquer utilizador com papel `admin`.
- [INFERIDO_DO_CÓDIGO] A correção segura precisa separar dois problemas:
  - contexto correto na criação do log
  - filtro correto na leitura do log

## 2. Problema atual

- [CONFIRMADO_NO_CÓDIGO] O model `AuditLog` guarda `user`, `action`, `entity`, `before`, `after`, `ip` e `timestamp`, mas não guarda `organization`.
- [CONFIRMADO_NO_CÓDIGO] `AuditLogViewSet` usa `queryset = AuditLog.objects.select_related('user').all()` sem filtro por tenant.
- [CONFIRMADO_NO_CÓDIGO] `AuditLogViewSet` está protegido por `IsAuthenticated` e `IsAdmin`, logo qualquer admin autenticado pode listar logs globais.
- [CONFIRMADO_NO_CÓDIGO] Não há testes atuais cobrindo isolamento de auditoria por organização.
- [INFERIDO_DO_CÓDIGO] Isto cria risco de exposição cruzada entre clientes num módulo que, pela natureza do produto, pode conter snapshots sensíveis de entidades jurídicas e operacionais.

## 3. Evidências no código

### 3.1 Model

- [CONFIRMADO_NO_CÓDIGO] [audit_logs/models.py](/c:/projectos/JurisAI/audit_logs/models.py) não possui FK para `organizations.Organization`.

### 3.2 Serializer

- [CONFIRMADO_NO_CÓDIGO] [audit_logs/serializers.py](/c:/projectos/JurisAI/audit_logs/serializers.py) expõe `user`, `user_email`, `action`, `entity`, `before`, `after`, `ip` e `timestamp`.
- [CONFIRMADO_NO_CÓDIGO] Não existe campo `organization` no payload de leitura.

### 3.3 View

- [CONFIRMADO_NO_CÓDIGO] [audit_logs/views.py](/c:/projectos/JurisAI/audit_logs/views.py) usa `ReadOnlyModelViewSet`.
- [CONFIRMADO_NO_CÓDIGO] A listagem usa queryset global.
- [CONFIRMADO_NO_CÓDIGO] A permissão atual é `IsAdmin`, sem object filtering adicional.

### 3.4 Geração de logs

- [CONFIRMADO_NO_CÓDIGO] [audit_logs/signals.py](/c:/projectos/JurisAI/audit_logs/signals.py) usa signals globais `pre_save`, `post_save` e `post_delete`.
- [CONFIRMADO_NO_CÓDIGO] `record_audit()` cria o log com base em:
  - `request` vindo de thread local
  - `user` autenticado, se existir
  - snapshots `before` e `after`
  - `entity` como string `app_label.model_name`
- [CONFIRMADO_NO_CÓDIGO] `record_audit()` atualmente não tenta persistir `organization`.

### 3.5 Middleware

- [CONFIRMADO_NO_CÓDIGO] [jurisai/middleware.py](/c:/projectos/JurisAI/jurisai/middleware.py) mantém o request atual em thread local.
- [CONFIRMADO_NO_CÓDIGO] O middleware define `request.organization = getattr(request.user, 'organization', None)`.
- [PRECISA_VALIDAR] Em requests autenticados por JWT no DRF, é preciso confirmar se o `request` bruto guardado no thread local já carrega o utilizador final no momento em que os signals gravam o log. A suíte atual não cobre isso explicitamente.

### 3.6 Admin Django

- [CONFIRMADO_NO_CÓDIGO] [audit_logs/admin.py](/c:/projectos/JurisAI/audit_logs/admin.py) registra `AuditLog` no Django Admin.
- [CONFIRMADO_NO_CÓDIGO] Não há filtro por organização no admin.
- [INFERIDO_DO_CÓDIGO] O Django Admin é uma superfície adicional de leitura global para staff/superusers.

### 3.7 Migrations

- [CONFIRMADO_NO_CÓDIGO] Só existe [audit_logs/migrations/0001_initial.py](/c:/projectos/JurisAI/audit_logs/migrations/0001_initial.py).
- [CONFIRMADO_NO_CÓDIGO] A migration inicial também não possui `organization`.

### 3.8 Testes

- [CONFIRMADO_NO_CÓDIGO] Não existe ficheiro de testes dedicado a `audit_logs/`.
- [CONFIRMADO_NO_CÓDIGO] A suíte atual em `tests/` não cobre `API-030` nem `API-031`.

## 4. Superfície de impacto

### 4.1 Endpoints afetados

| Endpoint | Método | Superfície | Estado |
|---|---|---|---|
| `API-030 /api/v1/audit-logs/` | GET | listagem de logs | [CONFIRMADO_NO_CÓDIGO] |
| `API-031 /api/v1/audit-logs/{id}/` | GET | detalhe de log | [CONFIRMADO_NO_CÓDIGO] |

### 4.2 Superfícies não-API

- [CONFIRMADO_NO_CÓDIGO] Django Admin de `AuditLog`.
- [CONFIRMADO_NO_CÓDIGO] Signals globais que criam logs para vários models do sistema.
- [NÃO_ENCONTRADO] Tasks dedicadas em `audit_logs/tasks.py`.

## 5. Arquivos provavelmente afetados

- [audit_logs/models.py](/c:/projectos/JurisAI/audit_logs/models.py)
- [audit_logs/serializers.py](/c:/projectos/JurisAI/audit_logs/serializers.py)
- [audit_logs/views.py](/c:/projectos/JurisAI/audit_logs/views.py)
- [audit_logs/signals.py](/c:/projectos/JurisAI/audit_logs/signals.py)
- [audit_logs/admin.py](/c:/projectos/JurisAI/audit_logs/admin.py)
- nova migration em `audit_logs/migrations/` [CONFIRMADO_NO_CÓDIGO]
- novos testes em `tests/` [CONFIRMADO_NO_CÓDIGO]
- [docs/06-security/security-audit.md](/c:/projectos/JurisAI/docs/06-security/security-audit.md)
- [docs/08-tests/recommended-test-cases.md](/c:/projectos/JurisAI/docs/08-tests/recommended-test-cases.md)
- [docs/09-improvements/change-log.md](/c:/projectos/JurisAI/docs/09-improvements/change-log.md)
- [docs/10-traceability/traceability-matrix.md](/c:/projectos/JurisAI/docs/10-traceability/traceability-matrix.md)

## 6. Endpoints afetados

- [CONFIRMADO_NO_CÓDIGO] `GET /api/v1/audit-logs/`
- [CONFIRMADO_NO_CÓDIGO] `GET /api/v1/audit-logs/{id}/`
- [INFERIDO_DO_CÓDIGO] O contrato público pode permanecer igual em shape de sucesso, desde que a filtragem e o escopo de visibilidade mudem apenas para remover acessos indevidos.

## 7. Entidades afetadas

| Entidade | Papel na melhoria | Estado |
|---|---|---|
| `ENT-011 AuditLog` | entidade central da melhoria | [CONFIRMADO_NO_CÓDIGO] |
| `ENT-001 Organization` | boundary multi-tenant a introduzir no log | [CONFIRMADO_NO_CÓDIGO] |
| `ENT-002 User` | fonte parcial de contexto para backfill e criação | [CONFIRMADO_NO_CÓDIGO] |

## 8. Necessidade ou não de migration

- [CONFIRMADO_NO_CÓDIGO] Sim, a melhoria precisa de migration se a estratégia recomendada for adotada.
- [CONFIRMADO_NO_CÓDIGO] O model atual não tem `organization`, então o isolamento forte de leitura não pode ser garantido apenas por queryset sobre o schema atual.
- [INFERIDO_DO_CÓDIGO] A migration mais segura é adicionar `organization` primeiro como `null=True, blank=True`, com índice e `on_delete=PROTECT` ou `SET_NULL` [PRECISA_VALIDAR].
- [PRECISA_VALIDAR] A decisão de tornar o campo obrigatório depois do backfill deve ser tomada numa fase posterior, não na primeira mudança.

## 9. Estratégia recomendada

### Estratégia principal

- [CONFIRMADO_NO_CÓDIGO] Adicionar `organization` a `AuditLog`.
- [INFERIDO_DO_CÓDIGO] Persistir `organization` no momento da criação do log com uma ordem explícita de resolução.
- [CONFIRMADO_NO_CÓDIGO] Filtrar `AuditLogViewSet` por `request.user.organization`.
- [INFERIDO_DO_CÓDIGO] Ajustar o Django Admin para não expor logs globais sem critério.

### Ordem recomendada para resolver `organization` em novos logs

1. [INFERIDO_DO_CÓDIGO] Se `instance` tiver `organization_id`, usar esse valor.
2. [INFERIDO_DO_CÓDIGO] Se o próprio model auditado for `Organization`, usar `instance.id`.
3. [INFERIDO_DO_CÓDIGO] Se `instance` tiver `user.organization_id` relevante e estável, usar como fallback apenas quando fizer sentido.
4. [INFERIDO_DO_CÓDIGO] Se houver `request.user.organization_id`, usar como fallback de contexto.
5. [PRECISA_VALIDAR] Se nenhum contexto existir, permitir `organization = null` na primeira fase para não quebrar a auditoria.

### Justificativa

- [CONFIRMADO_NO_CÓDIGO] Filtrar apenas por `user.organization` não resolve logs com `user=None`.
- [CONFIRMADO_NO_CÓDIGO] Filtrar por parsing de `before/after` no queryset não é viável nem seguro como solução principal.
- [INFERIDO_DO_CÓDIGO] Guardar `organization` explicitamente torna a leitura simples, indexável, testável e consistente com o resto do produto.

## 10. Estratégias alternativas consideradas

### Alternativa A: filtrar logs apenas por `user.organization`

- Vantagem:
  - [INFERIDO_DO_CÓDIGO] sem migration imediata
- Desvantagem:
  - [CONFIRMADO_NO_CÓDIGO] falha para logs com `user=None`
  - [INFERIDO_DO_CÓDIGO] falha para ações sistémicas ou requests onde o utilizador não esteja corretamente associado
  - [INFERIDO_DO_CÓDIGO] não protege contra histórico já inconsistente

### Alternativa B: derivar organização em tempo de leitura a partir de `before/after`

- Vantagem:
  - [INFERIDO_DO_CÓDIGO] evita alterar schema no curto prazo
- Desvantagem:
  - [CONFIRMADO_NO_CÓDIGO] `before/after` são JSON genéricos sem contrato forte
  - [INFERIDO_DO_CÓDIGO] custo de leitura e complexidade aumentam
  - [INFERIDO_DO_CÓDIGO] risco de erro lógico alto

### Alternativa C: remover temporariamente o endpoint REST de auditoria

- Vantagem:
  - [INFERIDO_DO_CÓDIGO] reduz exposição imediata
- Desvantagem:
  - [CONFIRMADO_NO_CÓDIGO] altera comportamento público
  - [CONFIRMADO_NO_CÓDIGO] foge ao objetivo de corrigir sem quebrar contrato desnecessariamente

## 11. Plano de implementação faseado

### Fase 0: validação de política

1. [CONFIRMADO_NO_CÓDIGO] Confirmar se admin de tenant deve ver apenas logs da própria organização.
2. [PRECISA_VALIDAR] Confirmar se existe algum papel operacional que precise de visão global legítima.
3. [PRECISA_VALIDAR] Confirmar se o Django Admin deve seguir a mesma política da API ou ter exceções restritas.

### Fase 1: testes antes da mudança

1. Criar testes que demonstrem a exposição global atual em `API-030`.
2. Criar testes que confirmem que utilizador não-admin não lista logs.
3. Criar testes que definam o comportamento esperado de listagem por tenant e de detalhe cross-tenant.

### Fase 2: schema mínimo

1. Adicionar `organization` a `AuditLog` como campo inicialmente nullable.
2. Criar migration de schema sem tornar o campo obrigatório.

### Fase 3: write path

1. Atualizar `record_audit()` para preencher `organization` em novos logs.
2. Definir e documentar a ordem de resolução do tenant.
3. Garantir que a ausência de contexto não impede criação do log na primeira fase.

### Fase 4: read path

1. Filtrar `AuditLogViewSet.get_queryset()` por `request.user.organization`.
2. Rever filtros e buscas para manter comportamento esperado dentro do tenant.
3. Ajustar Django Admin para reduzir ou eliminar leitura global indevida.

### Fase 5: dados antigos

1. Backfill de `organization` onde houver evidência segura.
2. Marcar como `null` os logs antigos sem resolução confiável.
3. [PRECISA_VALIDAR] Avaliar se vale a pena uma segunda migration para endurecer nullability mais tarde.

### Fase 6: documentação e validação

1. Atualizar docs de segurança, arquitetura, testes e rastreabilidade.
2. Rodar suíte focal e suíte completa.

## 12. Plano de testes antes da implementação

### Críticos

- [CONFIRMADO_NO_CÓDIGO] `CT-005` garantir que `AuditLog` não vaza dados entre organizações
- [INFERIDO_DO_CÓDIGO] teste de listagem por admin de organização A sem acesso a logs de organização B
- [INFERIDO_DO_CÓDIGO] teste de detalhe por admin tentando acessar log de outra organização
- [INFERIDO_DO_CÓDIGO] teste de não-admin recebendo bloqueio no endpoint

### Complementares

- [INFERIDO_DO_CÓDIGO] teste de criação de log com `organization` preenchida para model com `organization` direta
- [INFERIDO_DO_CÓDIGO] teste de criação de log para `Organization` usando a própria organização como boundary
- [PRECISA_VALIDAR] teste para requests JWT garantindo que o contexto do request realmente fornece utilizador/tenant ao signal

## 13. Plano de testes depois da implementação

- Reexecutar todos os testes da fase anterior.
- Rodar a suíte atual completa.
- Adicionar validações de regressão para:
  - logs novos com `organization`
  - logs filtrados por tenant
  - ausência de exposição global via API
  - comportamento esperado no Django Admin [PRECISA_VALIDAR]

## 14. Critérios de aceitação

1. [CONFIRMADO_NO_CÓDIGO] `AuditLog` deixa de ser listável globalmente por qualquer admin de tenant.
2. [CONFIRMADO_NO_CÓDIGO] `GET /api/v1/audit-logs/` retorna apenas logs da organização do utilizador autenticado.
3. [CONFIRMADO_NO_CÓDIGO] `GET /api/v1/audit-logs/{id}/` não expõe logs de outro tenant.
4. [CONFIRMADO_NO_CÓDIGO] Novos logs passam a guardar `organization` sempre que houver contexto suficiente.
5. [INFERIDO_DO_CÓDIGO] A criação de logs não é interrompida por falta de contexto em casos marginais na primeira fase.
6. [CONFIRMADO_NO_CÓDIGO] Testes e documentação são atualizados no mesmo ciclo.

## 15. Riscos

### Riscos de implementação incorreta

- [CONFIRMADO_NO_CÓDIGO] Quebrar criação de logs em fluxos hoje auditados.
- [CONFIRMADO_NO_CÓDIGO] Filtrar demais e ocultar logs legítimos do próprio tenant.
- [CONFIRMADO_NO_CÓDIGO] Manter leitura global no Django Admin mesmo após corrigir a API.
- [INFERIDO_DO_CÓDIGO] Backfill incorreto atribuindo tenant errado a logs históricos.
- [PRECISA_VALIDAR] Dependência do request em thread local pode não ser suficiente para todos os fluxos, especialmente fora de request-response tradicional.

### Risco geral da melhoria

- [CONFIRMADO_NO_CÓDIGO] Alto.
- Justificativa:
  - [CONFIRMADO_NO_CÓDIGO] exige alteração de schema
  - [CONFIRMADO_NO_CÓDIGO] afeta segurança e dados históricos
  - [INFERIDO_DO_CÓDIGO] pode alterar a visibilidade esperada por equipas operacionais

## 16. Rollback plan

1. Reverter filtro novo do queryset de auditoria se houver regressão operacional crítica.
2. Reverter uso de `organization` na criação de novos logs, mantendo a coluna nova se já estiver migrada.
3. Não apagar dados já backfillados sem plano explícito.
4. [PRECISA_VALIDAR] Se a mudança for entregue em múltiplas fases, preferir rollback parcial da fase corrente em vez de rollback total.

## 17. Perguntas para validação humana

1. Todo utilizador com papel `admin` deve ver apenas logs da própria organização, sem exceções?
2. Existe algum papel interno ou operacional que precise de visão global de logs?
3. O Django Admin deve seguir exatamente a mesma política de tenant da API?
4. Para logs históricos, a equipa aceita `organization = null` quando não houver backfill seguro?
5. Vale a pena planear uma segunda fase para tornar `organization` obrigatório depois do backfill?
6. Em modelos auditados sem `organization` direta, qual fallback é considerado aceitável: `request.user.organization`, `user.organization`, ou ambos com ordem definida?
7. Há necessidade de preservar compatibilidade total do payload de sucesso do serializer de `AuditLog`, ou a adição futura de `organization_id` na resposta é aceitável?
