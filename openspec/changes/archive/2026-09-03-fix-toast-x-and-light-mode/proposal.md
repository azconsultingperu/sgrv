## Why

En `fix-toast-redesign-details` se eliminó por error el botón X por completo; la intención era solo quitar su caja/fondo, no la interacción. Además el contraste en modo claro (sombra reforzada) no fue verificado en light y el sonido de error sigue con el asset viejo.

## What Changes

- **Restaurar botón X** en `app/static/js/main.js`: re-agregar elemento `mc-toast-cerrar` con ícono `x` suelto, sin caja/fondo/borde, clic cierra inmediato (`clearTimeout` + animación) sin afectar el auto-cierre de 6s cuando no se hace click.
- **Verificar/corregir contraste en modo claro**: auditar selector de `app/static/css/style.css` para `[data-bs-theme="light"] .mc-toast` (sombra `0 12px 32px rgba(15,23,42,0.14), 0 2px 8px rgba(15,23,42,0.08)`), corregir especificidad si `body:has(.login-card)` u otra regla lo pisa, y comprobar en light y dark antes de cerrar.
- **Cambiar sonido de error**: reemplazar `app/static/sounds/error.mp3` por `~/Descargas/creatorshome-error-002-337159.mp3` (copiar y renombrar a `error.mp3`), manteniendo volumen 0.35, `preload auto` y manejo de `play()` rechazado.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `toast-system`: cambia de "sin X" a "con X suelto sin caja" manteniendo auto-cierre 6s, y precisa contraste en light.
- `error-sound`: cambia el asset fuente del sonido de error al nuevo archivo de Descargas.

## Impact

- `app/static/js/main.js` — reintroducir `mc-toast-cerrar` sin caja y su listener.
- `app/static/css/style.css` — regla `.mc-toast-cerrar` sin fondo/borde + verificación/fix de `data-bs-theme="light"` sombra.
- `app/static/sounds/error.mp3` — binario reemplazado (copia desde Descargas), sin cambio de ruta.
- `app/templates/base.html` — bump `?v=` para `style.css`/`main.js` si se editan.
