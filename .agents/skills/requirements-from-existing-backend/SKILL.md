---
name: requirements-from-existing-backend
description: Derivar requisitos funcionais e não funcionais a partir do backend já implementado. Use quando for preciso formalizar o que o sistema realmente faz antes de propor mudanças.
---

# Objetivo da skill

Transformar comportamento implementado em requisitos rastreáveis, distinguindo funcionais, não funcionais e de segurança.

## Quando usar

- Quando não existe especificação formal atualizada.
- Quando for necessário criar requisitos a partir do código em `docs/04-requirements/`.
- Quando a equipa quiser alinhar melhorias com o comportamento já entregue.

## Quando não usar

- Quando a tarefa for definir produto futuro sem dependência forte do backend atual.
- Quando ainda não houver compreensão básica da arquitetura e módulos.

## Entradas esperadas

- Código do backend
- Documentação parcial existente
- Testes que evidenciem comportamento

## Processo passo a passo

1. Ler módulos, rotas, regras de negócio, integrações e controles de acesso.
2. Extrair requisitos funcionais implementados e identificar `RF-001`, `RF-002`, etc.
3. Extrair requisitos não funcionais observáveis e identificar `RNF-001`, `RNF-002`, etc.
4. Incluir requisitos de autenticação, autorização, dados, auditoria, integração e segurança.
5. Associar cada requisito à sua evidência no código.
6. Gerar:
   - `docs/04-requirements/software-requirements-from-backend.md`
   - `docs/04-requirements/non-functional-requirements.md`

## Ficheiros e pastas que deve analisar

- Rotas, views, services e regras
- Configurações de runtime e segurança
- Código de auditoria, filas, storage e integrações
- Testes e scripts operacionais

## Documentos que deve gerar

- `docs/04-requirements/software-requirements-from-backend.md`
- `docs/04-requirements/non-functional-requirements.md`

## Regras de segurança

- Não confundir requisito desejado com requisito implementado.
- Requisitos de segurança devem citar a evidência técnica ou a ausência dela.

## Regras de qualidade

- Escrever requisitos de forma objetiva e verificável.
- Relacionar cada requisito a módulos e endpoints quando possível.
- Marcar lacunas importantes com `[PRECISA_VALIDAR]`.

## Formato de saída

- Markdown com blocos por requisito
- Campos recomendados:
  - ID
  - Descrição
  - Tipo
  - Evidência
  - Fonte no código
  - Rastreabilidade

## Exemplos de documentação

- `RF-001`: autenticar usuários por JWT.
- `RF-002`: listar casos apenas da organização do usuário.
- `RNF-001`: usar paginação padrão.
- `RNF-002`: registrar eventos de auditoria quando implementado.

## Critérios de validação

- Requisitos funcionais refletem o comportamento atual.
- Requisitos não funcionais possuem evidência observável.
- Requisitos de segurança, dados e integração foram considerados.
- A rastreabilidade com código está explícita.

