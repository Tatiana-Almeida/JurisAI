# Document Upload Filename Sanitization Plan

## 1. Resumo do problema

- [CONFIRMADO_NO_CODIGO] O hardening inicial de uploads validou extensao, tamanho e `content_type` em [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py).
- [CONFIRMADO_NO_CODIGO] O nome original do ficheiro ainda entra diretamente no caminho final em [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py), concatenado como `uuid_filename`.
- [CONFIRMADO_NO_CODIGO] Nao existe sanitizacao explicita de `filename` no serializer nem no helper `document_upload_path`.
- [INFERIDO_DO_CODIGO] O comportamento seguro observado hoje para path traversal depende do tratamento atual do storage/nome resolvido pelo Django, nao de uma politica explicita do projeto.

## 2. Comportamento atual

- [CONFIRMADO_NO_CODIGO] `Document.file` usa `upload_to=document_upload_path` em [documents/models.py](/c:/projectos/JurisAI/documents/models.py).
- [CONFIRMADO_NO_CODIGO] `document_upload_path` monta:
  - `documents/<organization_id>/<law_case_id>/<uuid>_<filename>`
- [CONFIRMADO_NO_CODIGO] O helper preserva o `filename` original no sufixo do nome final.
- [CONFIRMADO_NO_CODIGO] O serializer atual nao inspeciona:
  - separadores de path
  - espacos
  - acentos
  - caracteres especiais
  - comprimento do nome
  - extensoes duplicadas
- [CONFIRMADO_NO_CODIGO] A suite [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) hoje so confirma que um nome com `../../evil.pdf` e rejeitado ou salvo sem `..` no caminho persistido.

## 3. Riscos

### SEC-UPL-NAME-001 Dependencia implícita do storage para traversal

- [CONFIRMADO_NO_CODIGO] O projeto nao aplica politica propria para remover `../` ou `..\\`.
- [INFERIDO_DO_CODIGO] Isso deixa a defesa dependente do backend de storage e do comportamento atual do Django.

### SEC-UPL-NAME-002 Nomes com caracteres problematicos

- [CONFIRMADO_NO_CODIGO] O nome original e preservado no caminho final.
- [INFERIDO_DO_CODIGO] Espacos repetidos, acentos, simbolos e caracteres de controlo podem gerar:
  - caminhos pouco previsiveis
  - dificuldade operacional
  - comportamento divergente entre filesystems

### SEC-UPL-NAME-003 Nomes excessivamente longos

- [CONFIRMADO_NO_CODIGO] Nao existe limite observavel para o comprimento do nome original antes de ser concatenado ao UUID.
- [INFERIDO_DO_CODIGO] Nomes longos podem gerar paths longos demais em Windows ou no storage final.

### SEC-UPL-NAME-004 Extensoes duplicadas ou nomes enganosos

- [CONFIRMADO_NO_CODIGO] A validacao atual olha para `Path(filename).suffix.lower()`, isto e, a ultima extensao.
- [INFERIDO_DO_CODIGO] `file.pdf.exe` ja sera rejeitado pelo hardening atual porque a ultima extensao e `.exe`.
- [PRECISA_VALIDAR] Ainda pode valer a pena normalizar o basename para evitar nomes confusos mesmo quando a ultima extensao e valida, como `relatorio.final.v2..pdf`.

## 4. Estrategia recomendada

- [INFERIDO_DO_CODIGO] Recomenda-se **sanitizar**, nao rejeitar por defeito, para manter UX e compatibilidade com uploads legitimos.
- [INFERIDO_DO_CODIGO] A rejeicao deve ficar reservada a casos extremos, como nome vazio apos sanitizacao.
- [INFERIDO_DO_CODIGO] A politica mais segura e pequena nesta fase e:
  1. extrair o basename do ficheiro
  2. remover componentes de path
  3. normalizar espacos
  4. substituir caracteres inseguros por `_`
  5. limitar o comprimento do nome base
  6. preservar a extensao validada
  7. manter o UUID no prefixo

## 5. Politica para path traversal

- [INFERIDO_DO_CODIGO] Sempre ignorar qualquer componente de diretoria enviada pelo cliente.
- [INFERIDO_DO_CODIGO] Usar apenas o basename do nome original antes de qualquer outra operacao.
- [INFERIDO_DO_CODIGO] Se o basename sanitizado ficar vazio, usar fallback controlado como `document`.
- [INFERIDO_DO_CODIGO] O resultado final nao deve conter:
  - `..`
  - `/`
  - `\\`

## 6. Politica para caracteres especiais

- [INFERIDO_DO_CODIGO] Recomenda-se politica ASCII-safe minima:
  - manter letras, numeros, `-`, `_`, `.`
  - converter espacos internos para `_`
  - remover ou substituir restantes caracteres por `_`
- [PRECISA_VALIDAR] Se a equipa quiser preservar acentos, isso deve ser decisao explicita; a opcao mais previsivel e normalizar para ASCII simples.

## 7. Politica para nomes longos

- [INFERIDO_DO_CODIGO] Limitar apenas o basename, preservando a extensao.
- [INFERIDO_DO_CODIGO] Limite inicial sugerido para o nome original sanitizado: **80 caracteres** no basename.
- [INFERIDO_DO_CODIGO] O path final continuaria suficientemente curto porque ja usa UUID e estrutura fixa por tenant/case.

## 8. Politica para extensoes duplicadas

- [CONFIRMADO_NO_CODIGO] A whitelist atual ja bloqueia a ultima extensao nao permitida.
- [INFERIDO_DO_CODIGO] Nomes com multiplos pontos podem continuar a ser aceites se a extensao final for valida, mas o basename deve ser normalizado.
- [INFERIDO_DO_CODIGO] Nao e necessario bloquear automaticamente `report.final.v2.pdf`; basta sanitizar.

## 9. Arquivos provavelmente afetados

- [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py)
- [documents/serializers.py](/c:/projectos/JurisAI/documents/serializers.py) [PRECISA_VALIDAR]
- [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)
- possivelmente novo teste unitario pequeno para helper de filename [INFERIDO_DO_CODIGO]

## 10. Plano de testes

Antes da implementacao:
- [CONFIRMADO_NO_CODIGO] A suite atual ja cobre path traversal com criterio “rejeitado ou sanitizado”.

Depois da implementacao:
1. endurecer o teste de traversal para exigir sanitizacao explicita no nome persistido quando o upload e aceite
2. adicionar teste para nome com espacos e caracteres especiais
3. adicionar teste para nome muito longo
4. adicionar teste para nome com multiplos pontos e extensao valida
5. rerodar a suite completa para garantir que tenant isolation e validacao de tipo/tamanho permanecem intactos

## 11. Plano de implementacao

### Fase 1: helper local de sanitizacao

1. [CONFIRMADO_NO_CODIGO] Criar helper pequeno para normalizar `filename`.
2. [CONFIRMADO_NO_CODIGO] Aplicar o helper dentro de `document_upload_path`.
3. [CONFIRMADO_NO_CODIGO] Preservar extensao final ja validada pelo serializer.
4. [CONFIRMADO_NO_CODIGO] A implementacao ficou em [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py), mantendo `UUID` no prefixo e a estrutura por tenant/case.

### Fase 2: endurecer testes

1. [CONFIRMADO_NO_CODIGO] Atualizar teste de traversal para comportamento explicito.
2. [CONFIRMADO_NO_CODIGO] Adicionar cobertura para espacos/caracteres especiais e nomes longos.
3. [CONFIRMADO_NO_CODIGO] Adicionar cobertura para basename com multiplos pontos.

### Fase 3: revisao opcional de UX

1. Validar se vale a pena expor nome original separado no futuro.
2. Nao fazer isso nesta etapa, porque hoje nao existe campo proprio e nao e necessario para seguranca minima.

## 12. Criterios de aceitacao

- [INFERIDO_DO_CODIGO] O caminho salvo nunca contem componentes de path fornecidos pelo cliente.
- [INFERIDO_DO_CODIGO] O nome persistido usa apenas caracteres seguros e comprimento controlado.
- [CONFIRMADO_NO_CODIGO] O endpoint, schema e payloads de sucesso permanecem iguais.
- [CONFIRMADO_NO_CODIGO] A validacao multi-tenant e a politica de tipo/tamanho permanecem intactas.

## 13. Rollback plan

1. Reverter apenas a sanitizacao adicionada no helper de upload.
2. Reexecutar [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py) e a suite completa.
3. Voltar temporariamente ao comportamento atual dependente do storage enquanto a politica e reavaliada.

## 14. Perguntas para validacao humana

1. [PRECISA_VALIDAR] A equipa prefere sanitizacao silenciosa como padrao, ou rejeicao para nomes problematicos?
2. [PRECISA_VALIDAR] E aceitavel normalizar tudo para um conjunto ASCII-safe?
3. [PRECISA_VALIDAR] O limite de 80 caracteres no basename e adequado?
4. [PRECISA_VALIDAR] Vale a pena manter espacos como `_` ou a equipa prefere `-`?
5. [PRECISA_VALIDAR] Ha alguma necessidade funcional de preservar o nome original exato para download/auditoria?
