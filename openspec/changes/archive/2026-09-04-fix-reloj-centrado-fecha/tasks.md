## 1. Fecha a Sept 04

- [x] 1.1 Cambiar `app/static/js/main.js` `actualizarReloj()` para generar `fechaCorta` como `${mes} ${pad(day)}` con array `['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']` y verificar en browser que el 04 sept muestra `Sept 04` (no `04 set`).
- [x] 1.2 Actualizar fallback `catch` del mismo bloque para usar el mismo array y verificar que `main.js` no lanza error si `toLocaleDateString` falla.

## 2. Centrado vertical perfecto

- [x] 2.1 Ajustar `app/static/css/style.css` `.clock-badge` y sus hijos (`#relojHora`, `#relojAmPm`, `#relojFecha` + icono) con `line-height:1; align-self:center;` e icono `display:block; flex-shrink:0;` y verificar en DevTools que icono y textos comparten misma línea media a 1024px y 375px.
- [x] 2.2 Revisar `app/templates/partials/navbar.html` `clock-badge` (padding/clases inline) para simetría vertical y verificar que a 375px solo hora es visible (`d-none d-sm-inline`) y a 1024px se ve `hh:mm:ss PM Sept 04` centrado.

## 3. Validación

- [x] 3.1 Verificar `title`/`aria-label` siguen en español largo con año (`Jueves, 04 de septiembre de 2026 — 02:05:22 PM (hora local)`) al hacer hover y con lector, y que no hay regresión en responsive.
- [x] 3.2 Ejecutar `openspec validate --change fix-reloj-centrado-fecha --strict` y `make lint-boundaries` (no aplicable) y confirmar validación pasa.
