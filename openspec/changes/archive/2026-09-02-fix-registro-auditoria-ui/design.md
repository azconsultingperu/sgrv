## Context

Ver `proposal.md`. El layout usa `body {overflow:hidden}` y `.main-content {overflow-y:auto}`; la validación usaba `window.scrollY`/`scrollIntoView` sobre `window` y añadía `is-invalid` genérico. El filtro de carrera en `consulta` está en `col-md-2` con `{{ c.nombre[:20] }}` y `custom-select-menu` con `width:100%` del botón angosto.

## Goals / Non-Goals

**Goals:** Panel no reaparece al validar, sin bordes rojos genéricos, carrera sin corte.
**Non-Goals:** Cambiar colores de validación para casos custom (DNI duplicado sigue rojo), tocar backend, cambiar lógica de qué campos son `required`.

## Decisions

**1. Scroll en `main-content` en vez de `window`**
- Cambiar `progress` y `scrollToInvalid` para usar `mainContent.scrollTop` y `mainContent.scrollTo` con `target.offsetTop`. Alternativa mantener `window` descartada: en este layout `window.scrollY` siempre es 0 y fuerza reflow del `sidebar` fixed.

**2. Quitar is-invalid genérico**
- En `main.js` `form.checkValidity()===false`, no hacer `querySelectorAll(':invalid').forEach(el=>el.classList.add('is-invalid'))` ni `input-glow`. Solo hacer `scroll` al primer `:invalid` y dejar que `invalid-feedback` se muestre. Mantener `is-invalid` solo para `fetch` de DNI duplicado.
- Alternativa mantener borde rojo descartada por pedido explícito de quitarlo.

**3. Ancho de carrera**
- Cambiar `col-md-2` a `col-md-3` en `consulta/index.html` para el select de carrera y quitar `[:20]` en Jinja. Además `custom-select-menu` con `min-width:240px; width:max-content; max-width:320px` para que el menú no esté limitado al ancho del botón. Alternativa solo agrandar columna sin tocar menú descartada: el menú seguiría recortado si el botón es angosto.

## Risks / Trade-offs

- **Quitar is-invalid genérico reduce feedback visual** → Mitigación: queda `invalid-feedback` y toast, suficiente sin ruido rojo.
- **Menu más ancho puede desbordar en móvil** → Mitigación: `max-width:90vw` y `right:0` si no cabe a la izquierda.
- **Scroll en main-content puede no centrar bien** → Mitigación: `block:center` con `offset -120px` para dejar espacio bajo navbar.

## Migration Plan

1. Editar `main.js` (scroll y quitar is-invalid genérico), `style.css` (ancho menú), `registro/index.html` y `consulta/index.html` (col y [:20]).
2. Bump `?v=` en `base.html`.
3. Probar en móvil ocultar panel → validar vacío → panel no reaparece, sin bordes rojos, carrera completa.
4. Rollback: revertir 4 archivos.

## Open Questions

- Ninguna.
