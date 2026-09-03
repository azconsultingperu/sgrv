## Context

Ver `proposal.md`. El sistema actual en `app/static/js/main.js` (`mostrarToast`/`crearToast`) y `app/static/css/style.css` (`#toastContainer`, `.mc-toast`, `.mc-toast-icono`, `.mc-toast-cerrar`, `.mc-toast-progreso`) fue rediseñado a 6s, posición inferior, triángulo sin caja y hover con borde blanco. Quedan 4 ajustes finos: eliminar X y barra, centrar ícono y reforzar contraste en modo claro. `app/templates/base.html` expone un único `#toastContainer` compartido; el modo auth se distingue por `body:has(.login-card)` y `es-movil` ya bifurca posición. No hay spec previo de toasts; se crea `toast-system`.

## Goals / Non-Goals

**Goals:** Toast interno sin interacción manual, ícono centrado, sin barra, distinguible en modo claro, idéntico en ambos temas salvo fondo/sombra.
**Non-Goals:** Cambiar duración (ya 6000ms), posición inferior (ya abajo), ícono triángulo o tamaño de texto; tocar login/recuperar; alterar lógica de qué mensaje se muestra o cola `TOAST_MAX_VISIBLES=1`.

## Decisions

**1. Quitar X y barra del DOM (no solo CSS `display:none`)**
- Eliminar en `main.js` la creación de `cerrar` (`document.createElement('button')` con `mc-toast-cerrar`) y de `progreso` (`mc-toast-progreso`), sus `appendChild`, sus listeners (`cerrar.addEventListener('click')`, `mouseenter`/`mouseleave` que pausaban el timer) y referencias `_cerrar`/`_pausar`. El auto-cierre queda solo con `setTimeout(cerrarToast, 6000)` y animación `mcToastOut`.
- Alternativa `display:none` descartada: deja nodos interactivos y confunde tests a11y (`aria-label` fantasma). Borrado real simplifica y evita `pointer-events` residuales.
- Verificar que `colaToasts` siga limpiando toasts previos vía `querySelectorAll('.mc-toast')` + `remove()` directo, sin `_cerrar`.

**2. Centrar ícono con `align-items: center`**
- Cambiar `.mc-toast { align-items: flex-start }` → `center` (en `style.css`). El ícono es `grid` sin caja y el cuerpo es flex, así el triángulo queda centrado respecto a título+descripción de altura variable.
- Alternativa `align-self:center` solo en ícono descartada: no centra cuando la descripción es multilínea; `center` en el contenedor es más robusto.
- Mantener `gap:0.85rem` y `padding:1rem 1.1rem` del rediseño previo.

**3. Eliminar barra de progreso**
- Quitar en `main.js` el `div mc-toast-progreso`, su `style.animationDuration` y `animationPlayState` (pausa/reanuda en hover ya no aplica). El hover que pausaba el timer se elimina junto con la barra; el timer corre 6s uninterrupted.
- En `style.css` borrar `.mc-toast-progreso` y `@keyframes mcToastProgreso`. El `border-color` hover blanco se mantiene pero sin pausa.
- Riesgo de regresión de pausa en hover intencional → Mitigación: la pausa era para leer con calma; ahora el usuario no interactúa (punto 1), la lectura es pasiva 6s; se documenta como cambio de comportamiento.

**4. Contraste en modo claro**
- Añadir regla específica `:root` vs `[data-bs-theme="dark"]` para `.mc-toast` en modo claro: `background: var(--surface-1)` ya es blanco, pero se distingue con `box-shadow: 0 12px 32px rgba(15,23,42,0.14), 0 2px 8px rgba(15,23,42,0.08)` más marcado que `var(--shadow-md)`, y `border: 1.2px solid var(--border-color)` se mantiene. En modo oscuro no se altera.
- Alternativa fondo gris `var(--surface-2)` descartada: rompe percepción de toast como “tarjeta” y choca con `surface-2` del `app-bg`; sombra es menos invasiva y respeta `var(--surface-1)` del design system.
- Login toasts quedan exentos: `body:has(.login-card) .mc-toast` no recibe esta sombra extra; su `box-shadow` sigue como antes.

## Risks / Trade-offs

- **Sin X ni pausa, el usuario no puede descartar un error largo** → Mitigación: 6s es suficiente para leer título+mensaje ampliados; el siguiente toast reemplaza al anterior (`TOAST_MAX_VISIBLES=1`).
- **Quitar `animationPlayState` puede dejar `remaining` sin uso** → Mitigación: simplificar a `setTimeout` único; eliminar variables `pausado`/`corriendo` no usadas tras el cambio.
- **`body:has()` no soportado en Firefox <121** → Mitigación: ya usado para posición de toasts (desde rediseño previo); degradación es que login y sistema compartan posición inferior, aceptable y ya validado.
- **Sombra más fuerte en modo claro puede verse pesada** → Mitigación: calibrar con screenshots en ambos temas antes de cerrar; ajustar `rgba` si se percibe excesivo.

## Migration Plan

1. Editar `main.js` (quitar X/progreso/pausa) y `style.css` (centrar, quitar reglas, reforzar sombra claro).
2. Bump `?v=` en `base.html` para `style.css` y `main.js`.
3. Probar en Chrome/Firefox con `data-bs-theme` light/dark: verificar sin X en DOM, sin barra, ícono centrado, cierre solo a 6s, contraste claro, login arriba intacto.
4. Rollback: revertir 2 archivos + bump inverso; sin migración DB.

## Open Questions

- Ninguna.
