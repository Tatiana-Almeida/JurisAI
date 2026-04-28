# Architecture Decisions

## ADR-001 Monólito modular

- [CONFIRMADO_NO_CÓDIGO] O sistema foi estruturado como monólito modular por apps Django.
- Consequência: simplicidade operacional inicial e forte partilha de contexto e modelos.

## ADR-002 Multi-tenant por organização

- [CONFIRMADO_NO_CÓDIGO] A organização é usada como boundary principal de dados.
- Consequência: necessidade de filtros e validações consistentes em todas as camadas.

## ADR-003 Assíncrono com Celery

- [CONFIRMADO_NO_CÓDIGO] Notificações e lembretes são processados em tasks.
- Consequência: dependência de Redis e worker ativo.

## ADR-004 Auditoria por signals globais

- [CONFIRMADO_NO_CÓDIGO] A auditoria é transversal via signals `pre_save/post_save/post_delete`.
- Consequência: baixo acoplamento explícito nas views, mas maior custo implícito e abrangência ampla.

