## Context

Ver `proposal.md` (Why) y evidencia del spike: Pixel 7 emulado 360×640 — `body.scrollHeight == viewport` (el body ño scrollea), `.main-content` (`height:100dvh + overflow-y:auto`, `style.css:346`) es el único scroller, tablas de ~639px en 321px visibles, drawer abre bien pero sin ✕/Escape (solo backdrop), toasts con autodestrucción (descartados como causa). Layout en `base.html:26-36`, sidebar fija 244px (`style.css:415`), navbar sticky (`style.css:636`), toggle en `main.js:95-160`.

## Goals / Non-Goals

**Goals:**
- Scroll de página nativo en `<=991px` con zona segura inferior.
- Acciones de tabla alcanzables sin swipe adivinable en `<=767px`.
- Drawer con cierre completo en móvil.

**Non-Goals:**
- Rediseño visual o cambio de componentes (mismos botones, mismos permisos).
- Soporte de tablets en horizontal como caso aparte (heredan desktop `>991px`).
- Quitar el scroller interno en desktop.

## Decisions

### Decisión 1: Scroll al body solo en móvil (media `<=991px`)

- **Qué:** bajo la media, `.main-content` pierde `height:100dvh/overflow` y el `body` vuelve a ser el scroller; re-anclar `sticky` (navbar `top:0`, progreso registro) al nuevo contexto.
- **Por qué sobre barra de acciones fija global:** ataca la raíz (Chrome solo esconde su barra con body-scroll) y arregla TODAS las páginas de un golpe, sin añadir UI nueva que tape contenido.
- **Alternativa descartada:** mantener scroller interno + `100svh`/offsets manuales — frágil ante cada modelo de barra de navegador.

### Decisión 2: `env(safe-area-inset-bottom)` en el contenedor móvil

- **Qué:** `padding-bottom` con fallback (`12px` si el navegador ño soporta `env()`).
- **Por qué sobre margen por página:** una sola regla cubre formularios, tablas y detalle; `viewport-fit=cover` ya está declarado en `base.html:5`.

### Decisión 3: Acciones de tabla con columna fija a la derecha

- **Qué:** en `<=767px`, primera columna (identidad: DNI/nombre) + última (acciones) visibles; columnas intermedias con scroll horizontal indicado; o variante tarjetas si la tabla lo pide.
- **Por qué sobre solo `table-responsive`:** el responsive actual exige descubrir el swipe; la columna fija garantiza el contrato del spec sin reescribir cada tabla.

### Decisión 4: Cierre de drawer con ✕ + Escape + backdrop

- **Qué:** botón ✕ en el header del sidebar (visible solo `<=991px`), listener de Escape, se conserva backdrop y auto-cierre al navegar.
- **Por qué sobre swipe-only:** el swipe es difícil de descubrir y de testear determinísticamente; ✕+Escape son explícitos y verificables en emulación.

### Decisión 5 (respaldo): barra de acciones fija inferior si el body-scroll no basta

- **Qué (solo si 4.2 física falla):** barra `position:fixed; bottom:0` con Guardar/Actualizar/Volver y `padding-bottom: env(safe-area-inset-bottom)`, visible solo `<=991px`, con `padding-bottom` compensatorio en el contenido para no taparlo.
- **Por qué:** el emulador no reproduce la barra dinámica real de Chrome; si esta tapa el final aun con body-scroll, la barra fija lo independiza del viewport.
- **Activación:** solo si el protocolo de 4.2 confirma solape del navegador real; no se implementa preventivamente.

## Risks / Trade-offs

- [Riesgo] `sticky` rotos al cambiar de scroller (navbar, progreso registro, headers de tabla) → **Mitigación:** matriz de verificación por página en tasks + screenshots emulados antes/después.
- [Riesgo] `lockMainScroll` (preventDefault en touchmove) deja la página congelada si el estado del drawer se desincroniza → **Mitigación:** el cierre por ✕/Escape reutiliza `closeSidebar()` existente (única vía de desbloqueo), con test de tap fuera del drawer.
- [Riesgo] `overflow-x: clip` de `.main-content` recorta dropdowns a la derecha en desktop → **Mitigación:** fuera de scope móvil salvo que un scenario lo exija; se anota como deuda.
- [Trade-off] El emulador ño reproduce 1:1 la barra dinámica de Chrome real → validación final en dispositivo físico del usuario (criterio de aceptación en tasks).

## Migration Plan

1. Deploy CSS/JS/templates (sin migración de BD).
2. Verificar en emulación 360×640 los scenarios del spec (screenshots antes/después).
3. Rollback: revert de los 3 archivos (`style.css`, `main.js`, `sidebar.html`) — cambio puramente frontend.
4. Usuario confirma en su teléfono (admin + operador) y se archiva el change.

## Open Questions

- Ninguna bloqueante. Detalle diferible: variante tarjetas vs columna fija por tabla (lo decide implementación según cada tabla, ambas cumplen el spec).
