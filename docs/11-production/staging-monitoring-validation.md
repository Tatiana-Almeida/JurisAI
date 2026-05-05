# Staging Monitoring Validation

## Objetivo

Registar a validacao da camada minima de monitorizacao externa para o staging do JurisAI.

## Ferramenta escolhida

- Ferramenta recomendada: UptimeRobot
- URL monitorada esperada: `https://staging.seudominio.com/health/`
- Frequencia sugerida: 5 minutos

## Estado atual

- [CONFIRMADO_NO_CODIGO] O endpoint publico `/health/` existe e foi validado localmente em runtime real na `v1.0.0-rc.3`.
- [PRECISA_VALIDAR] Nao foi possivel confirmar uma URL publica HTTPS neste ambiente porque ainda nao ha dominio/subdominio real configurado para staging.
- [PRECISA_VALIDAR] A criacao do monitor externo, o alerta por email/webhook e o teste de indisponibilidade ainda dependem da conta/ferramenta operacional escolhida.

## Configuracao minima sugerida

- tipo: HTTPS monitor
- nome: `JurisAI Staging Health`
- target: `https://staging.seudominio.com/health/`
- intervalo: 5 minutos
- timeout: 30 segundos
- alerta: email ou webhook operacional

## Resultado

- monitorizacao externa: pending
- alertas: pending
- justificacao: falta dominio HTTPS publico e integracao operacional com a ferramenta escolhida

## Proximo passo

- configurar o subdominio publico de staging
- ativar o reverse proxy/TLS no host
- criar o monitor HTTPS externo
- testar alertas com indisponibilidade controlada
