## Context

Ver `proposal.md` Why. Hoy `navbar.html:12` es un badge `inline-flex align-items:center gap-0.35rem` con 4 hijos: icono Lucide 14px + `#relojHora` (0.82rem/700) + `#relojAmPm` (0.68rem) + `#relojFecha` (0.74rem muted). `main.js:26` genera fecha vía `toLocaleDateString('es-PE', {day:'2-digit', month:'short'})` → `04 set`. El badge usa `min-height:34px` y `px-3 py-2` de Bootstrap; los spans de distinto tamaño rompen la línea base y el conjunto no se ve ópticamente centrado con el icono.

## Goals / Non-Goals

**Goals:** Fecha visible `Sept 04` (opción A, sin año), centrado vertical perfecto icono↔texto, mantener AM/PM 12h, responsive y accesibilidad.

**Non-Goals:** No cambiar idioma del `title`/`aria-label` (sigue español largo), no tocar hora 12h ni intervalo 1000ms, no añadir dependencias, no cambiar layout del navbar.

## Decisions

**Decisión 1: Array manual para `Sept` de 4 letras**
- *Por qué:* Ningún `Intl` produce `Sept` — `es-PE` da `set`, `en-US` da `Sep`, `es-ES` da `sept.`. Opción A pide `Sept` capitalizado. Array `['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']` + `pad(d.getDate())` garantiza `Sept 04` exacto, sin depender de locale del browser.
- *Alternativa descartada:* `toLocaleDateString('en-US', {month:'short', day:'2-digit'})` → daría `Sep 04` (3 letras), no cumple A. Regex post-proceso para insertar `t` es frágil.
- *Fallback:* mantener bloque `catch` con mismo array, coherente.

**Decisión 2: Unificar `line-height:1` + `align-self:center` + `display:block` en icono**
- *Por qué:* `align-items:center` en el contenedor no basta cuando los hijos tienen `font-size` y `font-weight` distintos; cada span necesita `line-height:1` y `align-self:center` para que su caja se centre ópticamente. Icono SVG/Canvas no es texto → `display:block` evita baseline gap de inline.
- *Alternativa descartada:* `align-items:baseline` → alinea baselines pero el icono (14px) queda arriba. `transform: translateY()` es mágico y frágil.
- *Implementación:* En `style.css:686` añadir a `.clock-badge` hijos: `line-height:1; vertical-align:middle;` y al `i/svg` 14px `display:block; flex-shrink:0; align-self:center;`. Quitar `py-2` asimétrico o balancearlo con `padding:0.35rem 0.75rem`.

**Decisión 3: Mantener `title`/`aria-label` en español largo**
- *Por qué:* La fecha corta es la única que cambia a inglés por pedido explícito; el tooltip completo sigue siendo comprensible para usuarios ES. Cambiar todo a inglés sería breaking del spec.
- *Alternativa descartada:* Traducir todo a `en-US` → pierde coherencia con resto del sistema en español.

## Risks / Trade-offs

- **Inconsistencia idioma badge vs tooltip (EN vs ES)** → Mitigación: documentado en spec; si molesta, futuro change unifica idioma.
- **Array hardcodeado vs i18n** → Mitigación: solo 12 strings, testeable; si se internacionaliza, migrar a `Intl` con mapping `Sep→Sept`.
- **Badge más ancho por `Sept` (4) vs `set` (3)** → Mitigación: sigue oculto en `<576px` (`d-none d-sm-inline`), ancho extra ~6px no rompe navbar.

## Migration Plan

Solo frontend. Cambios en 3 archivos. Rollback: revert commit. Verificación: abrir en 375px (solo hora) y 1024px (ver `Sept 04` centrado), inspeccionar `title` hover muestra español largo + hora PM.

## Open Questions

- Ninguna.
