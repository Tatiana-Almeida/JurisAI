# Stabilization Checkpoint After Upload Filename Sanitization

## 1. Resumo da melhoria

- [CONFIRMADO_NO_CODIGO] Foi adicionada uma politica explicita de filename seguro para uploads de `Document`.
- [CONFIRMADO_NO_CODIGO] A mudanca ficou restrita ao helper de upload path em [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py).
- [CONFIRMADO_NO_CODIGO] Endpoint, schema, payloads de sucesso, validacao de tipo/tamanho e isolamento multi-tenant permaneceram intactos.

## 2. Politica de sanitizacao aplicada

- [CONFIRMADO_NO_CODIGO] Usar apenas o basename do nome enviado.
- [CONFIRMADO_NO_CODIGO] Remover componentes de path e traversal.
- [CONFIRMADO_NO_CODIGO] Normalizar espacos para `_`.
- [CONFIRMADO_NO_CODIGO] Substituir caracteres inseguros por `_`.
- [CONFIRMADO_NO_CODIGO] Colapsar `_` repetidos.
- [CONFIRMADO_NO_CODIGO] Truncar o basename para `80` caracteres.
- [CONFIRMADO_NO_CODIGO] Preservar a extensao final.
- [CONFIRMADO_NO_CODIGO] Usar fallback `document` quando o basename sanitizado fica vazio.
- [CONFIRMADO_NO_CODIGO] Manter `UUID` no prefixo do nome persistido.

## 3. Helper criado

- [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py): `sanitize_upload_filename()`

## 4. Arquivos alterados

- [jurisai/utils.py](/c:/projectos/JurisAI/jurisai/utils.py)
- [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)
- [docs/09-improvements/change-log.md](/c:/projectos/JurisAI/docs/09-improvements/change-log.md)
- [docs/08-tests/recommended-test-cases.md](/c:/projectos/JurisAI/docs/08-tests/recommended-test-cases.md)
- [docs/09-improvements/document-upload-filename-sanitization-plan.md](/c:/projectos/JurisAI/docs/09-improvements/document-upload-filename-sanitization-plan.md)
- [docs/06-security/security-audit.md](/c:/projectos/JurisAI/docs/06-security/security-audit.md)
- [docs/07-quality/refactoring-plan.md](/c:/projectos/JurisAI/docs/07-quality/refactoring-plan.md)

## 5. Testes adicionados

- [CONFIRMADO_NO_CODIGO] Travessia de path com verificacao explicita do nome final seguro.
- [CONFIRMADO_NO_CODIGO] Normalizacao de espacos e caracteres especiais.
- [CONFIRMADO_NO_CODIGO] Truncamento de basename longo com extensao preservada.
- [CONFIRMADO_NO_CODIGO] Sanitizacao de basename com multiplos pontos.

Cobertura consolidada:
- [tests/test_document_upload_security.py](/c:/projectos/JurisAI/tests/test_document_upload_security.py)

## 6. Resultado da suite focal

- [CONFIRMADO_NO_CODIGO] `.\.venv\Scripts\python.exe -m pytest tests/test_document_upload_security.py`
- Resultado: `10 passed`

## 7. Resultado da suite completa

- [CONFIRMADO_NO_CODIGO] `.\.venv\Scripts\python.exe -m pytest`
- Resultado: `48 passed`

## 8. Riscos mitigados

- [CONFIRMADO_NO_CODIGO] Dependencia implícita do storage para lidar com `../` e `..\\`.
- [CONFIRMADO_NO_CODIGO] Persistencia de nomes com espacos e caracteres problematicos sem politica do projeto.
- [CONFIRMADO_NO_CODIGO] Paths com basename excessivamente longo.
- [CONFIRMADO_NO_CODIGO] Nomes pouco previsiveis com multiplos pontos no basename.

## 9. Riscos restantes

- [CONFIRMADO_NO_CODIGO] Ainda nao ha validacao por assinatura real de ficheiro (`magic bytes`).
- [CONFIRMADO_NO_CODIGO] A politica atual normaliza para um conjunto ASCII-safe; isso e previsivel e seguro, mas pode merecer decisao futura se a equipa quiser preservar nomes de exibicao com acentos.
- [CONFIRMADO_NO_CODIGO] Permanecem warnings tecnicos ja conhecidos:
  - `USE_L10N`
  - `InsecureKeyLengthWarning`
  - `UnorderedObjectListWarning`

## 10. Recomendacao do proximo ciclo

- [INFERIDO_DO_CODIGO] O proximo ciclo mais seguro e pequeno seria validar assinatura binaria (`magic bytes`) para PDF e imagens.
- [INFERIDO_DO_CODIGO] Se a prioridade for usabilidade em vez de seguranca adicional, a equipa pode antes decidir se quer preservar um nome original de exibicao separado do nome persistido.
