# Current Architecture

## ADR-001 Resumo arquitetural

- [CONFIRMADO_NO_CÓDIGO] A arquitetura atual é um monólito modular em Django/DRF.
- [CONFIRMADO_NO_CÓDIGO] Cada domínio de negócio é modelado como uma app Django separada.
- [INFERIDO_DO_CÓDIGO] O boundary arquitetural principal é por módulo de domínio, não por microserviço.

## Camadas observadas

| Camada | Elementos | Estado |
|---|---|---|
| Entrada HTTP | URLs, routers, APIViews, ViewSets | [CONFIRMADO_NO_CÓDIGO] |
| Aplicação | Views, serializers, alguns services e tasks | [CONFIRMADO_NO_CÓDIGO] |
| Domínio/Persistência | Models Django e regras em methods simples | [CONFIRMADO_NO_CÓDIGO] |
| Infraestrutura | Celery, Redis, SMTP, Gunicorn, Docker | [CONFIRMADO_NO_CÓDIGO] |

## Fluxos arquiteturais principais

1. [CONFIRMADO_NO_CÓDIGO] Request entra por `jurisai.urls`.
2. [CONFIRMADO_NO_CÓDIGO] Middleware injeta contexto de organização.
3. [CONFIRMADO_NO_CÓDIGO] ViewSet/APIView aplica auth/permissões.
4. [CONFIRMADO_NO_CÓDIGO] Serializer cria/valida dados.
5. [CONFIRMADO_NO_CÓDIGO] Model é persistido pelo ORM.
6. [CONFIRMADO_NO_CÓDIGO] Signals podem gerar auditoria.
7. [CONFIRMADO_NO_CÓDIGO] Tasks Celery tratam automações assíncronas.

## Características

- [CONFIRMADO_NO_CÓDIGO] Forte dependência de convenções DRF e ORM.
- [CONFIRMADO_NO_CÓDIGO] Baixa separação formal entre aplicação e domínio em algumas regras.
- [CONFIRMADO_NO_CÓDIGO] Uso de mocks em integrações específicas.

