## Context

Ver `proposal.md`. Tras `fix-toast-redesign-details`, `main.js` eliminó `mc-toast-cerrar` y `mc-toast-progreso` dejando solo auto-cierre, y `style.css` centró el ícono y añadió `box-shadow` para light. Hay que revertir la eliminación de la X (pero sin caja) y auditar el selector de contraste que no fue probado en light. El sonido `error.mp3` sigue siendo el viejo `vadim_makes...`.

## Goals / Non-Goals

**Goals:** X suelto clickeable + auto-cierre 6s coexistiendo, contraste en light verificado y corregido si el selector estaba pisado, nuevo asset de error copiado.
**Non-Goals:** Cambiar duración, posición inferior, ícono triángulo o lógica de cola; tocar login/recuperar; cambiar volumen o `preload`.

## Decisions

**1. Restaurar X sin caja (main.js + style.css)**
- En `main.js` re-crear `cerrar` como `button.mc-toast-cerrar` con `aria-label`, `textContent '✕'`, `appendChild` después de `cuerpo`, y `cerrar.addEventListener('click', () => { clearTimeout(temporizador); cerrarToast(); })`. No reintroducir `mc-toast-progreso` ni `animationPlayState`/`pausarTemporizador`; el timer es solo `setTimeout(cerrarToast, 6000)` guardado en `temporizador` para cancelar al hacer click.
- En `style.css` restaurar regla `.mc-toast-cerrar` mínima: `display:grid; width:22px; height:22px; place-items:center; background:transparent !important; border:none !important; box-shadow:none; color:var(--text-muted); cursor:pointer;` y `:hover { color:var(--text-primary); background:transparent !important; }`. Sin caja ni fondo.
- Alternativa re-agregar pausa en hover descartada: el punto 1-3 ya eliminaron la pausa intencionalmente; el hover solo da `border-color:#fff`.

**2. Verificar contraste en light**
- Inspeccionar especificidad: `[data-bs-theme="light"] .mc-toast` con `box-shadow: 0 12px 32px rgba(15,23,42,0.14), 0 2px 8px rgba(15,23,42,0.08)` debe ganar a `var(--shadow-md)`. Si `body:has(.login-card) .mc-toast` lo pisa, aumentar especificidad a `[data-bs-theme="light"]:not(:has(.login-card))` o mover regla después de la de login. Probar con toggle sol/luna y DevTools computed `box-shadow`.
- Alternativa `background: var(--surface-2)` descartada: ya evaluada y se prefiere sombra.

**3. Cambiar sonido**
- `cp ~/Descargas/creatorshome-error-002-337159.mp3 app/static/sounds/error.mp3` (sobrescribir). Mantener `new Audio('/static/sounds/error.mp3')` con `volume 0.35`. No cambiar ruta en JS.
- Alternativa renombrar a nuevo archivo y cambiar JS descartada: rompería caché y requeriría actualizar referencia.

## Risks / Trade-offs

- **X sin caja puede parecer poco clickeable** → Mitigación: `cursor:pointer` y `color` muted que pasa a `text-primary` en hover, mismo patrón que ícono de alerta sin caja.
- **Selector light pisado por `body:has(.login-card)`** → Mitigación: verificar orden y especificidad; si persiste, añadir `:where()` o `!important` solo en `box-shadow`.
- **Nuevo mp3 más largo/pesado** → Mitigación: verificar tamaño (<200KB) y `preload auto` no bloquea; ya probado localmente.

## Migration Plan

1. Editar `main.js` (X) y `style.css` (X + sombra), copiar mp3, bump `?v=` en `base.html`.
2. Probar `mostrarToast('error','Error','msg')` en dashboard con light/dark: X visible sin caja, click cierra inmediato, sin click cierra a 6s, sin barra, ícono centrado, sombra distinguible en light, login intacto.
3. Rollback: revertir 3 archivos + restaurar `error.mp3` anterior desde git.

## Open Questions

- Ninguna.
