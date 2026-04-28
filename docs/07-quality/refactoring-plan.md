# Refactoring Plan

## Principios

- [CONFIRMADO_NO_CODIGO] Nao reescrever o backend inteiro.
- [CONFIRMADO_NO_CODIGO] Priorizar mudancas pequenas, locais e com cobertura de testes.

## REF-001 Validar tenant em relacionamentos de entrada

- Risco: alto
- Evidencia: serializers de `LawCase`, `Deadline`, `Document`.
- Beneficio: reforca isolamento de dados.
- Estado atual: [CONFIRMADO_NO_CODIGO] Implementada.

## REF-002 Corrigir boundary de auditoria multi-tenant

- Risco: alto
- Evidencia: `AuditLog` sem `organization`; `AuditLogViewSet` sem filtro por tenant.
- Beneficio: reduz risco de exposicao entre clientes.
- Estado atual: [CONFIRMADO_NO_CODIGO] Implementada.

## REF-003 Extrair logica de webhook para service dedicado

- Risco: medio
- Evidencia: `StripeWebhookView` mistura parse, decisao e persistencia.
- Beneficio: melhora testabilidade e manutencao.
- Estado atual: [CONFIRMADO_NO_CODIGO] Fase 1 da `IMP-010` extraiu helpers puros para [billing/services.py](/c:/projectos/JurisAI/billing/services.py); a Fase 2 extraiu a leitura semantica minima de `event_id`, `event_type` e `data.object`, alem da resolucao de `organization`; a Fase 3 extraiu o processamento transacional e idempotente para um orquestrador interno; validacao por tipo ainda permanece na view.

## REF-004 Unificar validacoes repetidas de `organization_id`

- Risco: baixo
- Evidencia: serializers repetem padrao semelhante.
- Beneficio: reduz duplicacao e divergencia.
- Estado atual: [CONFIRMADO_NO_CODIGO] Implementada.

## REF-005 Revisar drift entre `Organization.plan`, seeds e limites IA

- Risco: medio
- Evidencia: `starter` aparece em migration e seeds, mas nao no model atual.
- Beneficio: consistencia de dominio e previsibilidade operacional.

## REF-006 Corrigir integracao OpenAI para SDK declarada

- Risco: medio
- Evidencia: `openai>=1.0` com uso de `ChatCompletion.create`.
- Beneficio: reduzir falhas de runtime em IA.

## REF-007 Corrigir duplicidade no fluxo WhatsApp mock

- Risco: baixo
- Evidencia: `send_pending_notifications` chamava `send_whatsapp`, que criava uma segunda `Notification`.
- Beneficio: reduz ruido operacional e mantem historico coerente.
- Estado atual: [CONFIRMADO_NO_CODIGO] Implementada.

## REF-008 Endurecer validacao de uploads de documentos

- Risco: medio
- Evidencia: `DocumentSerializer` aceitava ficheiros sem validar extensao, tamanho ou `content_type`.
- Beneficio: reduz risco operacional e de abuso em uploads.
- Estado atual: [CONFIRMADO_NO_CODIGO] Fase inicial implementada em [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py); sanitizacao explicita de nome implementada em [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py); validacao leve por assinatura binaria implementada para `PDF`, `PNG` e `JPG/JPEG`; formatos como `DOC`/`DOCX` podem ser revistos numa fase posterior.
