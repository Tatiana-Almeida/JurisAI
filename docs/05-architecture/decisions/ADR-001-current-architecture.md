# ADR-001 Current Architecture

## Contexto

- [CONFIRMADO_NO_CÓDIGO] O backend precisa suportar múltiplos domínios jurídicos relacionados.
- [CONFIRMADO_NO_CÓDIGO] O projeto centraliza auth, dados, integrações e tasks no mesmo repositório.

## Decisão observada

- [CONFIRMADO_NO_CÓDIGO] Adotar Django + DRF como núcleo do backend.
- [CONFIRMADO_NO_CÓDIGO] Organizar a solução por apps de domínio.
- [CONFIRMADO_NO_CÓDIGO] Usar Celery para processos assíncronos.
- [CONFIRMADO_NO_CÓDIGO] Usar `Organization` como boundary de tenant.

## Consequências

- [CONFIRMADO_NO_CÓDIGO] Desenvolvimento mais rápido com convenções fortes.
- [CONFIRMADO_NO_CÓDIGO] Regras de negócio tendem a ficar distribuídas entre views, serializers e services.
- [PRECISA_VALIDAR] O isolamento multi-tenant exige disciplina adicional para evitar bypass por relações cruzadas.

