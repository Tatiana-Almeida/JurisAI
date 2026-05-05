# Backup Schedule

## Objetivo

Definir uma rotina minima de backup para o PostgreSQL de staging sem guardar secrets no repositrio.

## Script associado

- `scripts/backup_postgres.sh`

## Frequencia sugerida

- diario: 1 backup por dia fora do horario de pico
- semanal: 1 backup adicional retido por 30 dias
- mensal: 1 backup adicional retido por 90 dias

## Exemplo de cron

```cron
15 2 * * * cd /srv/jurisai && BACKUP_DIR=/srv/jurisai/backups ./scripts/backup_postgres.sh >> /var/log/jurisai-backup.log 2>&1
```

## Politica de retencao

- ultimos 7 dias: manter backups diarios
- ultimos 30 dias: manter backups semanais
- ultimos 90 dias: manter backups mensais

## Regras operacionais

- guardar backups fora do volume ativo da aplicacao
- preferir copia adicional para armazenamento externo seguro
- encriptar o armazenamento externo quando possivel
- testar restore pelo menos mensalmente
- registar a data do ultimo restore verificado

## Validacao atual

- [CONFIRMADO_NO_CODIGO] O procedimento de backup e restore foi validado localmente na `v1.0.0-rc.3` com dump PostgreSQL e restore para base temporaria.
- [CONFIRMADO_NO_CODIGO] O script de backup criado nesta fase depende apenas de `.env.staging` e do compose de staging.
- [PRECISA_VALIDAR] O agendamento real via cron/systemd timer ainda depende do host de staging.
