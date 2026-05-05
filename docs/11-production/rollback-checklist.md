# Rollback Checklist

- identificar release atual
- identificar release anterior
- confirmar backup antes do deploy
- parar serviços
- voltar imagem/tag anterior
- restaurar banco se migration incompatível
- restaurar media se necessário
- subir serviços
- validar `/health/`
- rodar smoke tests
- revisar logs
- documentar incidente
