## Why

El login con datos inválidos no muestra el cartel de error (el mensaje se consume antes de llegar al sistema de toasts) y el usuario quiere un feedback sonoro de error. Sin ese aviso visible y audible, el fallo parece que no pasó nada.

## What Changes

- Mover `~/Descargas/vadim_makes_sound-ui-error-denied-sound-2-547856.mp3` a `app/static/sounds/error.mp3` (nombre indicativo, formato mp3) y exponerlo como asset estático.
- Corregir `app/templates/auth/login.html:14` que hace `{% set _ = get_flashed_messages(...) %}` y vacía la cola antes de `base.html:44` (`#flashData`), para que los mensajes `danger` lleguen al JS de `main.js:347` y se genere `mc-toast`.
- Enganchar sonido al sistema de notificaciones: en `main.js` cuando `mc-toast` es `danger`, crear `new Audio('/static/sounds/error.mp3')` con volumen bajo (~0.35), `preload="auto"`, y `play()` dentro del mismo gesto que crea el toast (respeta autoplay); si el navegador bloquea, ignorar silenciosamente y respetar `prefers-reduced-motion` como señal para no sonar si el usuario prefiere menos animación.
- Reutilizar el mismo sonido para `registrar` (cuando quede el toast único de "Faltan datos...") y `recuperar` (cuando se muestre el cartel genérico de error), sin duplicar código de audio.

## Capabilities

### New Capabilities
- `error-sound`: Sonido de error para notificaciones `danger` y su integración con el sistema de toasts.
- `login-toast-fix`: Corrección para que los mensajes de login inválido lleguen al contenedor de toasts y se muestren como `mc-toast danger`.

### Modified Capabilities
- _Ninguna_ — no altera `login-layout` ni `recover-password` más allá de asegurar que sus toasts ya suenen si son de error.

## Impact

- **Código afectado:** `app/templates/auth/login.html` (quitar consumo prematuro), `app/static/js/main.js` (hook de audio), `app/static/sounds/error.mp3` (nuevo asset), `app/templates/auth/recuperar.html` y `app/modules/registro/presentation/registro_controller.py` solo como consumidores del sonido (sin cambios extra si el toast ya es único).
- **Dependencias:** Ninguna nueva (mp3 estático).
- **Riesgo:** Bajo; el sonido respeta gesto de usuario y se silencia si el navegador lo bloquea; no toca lógica de autenticación ni BD.
