# Request Response Examples

## Login JWT

### Request

```json
{
  "email": "admin@example.com",
  "password": "strongpass123"
}
```

### Response

```json
{
  "access": "<jwt>",
  "refresh": "<jwt>"
}
```

- Estado: [CONFIRMADO_NO_CÓDIGO]

## Criar caso

### Request

```json
{
  "title": "Ação Trabalhista",
  "description": "Reclamação de horas extras",
  "client_id": "<uuid>",
  "lawyer_id": "<uuid>",
  "organization_id": "<uuid>",
  "status": "open"
}
```

### Response parcial

```json
{
  "id": "<uuid>",
  "title": "Ação Trabalhista",
  "description": "Reclamação de horas extras",
  "status": "open",
  "organization_id": "<uuid>"
}
```

- Estado: [CONFIRMADO_NO_CÓDIGO]

## Atualizar perfil

### Request

```json
{
  "name": "Usuário Atualizado"
}
```

### Response parcial

```json
{
  "id": "<uuid>",
  "email": "user@example.com",
  "name": "Usuário Atualizado",
  "role": "admin"
}
```

- Estado: [CONFIRMADO_NO_CÓDIGO]

## Gerar petição com IA

### Request

```json
{
  "contexto": "Resumo do caso",
  "tipo": "petição inicial"
}
```

### Response

```json
{
  "text": "..."
}
```

- Estado: [CONFIRMADO_NO_CÓDIGO]

## Erro de validação

### Response

```json
{
  "error": "validation_error",
  "details": {
    "organization_id": [
      "Este campo é obrigatório."
    ]
  }
}
```

- Estado: [INFERIDO_DO_CÓDIGO]

