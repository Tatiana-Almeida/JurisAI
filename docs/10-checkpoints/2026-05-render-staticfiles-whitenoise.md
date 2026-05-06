# Checkpoint - Render Static Files WhiteNoise

## Objetivo

Corrigir a entrega de static files do Django Admin no Render com `DEBUG=False`.

## Problema

O Django Admin carregava, mas os ficheiros:

- `/static/admin/js/theme.js`
- `/static/admin/js/nav_sidebar.js`

retornavam `404`.

O navegador recusava CSS/JS por MIME type `text/html`.

## Causa

Gunicorn/Django com `DEBUG=False` nao serve static files sozinho.

## Correcao

- WhiteNoise adicionado ao `requirements.txt`.
- `WhiteNoiseMiddleware` configurado.
- `STATIC_ROOT` confirmado.
- `staticfiles` storage configurado.
- `collectstatic` mantido via `RUN_COLLECTSTATIC=True`.

## Validacao esperada

- `manage.py check` passa.
- `collectstatic` passa.
- `pytest` passa.
- Render deploy passa.
- `/static/admin/js/theme.js` retorna JavaScript.
- `/admin/` carrega com CSS/JS.
