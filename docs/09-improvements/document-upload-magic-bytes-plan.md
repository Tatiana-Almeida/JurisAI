# Document Upload Magic Bytes Plan

## 1. Resumo do problema

- [CONFIRMADO_NO_CODIGO] O upload de `Document` ja valida extensao, tamanho maximo e `content_type` em [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py).
- [CONFIRMADO_NO_CODIGO] O nome do ficheiro ja e sanitizado explicitamente em [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py).
- [CONFIRMADO_NO_CODIGO] Ainda nao existe validacao do cabecalho binario real do ficheiro.
- [INFERIDO_DO_CODIGO] Isso permite que um ficheiro com extensao e `content_type` coerentes continue a ser aceite mesmo que os primeiros bytes nao correspondam ao formato declarado.

## 2. Riscos

### SEC-UPL-SIG-001 Spoofing de PDF

- [CONFIRMADO_NO_CODIGO] Um upload `.pdf` com `content_type=application/pdf` nao e hoje inspecionado nos bytes iniciais.
- Impacto:
  - ficheiro arbitrario mascarado de PDF
  - reducao da confianca operacional no armazenamento

### SEC-UPL-SIG-002 Spoofing de imagem PNG/JPEG

- [CONFIRMADO_NO_CODIGO] Uploads `.png`, `.jpg` e `.jpeg` sao hoje aceites so por extensao e `content_type`.
- Impacto:
  - ficheiros nao-imagem aceites como imagem
  - UX inconsistente em visualizacao/download

### SEC-UPL-SIG-003 Cobertura incompleta para formatos ambiguos

- [CONFIRMADO_NO_CODIGO] Os tipos permitidos hoje sao:
  - `.pdf`
  - `.doc`
  - `.docx`
  - `.txt`
  - `.jpg`
  - `.jpeg`
  - `.png`
- [INFERIDO_DO_CODIGO] Nem todos esses formatos sao bons candidatos a validacao leve por assinatura nesta fase.

## 3. Formatos cobertos nesta fase

- [INFERIDO_DO_CODIGO] Recomenda-se cobrir agora apenas:
  - `PDF`
  - `PNG`
  - `JPG/JPEG`

Justificativa:
- possuem assinaturas binariais simples, bem conhecidas e de baixo custo
- permitem validacao deterministica sem dependencias externas
- atacam a parte mais comum e previsivel do spoofing residual

## 4. Formatos nao cobertos e justificativa

### `.doc`

- [INFERIDO_DO_CODIGO] DOC legado costuma usar cabecalho OLE Compound File.
- [PRECISA_VALIDAR] E validavel tecnicamente, mas e menos comum e pode merecer tratamento separado para nao misturar a primeira fase.

### `.docx`

- [CONFIRMADO_NO_CODIGO] DOCX e ZIP-based.
- [INFERIDO_DO_CODIGO] Validar apenas `PK` seria fraco demais, porque qualquer ZIP passaria.
- [INFERIDO_DO_CODIGO] Uma validacao util de DOCX exigiria olhar entradas internas do ZIP, o que foge da ideia de fase leve.

### `.txt`

- [CONFIRMADO_NO_CODIGO] TXT nao tem assinatura binaria fixa.
- [INFERIDO_DO_CODIGO] Nesta fase, deve continuar dependente de extensao + `content_type`.

## 5. Estrategia recomendada

- [INFERIDO_DO_CODIGO] Implementar validacao leve apenas quando a assinatura binaria for simples e confiavel.
- [INFERIDO_DO_CODIGO] Politica recomendada:
  - para formatos com assinatura conhecida nesta fase, **falhar fechado**
  - para formatos nao cobertos nesta fase, manter o comportamento atual de extensao + `content_type`
- [INFERIDO_DO_CODIGO] Isso reduz risco sem penalizar todos os formatos permitidos de uma vez.

## 6. Politica para PDF

- [INFERIDO_DO_CODIGO] Verificar se os primeiros bytes comecam com `%PDF`
- [INFERIDO_DO_CODIGO] Se nao comecarem, retornar `400`
- [INFERIDO_DO_CODIGO] A leitura pode ser pequena, por exemplo 8 a 16 bytes

## 7. Politica para PNG

- [INFERIDO_DO_CODIGO] Verificar a assinatura PNG:
  - `89 50 4E 47 0D 0A 1A 0A`
- [INFERIDO_DO_CODIGO] Se nao corresponder, retornar `400`

## 8. Politica para JPG/JPEG

- [INFERIDO_DO_CODIGO] Verificar prefixo JPEG:
  - `FF D8 FF`
- [INFERIDO_DO_CODIGO] Se nao corresponder, retornar `400`
- [PRECISA_VALIDAR] Esta validacao e leve e suficiente para a fase inicial, mesmo sem parse completo do ficheiro.

## 9. Politica para DOC/DOCX/TXT

- [INFERIDO_DO_CODIGO] Nesta fase:
  - `DOC`: manter validacao atual
  - `DOCX`: manter validacao atual
  - `TXT`: manter validacao atual
- [INFERIDO_DO_CODIGO] O motivo e evitar falso sentimento de seguranca com assinaturas fracas ou ambíguas.
- [PRECISA_VALIDAR] Se a equipa quiser, DOC legado pode virar candidato a fase seguinte.

## 10. Plano de testes

Antes da implementacao:
- [CONFIRMADO_NO_CODIGO] [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) cobre extensao, tamanho, `content_type`, tenant e filename.

Depois da implementacao:
1. PDF valido com cabecalho `%PDF` continua `201`
2. PDF com extensao correta e bytes invalidos retorna `400`
3. PNG valido com assinatura correta continua `201`
4. PNG com bytes invalidos retorna `400`
5. JPEG valido com `FF D8 FF` continua `201`
6. JPEG com bytes invalidos retorna `400`
7. `DOC`, `DOCX` e `TXT` continuam com comportamento anterior nesta fase
8. tenant isolation e path sanitization continuam verdes

## 11. Plano de implementacao

### Fase 1: helper leve de assinatura

1. [CONFIRMADO_NO_CODIGO] Criar helper pequeno para ler os primeiros bytes do upload sem consumir definitivamente o stream.
2. [CONFIRMADO_NO_CODIGO] Associar assinaturas conhecidas a `.pdf`, `.png`, `.jpg`, `.jpeg`.
3. [CONFIRMADO_NO_CODIGO] Reposicionar o ponteiro do ficheiro apos a leitura.

### Fase 2: integrar no serializer

1. [CONFIRMADO_NO_CODIGO] Reusar a validacao atual de extensao, tamanho e `content_type`.
2. [CONFIRMADO_NO_CODIGO] Adicionar validacao de assinatura binaria apenas para formatos cobertos.
3. [CONFIRMADO_NO_CODIGO] Retornar `400` em caso de mismatch.
4. [CONFIRMADO_NO_CODIGO] A implementacao ficou localizada em [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py).

### Fase 3: expandir cobertura de testes

1. [CONFIRMADO_NO_CODIGO] Adicionar cenarios positivos e negativos para PDF/PNG/JPEG.
2. [CONFIRMADO_NO_CODIGO] Garantir que os testes antigos permanecem verdes.

## 12. Criterios de aceitacao

- [INFERIDO_DO_CODIGO] Uploads PDF/PNG/JPEG com bytes incompatíveis passam a retornar `400`
- [CONFIRMADO_NO_CODIGO] Endpoint, schema, storage e payloads de sucesso permanecem iguais
- [CONFIRMADO_NO_CODIGO] Extensao, tamanho, `content_type` e sanitizacao de filename permanecem ativos
- [CONFIRMADO_NO_CODIGO] Isolamento multi-tenant permanece intacto

## 13. Rollback plan

1. Reverter apenas a validacao de magic bytes no serializer/helper.
2. Manter as validacoes ja existentes de extensao, tamanho, `content_type` e filename.
3. Reexecutar a suite de upload e a suite completa.

## 14. Perguntas para validacao humana

1. [PRECISA_VALIDAR] A equipa concorda em validar magic bytes apenas para `PDF`, `PNG` e `JPG/JPEG` nesta fase?
2. [PRECISA_VALIDAR] `DOC` legado deve entrar numa fase seguinte ou pode ficar fora?
3. [PRECISA_VALIDAR] `DOCX` deve permanecer sem inspecao interna por agora, evitando parse de ZIP nesta fase?
4. [PRECISA_VALIDAR] Em caso de mismatch binario, a resposta deve continuar simplesmente como `400` com erro de validacao generico?
