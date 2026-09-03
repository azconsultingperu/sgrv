## Context

Ver `proposal.md` y spec `toast-system`. El toast actual en `app/static/css/style.css` usa `background: var(--surface-1)` (blanco/oscuro según tema) + `border-left-color` del estado y `color` del estado para texto/ícono. Con `data-bs-theme="light"` se añadió `box-shadow` reforzada para distinguirse del fondo, pero sigue mimetizándose. Los tonos de estado ya existen como CSS vars (`--danger-color: #c2413a` / `#f87171` en dark, etc.). No hay spec previa de fondo sólido; la lógica de `main.js` no cambia.

## Goals / Non-Goals

**Goals:** Fondo sólido por tipo (rojo/verde/ámbar/azul) con texto/ícono/X blancos, idéntico en light/dark, hover con borde blanco 1.2px funcionando, usando paleta existente.
**Non-Goals:** Cambiar duración 6s, posición inferior, ícono triángulo, lógica de cola o de qué mensaje se muestra; tocar `main.js` salvo si el X necesita ajuste de color; cambiar volumen/sonido.

## Decisions

**1. Mapear fondo sólido a vars existentes (modo claro)**
- `.mc-toast.error { background: var(--danger-color); border-color: var(--danger-color); color: #ffffff; }` y análogos para `success`/`warning`/`info` con `var(--success-color)` etc. En `warning` el ámbar `#b7791f` sobre blanco tiene contraste suficiente con texto blanco; si en pruebas el amarillo resulta poco legible, aclarar texto a `#ffffff` con `text-shadow: 0 1px 1px rgba(0,0,0,0.12)` como fallback.
- Alternativa usar `color-mix` para oscurecer/aclarar según tema descartada: el requisito pide idéntico en ambos temas, así que se usa el mismo var del tema claro (más saturado) en ambos. Si se usara el var de dark (`#f87171` rosado) en light se vería lavado.
- Se fija explícitamente `color: #ffffff` en el contenedor para que título/descripción hereden blanco; se sobrescribe `mc-toast-titulo`/`mc-toast-descripcion` que antes eran `var(--text-primary)`/`var(--text-secondary)`.

**2. Ícono y X en blanco**
- `.mc-toast-icono { color: #ffffff !important; background: transparent !important; }` y `.mc-toast-cerrar { color: rgba(255,255,255,0.92); } :hover { color: #ffffff; }`. Mantiene `width:28px` y `stroke-width:2.2` ya ampliados.
- Alternativa `filter: brightness(0) invert(1)` descartada: `color` con `currentColor` en SVG Lucide ya respeta `color`.

**3. Hover y sombra simplificados**
- Hover sigue `border-color:#ffffff` (1.2px ya definido en `.mc-toast`) — sobre fondo sólido el borde blanco es visible sin `box-shadow` extra. Se mantiene `transition: border-color 200ms ease`.
- Se elimina o simplifica la regla condicional `[data-bs-theme="light"] .mc-toast` con sombra reforzada: ya no necesaria porque el fondo sólido contrasta por color, no por sombra. Se puede dejar una sombra sutil uniforme `var(--shadow-md)` para elevación, igual en ambos temas, o borrar la regla light específica.

**4. Consistencia entre temas**
- No se bifurca por `data-bs-theme`; las 4 variantes usan los mismos `background` sólidos en light y dark. Si se quiere preservar accesibilidad en dark (donde `--danger-color` es `#f87171` más claro), se normaliza a usar el var de light (`#c2413a`) en ambos temas para que el rojo sea el mismo; documentar como decisión.

## Risks / Trade-offs

- **Amarillo/ámbar con texto blanco puede tener contraste bajo** → Mitigación: probar `warning` en ambos temas; si WCAG AA no pasa, usar texto `#111827` oscuro solo para `warning` o oscurecer el fondo a `#9a5f15`.
- **Fondo sólido tapa el contenido detrás pero puede sentirse pesado** → Mitigación: mantener `border-radius` y `box-shadow` sutil, no aumentar `padding`; el toast ya es `position:fixed` con `max-width:420px`.
- **Eliminar lógica light rompe si se revierte** → Mitigación: borrar solo la regla light específica, dejar `body:has(.login-card)` intacto si login debe seguir con fondo neutro (login no usa toast-system, pero por seguridad no tocar `#toastContainer`).

## Migration Plan

1. Editar `app/static/css/style.css`: redefinir `.mc-toast` base (sin `border-left-color`), 4 variantes con `background` sólido + `color:#fff`, texto/ícono/X en blanco, simplificar sombra light.
2. Bump `?v=` en `app/templates/base.html` si se edita CSS.
3. Probar `mostrarToast` para los 4 tipos en `dashboard` con toggle sol/luna: verificar fondo sólido, texto/ícono/X blancos, hover borde blanco, sin diferencia entre temas.
4. Rollback: revertir CSS y bump; sin migración DB.

## Open Questions

- Ninguna.
