## Why

En `consulta/detalle.html` la foto del alumno vive en la card izquierda (`col-md-4`) y los datos en la derecha (`col-md-8`). Al hacer scroll la izquierda se va arriba y el usuario pierde la referencia visual. Añadir `position:sticky` en desktop mantiene la foto anclada bajo el navbar mientras se lee la tabla larga, sin JS y sin afectar móvil.

## What Changes

- Añade clase `.detalle-foto-sticky` en `app/static/css/style.css` con `position:sticky; top:80px; align-self:flex-start; z-index:1` solo en `@media (min-width:768px)`. `80px` = 60px navbar + 16px aire + 4px borde, deja la card justo debajo del navbar sin solaparse.
- Aplica la clase a la card de foto en `app/templates/consulta/detalle.html` (`col-md-4 > .card`).
- En móvil (`<768px`) la clase no aplica y la grilla queda apilada normal (`col-12`).

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `consulta-detalle`: Detalle de alumno mantiene foto visible al hacer scroll en desktop.

## Impact

- `app/templates/consulta/detalle.html` — añade clase a card de foto
- `app/static/css/style.css` — nueva regla `.detalle-foto-sticky` con media query
- Sin cambios en modelo, rutas, JS ni migración.
