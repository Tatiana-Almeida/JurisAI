# Document Upload Hardening Plan

## 1. Resumo do estado atual

- [CONFIRMADO_NO_CODIGO] `Document.file` e um `FileField` opcional em [documents/models.py](/c:/projectos/JurisAI/documents/models.py).
- [CONFIRMADO_NO_CODIGO] O serializer [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py) apenas passa `file` para `Document.objects.create(...)`.
- [CONFIRMADO_NO_CODIGO] Nao ha validacao explicita observavel de:
  - tamanho de ficheiro
  - extensao
  - MIME type
  - content type real
  - sanitizacao de nome de ficheiro
- [CONFIRMADO_NO_CODIGO] O caminho de upload usa [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py), com:
  - prefixo `documents/<organization>/<case>/`
  - `uuid4()` no nome final
  - preservacao do nome original no sufixo
- [CONFIRMADO_NO_CODIGO] O acesso a documentos e protegido por autenticacao e filtro por tenant em [documents/views.py](/c:/projectos/JurisAI/documents/views.py).

## 2. Riscos encontrados

### SEC-UPL-001 Upload de ficheiros executaveis ou nao permitidos

- [CONFIRMADO_NO_CODIGO] Nao ha whitelist observavel de extensoes ou tipos.
- Impacto:
  - upload de binarios indevidos
  - aumento de superficie para abuso operacional

### SEC-UPL-002 Upload de ficheiros grandes

- [CONFIRMADO_NO_CODIGO] Nao ha limite de tamanho observavel no model, serializer ou settings.
- Impacto:
  - consumo excessivo de disco
  - requests grandes
  - possivel degradacao do worker/web

### SEC-UPL-003 Content-type spoofing

- [CONFIRMADO_NO_CODIGO] Nao ha validacao observavel de MIME type ou inspecao basica do conteudo.
- Impacto:
  - ficheiro com extensao aceitavel mas conteudo inesperado

### SEC-UPL-004 Nome de ficheiro com caracteres problematicos

- [CONFIRMADO_NO_CODIGO] O helper de upload preserva o `filename` original no sufixo.
- [INFERIDO_DO_CODIGO] O UUID reduz colisao, mas nao elimina necessidade de politica minima para nomes.

### SEC-UPL-005 Path traversal

- [INFERIDO_DO_CODIGO] O risco e reduzido porque o caminho e composto por `Path(...)` + UUID + nome, e o Django storage costuma normalizar o nome.
- [PRECISA_VALIDAR] Ainda e prudente aplicar politica defensiva de nome para nao depender apenas do storage backend.

## 3. Arquivos afetados

- [documents/models.py](/c:/projectos/JurisAI/documents/models.py)
- [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py)
- [documents/views.py](/c:/projectos/JurisAI/documents/views.py)
- [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py)
- [jurisai/settings.py](/c:/projectos/JurisAI/jurisai/settings.py) [PRECISA_VALIDAR]
- novos testes de upload em `tests/` [PRECISA_VALIDAR]

## 4. Estrategia recomendada

- [INFERIDO_DO_CODIGO] Aplicar endurecimento no serializer, nao no endpoint nem no schema.
- [INFERIDO_DO_CODIGO] Centralizar a politica minima em utilitarios compartilhados ou constantes pequenas para:
  - extensoes permitidas
  - MIME types permitidos
  - tamanho maximo
  - nome de ficheiro
- [INFERIDO_DO_CODIGO] Manter o contrato da API, rejeitando ficheiros invalidos com `400`.
- [INFERIDO_DO_CODIGO] Nao mudar o storage nesta fase; focar primeiro em validacao de entrada.

## 5. Limites sugeridos de tamanho

- [INFERIDO_DO_CODIGO] Limite inicial sugerido: **10 MB** por ficheiro.

Justificativa:
- conservador para ambiente local e media storage local
- suficiente para PDFs, contratos e pecas comuns
- baixo risco operacional

- [PRECISA_VALIDAR] A equipa pode preferir 5 MB ou 20 MB dependendo do uso real.

## 6. Extensoes permitidas

- [INFERIDO_DO_CODIGO] Whitelist inicial sugerida:
  - `.pdf`
  - `.doc`
  - `.docx`
  - `.txt`
  - `.jpg`
  - `.jpeg`
  - `.png`

- [PRECISA_VALIDAR] Se `evidence` precisar suportar mais formatos, rever antes de implementar.

## 7. MIME types permitidos

- [INFERIDO_DO_CODIGO] MIME types iniciais sugeridos:
  - `application/pdf`
  - `application/msword`
  - `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  - `text/plain`
  - `image/jpeg`
  - `image/png`

- [PRECISA_VALIDAR] Validacao so por `content_type` do upload e fraca; idealmente combinar:
  - extensao
  - content type informado
  - opcionalmente inspecao leve do cabecalho/magic bytes em fase posterior

## 8. Politica para nomes de ficheiro

- [INFERIDO_DO_CODIGO] Politica minima sugerida:
  - remover path separators
  - normalizar espacos
  - limitar comprimento do nome original
  - preservar apenas caracteres seguros
- [CONFIRMADO_NO_CODIGO] O UUID no prefixo do nome final ja reduz colisao, mas nao substitui sanitizacao.

## 9. Impacto no contrato da API

- [CONFIRMADO_NO_CODIGO] Os campos nao precisam mudar.
- [INFERIDO_DO_CODIGO] O contrato de sucesso pode permanecer igual.
- [INFERIDO_DO_CODIGO] O impacto funcional e que uploads antes aceites podem passar a ser rejeitados com `400` quando:
  - extensao nao permitida
  - MIME type nao permitido
  - tamanho excedido

## 10. Plano de testes antes da implementacao

- [CONFIRMADO_NO_CODIGO] Hoje nao ha teste dedicado de upload de ficheiro em `documents`.
- [INFERIDO_DO_CODIGO] Antes da implementacao, preparar cenarios de regressao para:
  - upload valido PDF
  - upload invalido por extensao
  - upload invalido por tamanho
  - upload com `law_case_id` valido no mesmo tenant
  - upload cross-tenant continua bloqueado

## 11. Plano de implementacao faseado

### Fase 1: validacao minima no serializer

1. [CONFIRMADO_NO_CODIGO] Validar tamanho maximo.
2. [CONFIRMADO_NO_CODIGO] Validar extensao por whitelist.
3. [CONFIRMADO_NO_CODIGO] Validar `content_type` quando disponivel.
4. [CONFIRMADO_NO_CODIGO] A politica inicial foi aplicada em [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py) com limite de 10 MB e whitelist para PDF, Office, texto e imagens JPEG/PNG.

### Fase 2: endurecimento de nome

1. Ajustar `document_upload_path` ou helper dedicado para sanitizar o nome original.
2. Garantir que o nome final continue unico e previsivel.

### Fase 3: reforco opcional

1. Avaliar inspecao basica de assinatura/magic bytes para PDF e imagens.
2. Rever se algum tipo adicional precisa ser suportado.

## 12. Criterios de aceitacao

- [INFERIDO_DO_CODIGO] Upload valido continua funcionando para tipos aprovados.
- [INFERIDO_DO_CODIGO] Upload com extensao indevida retorna `400`.
- [INFERIDO_DO_CODIGO] Upload acima do limite retorna `400`.
- [INFERIDO_DO_CODIGO] Nome de ficheiro nao consegue introduzir caminho arbitrario.
- [CONFIRMADO_NO_CODIGO] Nao ha mudanca de endpoint, schema ou payload de sucesso.

## 13. Riscos

- [PRECISA_VALIDAR] Pode bloquear ficheiros que hoje os utilizadores conseguem enviar.
- [INFERIDO_DO_CODIGO] Validacao so por extensao/content type pode gerar falso positivo ou falso negativo.
- [INFERIDO_DO_CODIGO] Se o limite de tamanho for pequeno demais, pode afetar documentos reais.

## 14. Rollback plan

1. Reverter apenas as validacoes adicionadas no serializer/helper.
2. Reexecutar testes de documents e suite completa.
3. Manter a politica antiga enquanto se redefine whitelist/limites.

## 15. Perguntas para validacao humana

1. [PRECISA_VALIDAR] Quais formatos de ficheiro precisam ser oficialmente suportados?
2. [PRECISA_VALIDAR] O limite inicial de 10 MB e aceitavel?
3. [PRECISA_VALIDAR] `evidence` precisa aceitar imagens alem de PDF e Office?
4. [PRECISA_VALIDAR] A equipa quer inspecao leve de assinatura de ficheiro ja na primeira fase ou isso fica para uma fase posterior?
