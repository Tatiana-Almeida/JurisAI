# Integrations

## OpenAI

- [CONFIRMADO_NO_CÓDIGO] A integração ocorre em `ai_assistant.services.ai_service`.
- [CONFIRMADO_NO_CÓDIGO] Quando não há chave ou SDK disponível, o serviço retorna resposta mock.
- [PRECISA_VALIDAR] A compatibilidade exata com a versão declarada da SDK precisa ser confirmada.

## Email SMTP

- [CONFIRMADO_NO_CÓDIGO] O envio de email usa `django.core.mail.send_mail`.
- [CONFIRMADO_NO_CÓDIGO] Lembretes de prazo e notificações utilizam este canal.

## Stripe/Webhook

- [CONFIRMADO_NO_CÓDIGO] Existe um endpoint público para receber eventos de cobrança.
- [NÃO_ENCONTRADO] Validação de assinatura do webhook.

## Redis/Celery

- [CONFIRMADO_NO_CÓDIGO] Redis é usado como broker e result backend.
- [CONFIRMADO_NO_CÓDIGO] Há tasks para prazos, notificações e cobrança recorrente.
- [NÃO_ENCONTRADO] Serviço Celery Beat no `docker-compose.yml`.

## WhatsApp mock

- [CONFIRMADO_NO_CÓDIGO] O suposto envio de WhatsApp apenas cria um registo local `Notification`.

