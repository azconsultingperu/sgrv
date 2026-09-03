## 1. JS — quitar X, barra y pausa

- [x] 1.1 Quitar en `app/static/js/main.js` la creación del botón `mc-toast-cerrar` (elemento, `aria-label`, `textContent '✕'`, `appendChild`, `addEventListener click`, propiedades `_cerrar`) y de la barra `mc-toast-progreso` (`createElement`, `className`, `style.animationDuration`, `appendChild`, `animationPlayState`), y su lógica de pausa/reanuda (`pausarTemporizador`/`iniciarTemporizador` con `mouseenter`/`mouseleave`, variables `pausado`/`corriendo`/`remaining` si quedan sin uso); verificar con `grep -n "mc-toast-cerrar\|mc-toast-progreso\|_cerrar\|pausarTemporizador" app/static/js/main.js` que retorna vacío y con `mostrarToast` manual en consola que el toast no tiene X ni barra en el DOM.

- [x] 1.2 Simplificar el auto-cierre a `setTimeout(cerrarToast, 6000)` sin `animationPlayState` y ajustar limpieza de cola (`querySelectorAll('.mc-toast')` + `remove()` directo) para que no dependa de `_cerrar`; verificar que dos toasts seguidos reemplazan al anterior y que el segundo se auto-cierra a los 6s sin interacción.

## 2. CSS — alineación, barra y contraste

- [x] 2.1 Cambiar en `app/static/css/style.css` `.mc-toast { align-items: flex-start }` a `center`, eliminar reglas `.mc-toast-cerrar` (y `:hover`), `.mc-toast-progreso` y `@keyframes mcToastProgreso`, y verificar visualmente en DevTools que el triángulo queda centrado verticalmente respecto a título+descripción y que no existe barra bajo el texto.

- [x] 2.2 Reforzar contraste en modo claro añadiendo regla para `[data-bs-theme="light"] .mc-toast` o `:root .mc-toast` con `box-shadow` más marcado (ej. `0 12px 32px rgba(15,23,42,0.14), 0 2px 8px rgba(15,23,42,0.08)`) manteniendo `border-left-color` de estado; verificar en Chrome/Firefox con `data-bs-theme` light que el toast se distingue del fondo blanco y en dark que no se degrada, y que `body:has(.login-card) .mc-toast` no recibe este refuerzo.

## 3. Verificación integrada

- [x] 3.1 Probar en `dashboard`, `registrar` y `consultar` (modo claro y oscuro) que los toasts: no tienen X, no tienen barra, ícono centrado, se auto-cierran solo a los 6s, no se cierran al clickear, y login/recuperar siguen con toasts arriba a la derecha sin cambios; hacer bump de `?v=` en `app/templates/base.html` para `style.css` y `main.js` y verificar que el navegador carga la nueva versión.
