## 1. JS — restaurar X sin caja

- [x] 1.1 Re-agregar en `app/static/js/main.js` la creación del botón `mc-toast-cerrar` (`button` con `aria-label="Cerrar notificación"`, `textContent '✕'`, `appendChild` tras `cuerpo`, `addEventListener('click')` que hace `clearTimeout(temporizador); cerrarToast()`) sin reintroducir `mc-toast-progreso` ni `animationPlayState`/`pausarTemporizador`; verificar con `grep -n "mc-toast-cerrar" app/static/js/main.js` que retorna 1 línea y con `mostrarToast` manual que el toast tiene X visible y clic la cierra inmediato mientras que sin clic se auto-cierra a los 6000ms.

## 2. CSS — X sin caja y contraste light

- [x] 2.1 Restaurar en `app/static/css/style.css` la regla `.mc-toast-cerrar` (22x22, `background:transparent !important; border:none !important; box-shadow:none; color:var(--text-muted); cursor:pointer`) y `:hover` (`color:var(--text-primary); background:transparent !important;`) sin caja/fondo; verificar en DevTools que la X es solo ícono suelto.

- [x] 2.2 Verificar/corregir contraste en modo claro: inspeccionar que `[data-bs-theme="light"] .mc-toast` con `box-shadow: 0 12px 32px rgba(15,23,42,0.14), 0 2px 8px rgba(15,23,42,0.08)` se aplica y no es pisado por `body:has(.login-card) .mc-toast` u otra regla; si es pisado, ajustar especificidad/orden; verificar toggle sol/luna en dashboard que el toast en light se distingue del fondo blanco y en dark mantiene estilo, y que login sigue sin este refuerzo.

## 3. Sonido de error

- [x] 3.1 Copiar `~/Descargas/creatorshome-error-002-337159.mp3` a `app/static/sounds/error.mp3` (sobrescribir) con `cp` y verificar con `ls -lh app/static/sounds/error.mp3` y `ffprobe` o `file` que es audio/mpeg y reproduce al disparar `mostrarToast('error',...)` con volumen 0.35.

## 4. Verificación y bump

- [x] 4.1 Probar en dashboard/registrar/consultar en modo claro y oscuro que toasts: tienen X sin caja clickeable que cierra inmediato, sin barra, ícono centrado, auto-cierre 6s, no cierran al clickear cuerpo, login/recuperar siguen arriba sin cambios; hacer bump de `?v=` en `app/templates/base.html` para `style.css` y `main.js` y verificar recarga.
