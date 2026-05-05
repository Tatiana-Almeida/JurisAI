# Backup and Restore

## Objetivo

Definir uma base mínima de backup e restore para staging, com foco em PostgreSQL e documentos persistidos.

## PostgreSQL backup

Exemplo:

```powershell
docker compose -f docker-compose.staging.yml exec db pg_dump -U jurisai jurisai > backups/jurisai_YYYYMMDD.sql
```

## PostgreSQL restore

Exemplo:

```powershell
Get-Content backups\jurisai_YYYYMMDD.sql | docker compose -f docker-compose.staging.yml exec -T db psql -U jurisai jurisai
```

## Media backup

Além do banco, fazer backup do volume `media_data`, porque documentos jurídicos não devem depender apenas do dump relacional.

## Frequência sugerida

- diário para staging estável
- antes de qualquer migration relevante
- antes de testes destrutivos

## Retenção

- manter retenção mínima definida por política interna
- separar backups recentes e backups de referência

## Restore testado

Não basta gerar backup. O restore precisa ser testado periodicamente.

## Cuidado com dados sensíveis

- proteger dumps e ficheiros de media
- limitar acesso operacional
- apagar cópias temporárias inseguras
