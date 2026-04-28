# Backend Overview

## Escopo

- [CONFIRMADO_NO_CÓDIGO] O projeto é um backend monolítico modular em Python com Django e Django REST Framework.
- [CONFIRMADO_NO_CÓDIGO] O backend está organizado por apps de domínio: `accounts`, `organizations`, `law_cases`, `deadlines`, `documents`, `ai_assistant`, `billing`, `notifications` e `audit_logs`.
- [CONFIRMADO_NO_CÓDIGO] O módulo central `jurisai/` concentra configuração Django, URLs raiz, middleware, permissões, Celery, healthcheck, utilitários e tratamento de exceções.
- [CONFIRMADO_NO_CÓDIGO] O entrypoint de gestão local é [manage.py](/c:/projectos/JurisAI/manage.py).

## Objetivo funcional observado

- [CONFIRMADO_NO_CÓDIGO] O backend oferece autenticação JWT, gestão de usuários, organizações, casos jurídicos, prazos, documentos, pagamentos, notificações, auditoria e endpoints de IA.
- [CONFIRMADO_NO_CÓDIGO] O README descreve o produto como um SaaS jurídico com suporte multi-tenant por organização.
- [INFERIDO_DO_CÓDIGO] A organização é o boundary principal de tenant e segmentação de dados.

## Padrão geral de implementação

- [CONFIRMADO_NO_CÓDIGO] As apps seguem um padrão recorrente: `models.py`, `serializers.py`, `views.py`, `urls.py`, `migrations/`.
- [CONFIRMADO_NO_CÓDIGO] A API usa `ModelViewSet` para a maioria dos recursos CRUD.
- [CONFIRMADO_NO_CÓDIGO] O filtro por tenant é aplicado principalmente em `get_queryset()` das views e parcialmente nas permissões.
- [INFERIDO_DO_CÓDIGO] A camada de domínio está distribuída entre models, serializers, views e alguns serviços/tarefas assíncronas.

## Módulos principais

| Módulo | Responsabilidade principal | Estado |
|---|---|---|
| `accounts` | Usuários, cadastro, perfil, senha, autenticação via JWT | [CONFIRMADO_NO_CÓDIGO] |
| `organizations` | Organizações e limites por plano | [CONFIRMADO_NO_CÓDIGO] |
| `law_cases` | Casos jurídicos e soft delete | [CONFIRMADO_NO_CÓDIGO] |
| `deadlines` | Prazos processuais e lembretes | [CONFIRMADO_NO_CÓDIGO] |
| `documents` | Conteúdo e upload/versionamento de documentos | [CONFIRMADO_NO_CÓDIGO] |
| `ai_assistant` | Geração e histórico de solicitações de IA | [CONFIRMADO_NO_CÓDIGO] |
| `billing` | Pagamentos, assinaturas, faturas e webhook | [CONFIRMADO_NO_CÓDIGO] |
| `notifications` | Notificações por email e WhatsApp mock | [CONFIRMADO_NO_CÓDIGO] |
| `audit_logs` | Trilha de auditoria por signals | [CONFIRMADO_NO_CÓDIGO] |
| `jurisai` | Configuração, middleware, permissões e runtime | [CONFIRMADO_NO_CÓDIGO] |

## Fluxo de runtime observado

1. [CONFIRMADO_NO_CÓDIGO] A request entra pelo Django.
2. [CONFIRMADO_NO_CÓDIGO] O middleware `TenantMiddleware` injeta `request.organization` a partir de `request.user.organization`.
3. [CONFIRMADO_NO_CÓDIGO] O DRF autentica via JWT por padrão.
4. [CONFIRMADO_NO_CÓDIGO] As views aplicam permissões e filtram querysets por organização na maioria dos recursos.
5. [CONFIRMADO_NO_CÓDIGO] Serializers validam e criam objetos.
6. [CONFIRMADO_NO_CÓDIGO] Signals de `audit_logs` registram alterações em models elegíveis.
7. [CONFIRMADO_NO_CÓDIGO] Tarefas Celery são usadas para lembretes e envio de notificações.

## Achados relevantes

- [CONFIRMADO_NO_CÓDIGO] O backend usa `DefaultRouter` e `ModelViewSet`, o que reduz boilerplate das rotas.
- [CONFIRMADO_NO_CÓDIGO] A API tem tratamento de exceções centralizado em `jurisai.exceptions.custom_exception_handler`.
- [CONFIRMADO_NO_CÓDIGO] O código contém componentes mock ou parciais em IA e WhatsApp.
- [PRECISA_VALIDAR] O README afirma “pronto para produção”, mas há sinais de inconsistência operacional e de segurança que exigem validação antes dessa classificação.

## Pontos a validar

- [PRECISA_VALIDAR] Se existe `.env.example`, já que o README faz referência a ele e o ficheiro não foi lido nesta análise.
- [PRECISA_VALIDAR] Se há pipeline de CI/CD, lint e verificação automática fora do repositório atual.
- [PRECISA_VALIDAR] Se o ambiente real de produção usa PostgreSQL, Redis, Celery Beat e serviços de email/Stripe de forma completa.

