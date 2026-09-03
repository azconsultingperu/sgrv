## Why

El rediseño de toasts aplicado en `redesign-toast-notifications` dejó 4 detalles pendientes que afectan usabilidad y contraste: el botón X es innecesario (el auto-cierre de 6s es suficiente), el ícono triangular está desalineado verticalmente, la barra de progreso visual es ruido, y en modo claro el toast se funde con el fondo blanco. Estos ajustes pulen el comportamiento final sin cambiar la lógica de qué mensaje se muestra.

## What Changes

- **BREAKING (UI):** Quitar por completo el botón X del toast — el componente ya no renderiza el elemento `mc-toast-cerrar`; el cierre es solo por auto-cierre a los 6s.
- Centrar verticalmente el ícono de alerta (triángulo) respecto al bloque de texto (título + mensaje) usando `align-items: center` en el contenedor flex del toast.
- Eliminar la barra/línea indicadora de tiempo restante (elemento `mc-toast-progreso` y su `animation`), manteniendo el `setTimeout` de 6s.
- Reforzar contraste en modo claro: fondo del toast ligeramente diferenciado del blanco puro de la página (ej. `var(--surface-1)` con sombra más marcada) para que se perciba flotante, manteniendo el borde de color de estado (rojo/verde/etc.) como diferenciador principal.

## Capabilities

### New Capabilities
- `toast-system`: Sistema centralizado de toasts/notificaciones internas (dashboard, registrar, consultar, etc.). Cubre auto-cierre, posición, ícono, alineación, indicador visual y contraste por tema. Excluye login/recuperar contraseña que mantienen su posición y comportamiento actuales.

### Modified Capabilities
- Ninguna — `notifications` (emails) no se toca; el cambio es solo UI de toasts.

## Impact

- `app/static/js/main.js` — eliminar creación y listeners del botón cerrar y de la barra de progreso; mantener `mostrarToast`/`crearToast` con solo `setTimeout(6000)`.
- `app/static/css/style.css` — ajustar `.mc-toast` (quitar `mc-toast-cerrar`, quitar `mc-toast-progreso`, cambiar `align-items` a `center`, reforzar `background`/`box-shadow` en modo claro).
- Sin impacto en backend, `app/templates/base.html` ni `auth.css`; login/recuperar no se ven afectados (verificado por `body:has(.login-card)`).
