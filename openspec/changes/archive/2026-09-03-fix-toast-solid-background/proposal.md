## Why

El toast actual usa fondo neutro (blanco/oscuro según tema) con solo borde izquierdo de color, lo que lo hace mimetizarse con el fondo de la página y ser difícil de distinguir. Un fondo sólido del color de estado lo hace inmediatamente reconocible sin depender del tema.

## What Changes

- **BREAKING (UI):** Fondo del toast pasa de neutro a sólido del color de estado: error=rojo, éxito=verde, advertencia=ámbar/amarillo, info=azul. Usa los mismos tonos de `--danger-color`, `--success-color`, `--warning-color`, `--info-color` (modo claro) para consistencia.
- Texto (título + descripción) pasa a blanco/casi blanco (`#ffffff` o `rgba(255,255,255,0.92)`) para contraste sobre fondo sólido.
- Ícono (triángulo/circle-check/info) en blanco, sin caja, adaptado al fondo de color.
- Botón X (cuando exista) en blanco, sin caja, visible sobre fondo de color.
- Mantener hover con borde blanco 1.2px sin blur sobre el fondo sólido.
- Eliminar lógica condicional de contraste por tema (`[data-bs-theme="light"] .mc-toast` sombra reforzada) al no ser necesaria: el fondo sólido se ve idéntico en claro y oscuro.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `toast-system`: cambia de "fondo neutro + borde izquierdo de color" a "fondo sólido del color de estado con texto/ícono/X blancos e independiente del tema".

## Impact

- `app/static/css/style.css` — redefinir `.mc-toast`, `.mc-toast.success/error/warning/info` (background sólido, color texto, borde) y variantes `mc-toast-icono`/`mc-toast-cerrar`; simplificar/eliminar reglas `[data-bs-theme="light"] .mc-toast` y `body:has(.login-card)` si aplica.
- Sin impacto en `app/static/js/main.js` (lógica de mostrar/cerrar), backend o `base.html` salvo bump de `?v=` si se edita CSS.
