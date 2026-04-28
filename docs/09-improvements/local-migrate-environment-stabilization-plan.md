# Local Migrate Environment Stabilization Plan

## 1. Problema atual

- [CONFIRMADO_NO_CODIGO] `manage.py migrate` fora do Docker tenta usar PostgreSQL com `POSTGRES_HOST=db`.
- [CONFIRMADO_NO_CODIGO] Neste workspace, o host `db` nao existe fora do `docker-compose`, entao o comando falha localmente.
- [CONFIRMADO_NO_CODIGO] A validacao local das migrations precisou usar `DJANGO_USE_SQLITE=True`.
- [CONFIRMADO_NO_CODIGO] A suite de testes nao sofre com isso porque `pytest` ativa SQLite automaticamente via settings.

## 2. Causa provavel

- [CONFIRMADO_NO_CODIGO] [jurisai/settings.py](/c:/projectos/JurisAI/jurisai/settings.py) escolhe SQLite apenas quando:
  - `DJANGO_USE_SQLITE=True`
  - ou o processo detecta `pytest` em `sys.argv`
- [CONFIRMADO_NO_CODIGO] Caso contrario, o default e PostgreSQL com:
  - `HOST=os.getenv('POSTGRES_HOST', 'db')`
- [CONFIRMADO_NO_CODIGO] [.env.example](/c:/projectos/JurisAI/.env.example) define `POSTGRES_HOST=db` e nao documenta `DJANGO_USE_SQLITE`.
- [CONFIRMADO_NO_CODIGO] O [README.md](/c:/projectos/JurisAI/README.md) orienta o bootstrap principalmente via Docker.
- [INFERIDO_DO_CODIGO] O comportamento atual faz sentido dentro do Compose, mas e hostil para execucao local fora dele.

## 3. Diferenca entre ambiente local, Docker e producao

### Local fora do Docker

- [CONFIRMADO_NO_CODIGO] Sem `DJANGO_USE_SQLITE=True`, o projeto tenta conectar no host `db`.
- [INFERIDO_DO_CODIGO] Esse host so existe no network namespace do Docker Compose.

### Docker Compose

- [CONFIRMADO_NO_CODIGO] [docker-compose.yml](/c:/projectos/JurisAI/docker-compose.yml) define o servico `db`.
- [CONFIRMADO_NO_CODIGO] Nesse contexto, `POSTGRES_HOST=db` e coerente.

### Producao

- [INFERIDO_DO_CODIGO] Em producao, a expectativa e usar PostgreSQL real com variaveis explicitas.
- [INFERIDO_DO_CODIGO] Nao devemos enfraquecer esse caminho nem introduzir fallback silencioso para SQLite em producao.

## 4. Opcoes de correcao

### Opcao A: documentar e explicitar `DJANGO_USE_SQLITE=True` para ambiente local

- [INFERIDO_DO_CODIGO] Adicionar documentacao clara em `.env.example`, README e setup local.
- [INFERIDO_DO_CODIGO] Eventualmente criar um `.env.local` documentado para desenvolvimento sem Docker.

Vantagens:
- menor risco
- zero mudanca de logica de producao
- sem heuristicas implicitas

Desvantagens:
- depende de disciplina manual do developer

### Opcao B: ajustar `setup_local.py` para exportar/forcar SQLite localmente

- [INFERIDO_DO_CODIGO] O comando customizado poderia usar SQLite quando rodado fora do Docker.

Vantagens:
- melhora experiencia do bootstrap local

Desvantagens:
- mexe em comportamento de runtime do comando
- exige criterio confiavel para distinguir ambientes

### Opcao C: introduzir perfil explicito de ambiente local em settings

- [INFERIDO_DO_CODIGO] Exemplo: `DJANGO_ENV=local` ou `DJANGO_USE_SQLITE=True` melhor documentado e suportado.

Vantagens:
- mais claro e escalavel

Desvantagens:
- maior mudanca estrutural
- risco maior que o necessario para o problema atual

## 5. Opcao recomendada

- [INFERIDO_DO_CODIGO] Recomendo a **Opcao A**, com possivel complemento minimo da **Opcao B** apenas em documentacao/UX.

### Recomendacao concreta

1. Documentar `DJANGO_USE_SQLITE=True` como fluxo oficial para desenvolvimento local fora do Docker.
2. Atualizar `.env.example` para incluir a variavel comentada ou com default seguro de exemplo.
3. Atualizar README com dois caminhos explicitos:
   - Docker Compose com PostgreSQL/Redis
   - local leve com SQLite
4. Avaliar se `setup_local.py` deve apenas exibir uma mensagem orientando o uso de SQLite local, sem mudar logica ainda.

Essa abordagem preserva producao e reduz o risco de fallback implicito perigoso.

## 6. Impacto em seguranca

- [INFERIDO_DO_CODIGO] Baixo, se a mudanca ficar em documentacao e configuracao explicita.
- [CONFIRMADO_NO_CODIGO] Nao devemos fazer fallback automatico silencioso para SQLite em ausencia de Postgres, porque isso pode mascarar erro de configuracao em ambientes errados.
- [INFERIDO_DO_CODIGO] Exigir uma flag explicita (`DJANGO_USE_SQLITE=True`) e mais seguro.

## 7. Impacto em testes

- [CONFIRMADO_NO_CODIGO] `pytest` ja usa SQLite automaticamente por `RUNNING_PYTEST`.
- [INFERIDO_DO_CODIGO] O plano nao exige mudanca na estrategia atual de testes.
- [INFERIDO_DO_CODIGO] Pode ser util adicionar teste ou nota documental para o comportamento de selecao de banco, mas nao e obrigatorio no primeiro passo.

## 8. Impacto em documentacao

- [CONFIRMADO_NO_CODIGO] [README.md](/c:/projectos/JurisAI/README.md) precisa distinguir melhor Docker vs ambiente local puro.
- [CONFIRMADO_NO_CODIGO] [.env.example](/c:/projectos/JurisAI/.env.example) nao menciona `DJANGO_USE_SQLITE`.
- [INFERIDO_DO_CODIGO] `docs/00-code-discovery/runtime-and-scripts.md` e checkpoint(s) tecnicos tambem podem precisar de ajuste para refletir o fluxo local recomendado.

## 9. Plano de implementacao

### Fase 1: alinhamento documental

1. Adicionar `DJANGO_USE_SQLITE` ao `.env.example`.
2. Atualizar README com:
   - fluxo Docker
   - fluxo local com SQLite
3. Documentar exemplos de comando:
   - `DJANGO_USE_SQLITE=True .\.venv\Scripts\python.exe manage.py migrate`

### Fase 2: UX de bootstrap local

1. Avaliar se `setup_local.py` deve:
   - permanecer como esta
   - ou orientar o developer quando usado fora do Docker

### Fase 3: revisao opcional de settings

1. So se realmente necessario, considerar um perfil explicito de ambiente local.
2. Evitar fallback implicito para SQLite quando a intencao era usar Postgres.

## 10. Rollback plan

1. Reverter apenas mudancas de documentacao/configuracao local.
2. Manter `settings.py` de producao intacto.
3. Validar novamente:
   - fluxo Docker
   - fluxo local com SQLite

## 11. Criterios de aceitacao

- [INFERIDO_DO_CODIGO] Um developer consegue rodar `manage.py migrate` localmente sem Docker usando instrucoes oficiais do repositorio.
- [INFERIDO_DO_CODIGO] O fluxo Docker continua intacto com `POSTGRES_HOST=db`.
- [INFERIDO_DO_CODIGO] Nao ha fallback implicito perigoso para SQLite em producao.
- [INFERIDO_DO_CODIGO] A documentacao deixa claro qual caminho usar em cada ambiente.
