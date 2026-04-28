# Improvement Plan

## Escopo

- [CONFIRMADO_NO_CÓDIGO] Este documento propõe melhorias com base na documentação já gerada em `docs/`.
- [CONFIRMADO_NO_CÓDIGO] Nenhuma alteração foi implementada nesta etapa.
- [CONFIRMADO_NO_CÓDIGO] O plano segue a skill `safe-improvement-workflow`: analisar, documentar comportamento atual, identificar problema, classificar risco, propor melhoria, indicar arquivos afetados, testes e necessidade de validação humana.

## Princípios do plano

1. [CONFIRMADO_NO_CÓDIGO] Não reescrever o backend inteiro.
2. [CONFIRMADO_NO_CÓDIGO] Não alterar contrato funcional sem documentação e validação.
3. [CONFIRMADO_NO_CÓDIGO] Priorizar mudanças pequenas, rastreáveis e testáveis.
4. [CONFIRMADO_NO_CÓDIGO] Tratar itens de alto risco como dependentes de validação humana antes da implementação.

## Ordem sugerida de execução

1. `IMP-001` Blindar validação multi-tenant em entradas
2. `IMP-002` Endurecer o webhook de billing
3. `IMP-003` Corrigir boundary multi-tenant de auditoria
4. `IMP-004` Corrigir drift de planos entre model, migration e seeds
5. `IMP-005` Corrigir integração OpenAI para a SDK declarada
6. `IMP-006` Unificar validações repetidas de `organization_id`
7. `IMP-007` Endurecer upload de documentos
8. `IMP-008` Rever agendamento Celery/Beat e consistência operacional
9. `IMP-009` Corrigir fluxo de notificações WhatsApp mock
10. `IMP-010` Fechar lacunas de configuração defensiva

## IMP-001 Blindar validação multi-tenant em relacionamentos de entrada

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] `LawCaseSerializer`, `DeadlineSerializer` e `DocumentSerializer` forçam `organization_id` do usuário, mas não validam se os IDs relacionados pertencem à mesma organização.
- Melhoria proposta:
  - Validar explicitamente coerência entre `request.user.organization` e objetos relacionados (`client`, `lawyer`, `law_case`).
- Risco:
  - alto
- Arquivos afetados:
  - [law_cases/serializers.py](/c:/projectos/JurisAI/law_cases/serializers.py)
  - [deadlines/serializers.py](/c:/projectos/JurisAI/deadlines/serializers.py)
  - [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py)
  - [tests/test_api.py](/c:/projectos/JurisAI/tests/test_api.py)
- Testes necessários:
  - `CT-001`
  - `CT-002`
  - `CT-003`
  - testes positivos de criação dentro do tenant
- Impacto esperado:
  - Redução forte do risco de acesso cruzado entre organizações.
  - Maior coerência entre intenção multi-tenant e comportamento real.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Pode rejeitar requests que hoje passam, mesmo que indevidamente.

## IMP-002 Endurecer o webhook de billing

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] O endpoint `/api/v1/webhook/` é público e não há validação de assinatura observável.
  - [CONFIRMADO_NO_CÓDIGO] A view mistura parse, regra de negócio e persistência.
- Melhoria proposta:
  - Introduzir validação de assinatura/origem.
  - Extrair a lógica de processamento para um service dedicado.
  - Corrigir o uso da variável `status` que conflita com o import do DRF.
- Risco:
  - alto
- Arquivos afetados:
  - [billing/views.py](/c:/projectos/JurisAI/billing/views.py)
  - [billing/serializers.py](/c:/projectos/JurisAI/billing/serializers.py)
  - [billing/models.py](/c:/projectos/JurisAI/billing/models.py)
  - novo service em `billing/` [PRECISA_VALIDAR]
  - [tests/test_api.py](/c:/projectos/JurisAI/tests/test_api.py) ou novos testes dedicados [PRECISA_VALIDAR]
- Testes necessários:
  - `CT-004`
  - testes de eventos válidos
  - testes de eventos inválidos/sem assinatura
  - testes de idempotência [PRECISA_VALIDAR]
- Impacto esperado:
  - Redução de fraude, inserção indevida de pagamentos e regressões no fluxo de cobrança.
  - Melhor testabilidade do módulo.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Afeta integração externa e fluxo financeiro.

## IMP-003 Corrigir boundary multi-tenant de auditoria

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] `AuditLog` não possui `organization`.
  - [CONFIRMADO_NO_CÓDIGO] `AuditLogViewSet` expõe logs globais para qualquer admin autenticado.
- Melhoria proposta:
  - Incluir `organization` nos logs sempre que possível.
  - Filtrar leitura por tenant.
  - Rever estratégia de auditoria de entidades sem organização direta.
- Risco:
  - alto
- Arquivos afetados:
  - [audit_logs/models.py](/c:/projectos/JurisAI/audit_logs/models.py)
  - [audit_logs/views.py](/c:/projectos/JurisAI/audit_logs/views.py)
  - [audit_logs/serializers.py](/c:/projectos/JurisAI/audit_logs/serializers.py)
  - [audit_logs/signals.py](/c:/projectos/JurisAI/audit_logs/signals.py)
  - migration nova em `audit_logs/migrations/` [PRECISA_VALIDAR]
  - testes novos para auditoria [PRECISA_VALIDAR]
- Testes necessários:
  - `CT-005`
  - testes de criação de log com organização
  - testes de listagem filtrada por tenant
  - testes de leitura por admin de tenant diferente
- Impacto esperado:
  - Redução de risco de vazamento entre clientes.
  - Melhor aderência do módulo de auditoria ao modelo SaaS multi-tenant.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Exige mudança de schema e política de acesso.

## IMP-004 Corrigir drift de planos entre model, migration e seeds

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] `Organization.plan` está inconsistente entre migration inicial, model atual e comandos de seed.
- Melhoria proposta:
  - Escolher o catálogo canónico de planos.
  - Atualizar models, seeds, regras de IA e, se necessário, migrations de correção.
  - Documentar impacto em dados existentes.
- Risco:
  - médio
- Arquivos afetados:
  - [organizations/models.py](/c:/projectos/JurisAI/organizations/models.py)
  - [accounts/management/commands/seed_initial.py](/c:/projectos/JurisAI/accounts/management/commands/seed_initial.py)
  - [accounts/management/commands/seed_demo.py](/c:/projectos/JurisAI/accounts/management/commands/seed_demo.py)
  - [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py)
  - migrations de `organizations/` [PRECISA_VALIDAR]
- Testes necessários:
  - `CT-006`
  - testes de limites por plano
  - testes de seeds em ambiente limpo [PRECISA_VALIDAR]
- Impacto esperado:
  - Consistência de domínio, menos comportamento inesperado e documentação mais confiável.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Pode afetar dados já persistidos e regras comerciais.

## IMP-005 Corrigir integração OpenAI para a SDK declarada

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] O projeto declara `openai>=1.0`, mas usa uma interface legado.
- Melhoria proposta:
  - Atualizar `AIService` para a API compatível com a versão declarada.
  - Preservar fallback mock quando a chave não estiver configurada.
- Risco:
  - médio
- Arquivos afetados:
  - [ai_assistant/services/ai_service.py](/c:/projectos/JurisAI/ai_assistant/services/ai_service.py)
  - [requirements.txt](/c:/projectos/JurisAI/requirements.txt) [PRECISA_VALIDAR]
  - testes novos de serviço [PRECISA_VALIDAR]
- Testes necessários:
  - `CT-007`
  - testes de fallback mock
  - testes de persistência de `AIRequest`
- Impacto esperado:
  - Menos risco de falha em runtime nas rotas de IA.
  - Maior previsibilidade do módulo.
- Precisa validação humana antes da implementação:
  - não, desde que o contrato das respostas seja preservado

## IMP-006 Unificar validações repetidas de `organization_id`

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] Vários serializers repetem o mesmo padrão de preenchimento/validação de `organization_id`.
- Melhoria proposta:
  - Extrair mixin/base serializer utilitário para reduzir duplicação.
- Risco:
  - baixo
- Arquivos afetados:
  - [accounts/serializers.py](/c:/projectos/JurisAI/accounts/serializers.py)
  - [law_cases/serializers.py](/c:/projectos/JurisAI/law_cases/serializers.py)
  - [deadlines/serializers.py](/c:/projectos/JurisAI/deadlines/serializers.py)
  - [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py)
  - [billing/serializers.py](/c:/projectos/JurisAI/billing/serializers.py)
  - [notifications/serializers.py](/c:/projectos/JurisAI/notifications/serializers.py)
  - novo utilitário compartilhado em `jurisai/` ou módulo comum [PRECISA_VALIDAR]
- Testes necessários:
  - regressão dos serializers afetados
  - `CT-006`
- Impacto esperado:
  - Menos divergência futura e manutenção mais simples.
- Precisa validação humana antes da implementação:
  - não

## IMP-007 Endurecer upload de documentos

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] `Document.file` não possui validação explícita de tipo, tamanho ou extensão observável.
- Melhoria proposta:
  - Adicionar validações no serializer/model.
  - Definir política mínima de upload segura.
- Risco:
  - médio
- Arquivos afetados:
  - [documents/models.py](/c:/projectos/JurisAI/documents/models.py)
  - [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py)
  - [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py) [PRECISA_VALIDAR]
  - testes novos de upload [PRECISA_VALIDAR]
- Testes necessários:
  - upload válido
  - upload inválido por tipo
  - upload inválido por tamanho [PRECISA_VALIDAR]
- Impacto esperado:
  - Menos risco operacional e de segurança ligado a ficheiros.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Pode bloquear tipos de documento hoje aceites.

## IMP-008 Rever agendamento Celery/Beat e consistência operacional

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] Há schedule definido em settings, mas não existe serviço `beat` no `docker-compose`.
  - [PRECISA_VALIDAR] `django_celery_beat` aparece em `INSTALLED_APPS` sem evidência correspondente em dependências.
- Melhoria proposta:
  - Definir estratégia única para agendamento: `CELERY_BEAT_SCHEDULE` estático ou `django-celery-beat`.
  - Ajustar dependências e runtime para refletir a escolha.
- Risco:
  - médio
- Arquivos afetados:
  - [jurisai/settings.py](/c:/projectos/JurisAI/jurisai/settings.py)
  - [docker-compose.yml](/c:/projectos/JurisAI/docker-compose.yml)
  - [requirements.txt](/c:/projectos/JurisAI/requirements.txt)
  - documentação operacional em `docs/00-code-discovery/` e `docs/05-architecture/`
- Testes necessários:
  - verificação de bootstrap dos serviços
  - teste manual/automatizado de execução de tasks agendadas [PRECISA_VALIDAR]
- Impacto esperado:
  - Melhor previsibilidade operacional de lembretes e notificações.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Afeta deployment e runtime de background.

## IMP-009 Corrigir fluxo de notificações WhatsApp mock

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] `send_pending_notifications` chama `send_whatsapp`, que cria novo `Notification`, gerando duplicidade lógica.
- Melhoria proposta:
  - Separar “registrar envio” de “representar canal mock”.
  - Evitar criação de um segundo registo quando o primeiro já representa a notificação.
- Risco:
  - baixo
- Arquivos afetados:
  - [notifications/services.py](/c:/projectos/JurisAI/notifications/services.py)
  - [notifications/tasks.py](/c:/projectos/JurisAI/notifications/tasks.py)
  - testes novos de tarefa [PRECISA_VALIDAR]
- Testes necessários:
  - `CT-010`
  - verificação de ausência de duplicidade
- Impacto esperado:
  - Histórico de notificações mais coerente.
  - Menos ruído operacional e de auditoria.
- Precisa validação humana antes da implementação:
  - não

## IMP-010 Fechar lacunas de configuração defensiva

- Problema atual:
  - [CONFIRMADO_NO_CÓDIGO] `SECRET_KEY` tem fallback inseguro.
  - [NÃO_ENCONTRADO] Rate limiting observável.
  - [NÃO_ENCONTRADO] Política CORS explícita.
- Melhoria proposta:
  - Tornar `SECRET_KEY` obrigatória em produção.
  - Avaliar e configurar throttling para endpoints críticos.
  - Definir política CORS conforme o front real.
- Risco:
  - médio
- Arquivos afetados:
  - [jurisai/settings.py](/c:/projectos/JurisAI/jurisai/settings.py)
  - [requirements.txt](/c:/projectos/JurisAI/requirements.txt) [PRECISA_VALIDAR]
  - documentação de runtime em `docs/00-code-discovery/`
- Testes necessários:
  - autenticação em ambiente configurado
  - testes de throttling [PRECISA_VALIDAR]
  - validação manual de CORS com cliente real [PRECISA_VALIDAR]
- Impacto esperado:
  - Melhor baseline de segurança e menor risco de exposição por configuração.
- Precisa validação humana antes da implementação:
  - sim
- Motivo:
  - Depende do ambiente real de produção e dos clientes consumidores da API.

## Resumo por risco

### Alto risco

- `IMP-001` Blindar validação multi-tenant em entradas
- `IMP-002` Endurecer o webhook de billing
- `IMP-003` Corrigir boundary multi-tenant de auditoria

### Médio risco

- `IMP-004` Corrigir drift de planos
- `IMP-005` Corrigir integração OpenAI
- `IMP-007` Endurecer upload de documentos
- `IMP-008` Rever agendamento Celery/Beat
- `IMP-010` Fechar lacunas de configuração defensiva

### Baixo risco

- `IMP-006` Unificar validações repetidas de `organization_id`
- `IMP-009` Corrigir fluxo de notificações WhatsApp mock

## Recomendação de execução

1. [CONFIRMADO_NO_CÓDIGO] Validar humanamente `IMP-001`, `IMP-002` e `IMP-003` antes de qualquer implementação.
2. [CONFIRMADO_NO_CÓDIGO] Começar por `IMP-009` e `IMP-006` se o objetivo for ganho rápido com baixo risco.
3. [CONFIRMADO_NO_CÓDIGO] Em seguida, preparar testes para `IMP-001` e `IMP-002`.
4. [CONFIRMADO_NO_CÓDIGO] Só depois abordar itens com migration ou impacto operacional mais amplo.

