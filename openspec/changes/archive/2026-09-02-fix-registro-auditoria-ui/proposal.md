## Why

En móvil, ocultar el panel con la hamburguesa y luego validar el formulario de registro con campos vacíos hace que el panel reaparezca por un reflow de `scrollIntoView` sobre `window` en un layout con scroll en `.main-content`; además los bordes rojos `is-invalid`/`input-glow` en cada campo faltante generan ruido visual y el select de carrera en consultar muestra nombres truncados por ancho corto y `[:20]`.

## What Changes

- **Panel:** cambiar `scroll` y progreso de `window` a `main-content` (`mainContent.scrollTop` + `scrollIntoView` dentro de `main-content`) para que validar no dispare repaint del `sidebar`.
- **Bordes rojos:** quitar `is-invalid`/`input-glow` del handler genérico de `form.checkValidity()===false` (mantenerlo solo para casos con lógica custom como DNI duplicado); dejar solo `invalid-feedback` y toast.
- **Carrera en consultar:** ampliar filtro de `col-md-2` a `col-md-3` y hacer `custom-select-menu` con `min-width:240px; width:max-content; max-width:320px` para que nombres largos no se corten; quitar `[:20]` en Jinja.

## Capabilities

### New Capabilities
- `registro-auditoria-ui`: Correcciones de panel que no reaparece al validar, validación sin bordes rojos genéricos y filtro de carrera con ancho suficiente.

### Modified Capabilities
- Ninguna

## Impact

- `app/static/js/main.js` — fix de scroll/progreso a `main-content` y quitar `is-invalid` genérico.
- `app/static/css/style.css` — ajuste de `.card:has(.custom-select)` y `.custom-select-menu` ancho.
- `app/templates/registro/index.html`, `app/templates/consulta/index.html` — cambio de `col-md-2` a `col-md-3` y quitar `[:20]`, más `is-invalid` removido.
- Sin impacto en backend.
