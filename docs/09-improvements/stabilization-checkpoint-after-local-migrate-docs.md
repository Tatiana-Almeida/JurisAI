# Stabilization Checkpoint After Local Migrate Docs

## 1. Resumo da estabilizacao

- [CONFIRMADO_NO_CODIGO] O projeto passou a documentar explicitamente dois fluxos distintos para `manage.py migrate`.
- [CONFIRMADO_NO_CODIGO] O fluxo Docker/Compose continua usando PostgreSQL com `POSTGRES_HOST=db`.
- [CONFIRMADO_NO_CODIGO] O fluxo local leve fora do Docker passou a usar SQLite de forma explicita com `DJANGO_USE_SQLITE=True`.
- [CONFIRMADO_NO_CODIGO] Nenhum fallback automatico silencioso foi introduzido.
- [CONFIRMADO_NO_CODIGO] `settings.py` permaneceu inalterado.

## 2. Arquivos alterados

- [.env.example](/c:/projectos/JurisAI/.env.example)
- [README.md](/c:/projectos/JurisAI/README.md)
- [docs/09-improvements/change-log.md](/c:/projectos/JurisAI/docs/09-improvements/change-log.md)

## 3. Fluxos documentados

### Docker / Compose

- [CONFIRMADO_NO_CODIGO] Subir servicos:
  - `docker compose up -d db redis`
- [CONFIRMADO_NO_CODIGO] Migrar:
  - `docker compose run --rm web python manage.py migrate`
- [CONFIRMADO_NO_CODIGO] Seed demo:
  - `docker compose run --rm web python manage.py seed_demo`
- [CONFIRMADO_NO_CODIGO] O host `db` e esperado neste fluxo.

### Local leve com SQLite

- [CONFIRMADO_NO_CODIGO] Ativar:
  - `DJANGO_USE_SQLITE=True`
- [CONFIRMADO_NO_CODIGO] Migrar:
  - `DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py migrate`
- [CONFIRMADO_NO_CODIGO] Seed demo:
  - `DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py seed_demo`
- [CONFIRMADO_NO_CODIGO] Testes:
  - `.\.venv\Scripts\python.exe -m pytest`
- [CONFIRMADO_NO_CODIGO] O uso de SQLite local continua explicito e nao deve ser usado em producao.

## 4. Comandos validados

- [CONFIRMADO_NO_CODIGO] `.\.venv\Scripts\python.exe -m pytest`

## 5. Resultado da suite

- [CONFIRMADO_NO_CODIGO] Resultado: `38 passed`

## 6. Riscos mitigados

- [CONFIRMADO_NO_CODIGO] O fluxo local de migracao deixou de depender de conhecimento implicito do developer.
- [CONFIRMADO_NO_CODIGO] A documentacao agora separa claramente ambiente local e ambiente Docker.
- [CONFIRMADO_NO_CODIGO] O risco de introduzir fallback silencioso para SQLite foi evitado.

## 7. Riscos restantes

- [CONFIRMADO_NO_CODIGO] `manage.py migrate` sem `DJANGO_USE_SQLITE=True` continua a exigir um host Postgres valido fora do Docker.
- [CONFIRMADO_NO_CODIGO] Permanecem warnings tecnicos conhecidos:
  - `USE_L10N`
  - `InsecureKeyLengthWarning`
  - `UnorderedObjectListWarning`

## 8. Recomendacao do proximo ciclo

- [INFERIDO_DO_CODIGO] O proximo ciclo mais seguro e escolher entre:
  - melhorar a UX do bootstrap local sem mexer em configuracao de producao
  - ou retomar hardening e refatoracoes internas de baixo/medio risco, como uploads de documentos
