## Why

El reloj del navbar (`#relojNavbar` en `navbar.html:12`) muestra hora y fecha pero con dos defectos visibles: (1) la fecha aparece como `04 set` (es-PE, día primero, minúsculas, 3 letras) cuando el usuario espera `Sept 04` (mes primero, inglés, 4 letras, capitalizado), y (2) el conjunto hora+AM/PM+fecha no está perfectamente centrado verticalmente respecto al icono Lucide `clock` (14px) — la fecha y el sufijo AM/PM de menor tamaño quedan con baseline desalineado y el badge se percibe desbalanceado.

## What Changes

- **Fecha `Sept 04` (opción A):** Cambiar `main.js:26` de `toLocaleDateString('es-PE', {day:'2-digit', month:'short'})` a un array manual `['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']` con formato `${mes} ${pad(day)}` capitalizado, sin año en el badge (el año queda solo en `title`/`aria-label`). Mantiene hora `hh:mm:ss AM/PM` 12h existente.
- **Centrado perfecto:** Ajustar `style.css:686` `.clock-badge` y `navbar.html:12-16` para que icono, `relojHora`, `relojAmPm` y `relojFecha` compartan `line-height:1`, `align-items:center` y `align-self:center`, eliminando desalineación por tamaños distintos. Icono con `display:block` y `flex-shrink:0`.
- **Sin regresión responsive:** Mantener `d-none d-sm-inline` para fecha en `<576px`; `title`/`aria-label` siguen con fecha larga en español (`Jueves, 04 de septiembre de 2026 — 02:05:22 PM (hora local)`).

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `navbar-clock`: Formato de fecha visible cambia de `DD MMM es-PE` a `MMM DD en-US custom Sept` y centrado vertical del badge.

## Impact

- `app/static/js/main.js` — lógica de `actualizarReloj()` (fechaCorta).
- `app/static/css/style.css` — `.clock-badge`, `#relojHora`, `#relojAmPm`, `#relojFecha` (line-height, align-self, tamaño icono).
- `app/templates/partials/navbar.html` — ajuste menor de clases/estilos inline del badge si hace falta para centrado.
- Sin cambios backend, sin migración, sin dependencias nuevas.
