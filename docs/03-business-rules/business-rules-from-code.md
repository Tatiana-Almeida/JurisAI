# Business Rules From Code

## RN-001 Limite de usuários por plano

- Regra: [CONFIRMADO_NO_CÓDIGO] Uma organização só pode adicionar usuário se `users.count() < max_users()`.
- Origem: `organizations.models.Organization.can_add_user` e `accounts.views.UserViewSet.perform_create`.
- Impacto: criação de usuários.

## RN-002 Limite de casos por plano

- Regra: [CONFIRMADO_NO_CÓDIGO] A criação de caso é bloqueada quando `organization.cases.count() >= organization.max_cases()`.
- Origem: `law_cases.views.LawCaseViewSet.perform_create`.

## RN-003 Limite de documentos por plano

- Regra: [CONFIRMADO_NO_CÓDIGO] A criação de documento é bloqueada quando `organization.documents.count() >= organization.max_documents()`.
- Origem: `documents.views.DocumentViewSet.perform_create`.

## RN-004 Quota mensal de IA por plano

- Regra: [CONFIRMADO_NO_CÓDIGO] O número de `AIRequest` no mês corrente é comparado com o limite do plano.
- Origem: `ai_assistant.services.ai_service._ensure_ai_quota`.

## RN-005 Usuário só vê dados da própria organização

- Regra: [CONFIRMADO_NO_CÓDIGO] Diversas views filtram o queryset por `request.user.organization`.
- Origem: `accounts`, `organizations`, `law_cases`, `deadlines`, `documents`, `billing`, `notifications`, `ai_assistant`.
- Observação: [PRECISA_VALIDAR] A regra não é aplicada uniformemente no nível do serializer ao validar relações.

## RN-006 Apenas admin pode criar usuários

- Regra: [CONFIRMADO_NO_CÓDIGO] Usuários com `role` diferente de `admin` não podem criar usuários via `UserViewSet`.
- Origem: `accounts.views.UserViewSet.perform_create`.

## RN-007 Perfil não permite mudar role nem organização

- Regra: [CONFIRMADO_NO_CÓDIGO] O endpoint `profile` remove `role` e `organization_id` do payload de atualização.
- Origem: `accounts.views.UserViewSet.profile`.

## RN-008 Registro cria uma organização junto com o primeiro usuário

- Regra: [CONFIRMADO_NO_CÓDIGO] `RegisterView` cria `Organization` antes de validar/criar o usuário.
- Origem: `accounts.views.RegisterView.post`.

## RN-009 Exclusão de caso é soft delete

- Regra: [CONFIRMADO_NO_CÓDIGO] `destroy` em `LawCase` marca `deleted=True` em vez de remover o registo.
- Origem: `law_cases.views.LawCaseViewSet.perform_destroy`.

## RN-010 Complete marca prazo como concluído

- Regra: [CONFIRMADO_NO_CÓDIGO] A ação `complete` em `Deadline` marca `completed=True`.
- Origem: `deadlines.views.DeadlineViewSet.complete`.

## RN-011 Filtro de próximos prazos

- Regra: [CONFIRMADO_NO_CÓDIGO] Quando `upcoming_days` é inteiro válido, o endpoint filtra prazos até `now + days` com `completed=False`.
- Origem: `deadlines.views.DeadlineViewSet.get_queryset`.

## RN-012 Versionamento de documentos por caso

- Regra: [CONFIRMADO_NO_CÓDIGO] O serializer busca a última versão do documento do caso e incrementa `version`.
- Origem: `documents.serializers.DocumentSerializer.create`.

## RN-013 Notificação WhatsApp é mock

- Regra: [CONFIRMADO_NO_CÓDIGO] Enviar WhatsApp cria um registo `Notification` marcado como enviado, sem integração real externa.
- Origem: `notifications.services.NotificationService.send_whatsapp`.

## RN-014 Lembretes de prazo por email

- Regra: [CONFIRMADO_NO_CÓDIGO] Prazos vencendo em até 24 horas geram email para o advogado do caso.
- Origem: `deadlines.tasks.send_deadline_reminders`.

## RN-015 Auditoria automática de create/update/delete

- Regra: [CONFIRMADO_NO_CÓDIGO] Signals globais gravam snapshots `before/after` em `AuditLog` para models elegíveis.
- Origem: `audit_logs.signals`.

## RN-016 Webhook de billing cria pagamentos/atualiza assinatura

- Regra: [CONFIRMADO_NO_CÓDIGO] O webhook trata `invoice.payment_succeeded`, `invoice.payment_failed` e `customer.subscription.updated`.
- Origem: `billing.views.StripeWebhookView.post`.
- Observação: [PRECISA_VALIDAR] Não há validação de assinatura observável.

