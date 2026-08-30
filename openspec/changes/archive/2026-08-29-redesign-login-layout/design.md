## Context

Ver `proposal.md - Why`. Estado actual en `app/templates/auth/login.html:16` usa `col-11 col-sm-9 col-md-6 col-lg-5` (~480–540px en desktop) y fila `.login-options` con `d-flex justify-content-between` que pone checkbox izquierda y link olvidó derecha en la misma fila. `app/static/css/auth.css:38` define `.login-card` sin `max-width` explícito, y `.login-options.mb-4` deja 1.5rem hasta el botón.

## Goals / Non-Goals

**Goals:**
- Tarjeta 400px centrada sin romper responsive 360px.
- Link olvidó como acción secundaria debajo del botón, centrado.
- Espaciado compacto checkbox→botón→link→footer.

**Non-Goals:**
- Cambiar `auth_controller`, validación, `name/id`, CSRF o rutas.
- Rediseño del fondo `frontis` ni tipografía base.
- Nueva dependencia.

## Decisions

### 1. Ancho 400px vía `max-width` en `.login-card` + wrapper centrado
- **Decisión:** Añadir `.login-card { max-width: 400px; margin-left: auto; margin-right: auto; width: 100%; }` y reducir contenedor de `col-lg-5` a `col-lg-4` o mantener `col-*` pero capar con `max-width` para no pelear con grid. `p-4 p-md-5` se mantiene; inputs conservan `padding 0.7rem 0.85rem`.
- **Rationale:** `max-width` + `auto` centra sin tocar grid responsive; 400px deja ~24px de padding lateral interno sin aire muerto. `col-lg-4` solo sería 33% del row, demasiado estrecho en 992px; capar es más predecible.
- **Alternativa:** Cambiar solo `col-*` a `col-md-5 col-lg-4` — rechazada: en 768px sigue ancho y depende de breakpoint, no de contenido.

### 2. Reestructurar fila: checkbox solo + link debajo del botón
- **Decisión:** En `login.html:44` reemplazar `d-flex login-options` de dos elementos por `<div class="login-options mb-3"><div class="form-check">...</div></div>` solo con checkbox alineado `justify-content-start` (izquierda). Debajo del `<button>` insertar `<div class="text-center mt-2"><a class="login-link login-link--secondary" ...>¿Olvidó su contraseña?</a></div>` con clase `login-link--secondary` para variante.
- **Rationale:** Separar acción primaria (botón) de secundaria (link) mejora jerarquía; centrado debajo del botón sigue patrón común de auth y no compite con checkbox.
- **Alternativa:** Checkbox centrado — rechazada: rompe alineación con inputs que son left-aligned; izquierda se ve más equilibrado con campo de texto arriba.

### 3. Variante de link secundario y espaciado
- **Decisión:** `auth.css:190` añadir `.login-link--secondary { font-size: 0.85rem; }` (ya hay `@media` que pone `login-link` 0.85rem en móvil, se unifica a 0.85rem en desktop también para secundario), `text-decoration: none` en reposo, `hover` subraya. Márgenes: `.login-options { margin-bottom: 0.75rem !important; }` (~12px), `.login-btn { margin-bottom: 0; }`, link olvidó `margin-top: 10px`, `.auth-motto { margin-top: 0.9rem; }` (en vez de `mt-3` 1rem). En `@media (max-width:575.98px)` mantener `row-gap` pero ya no aplica porque checkbox está solo.
- **Rationale:** Reduce salto checkbox→botón de 24px a 12px y botón→link a 10px, deja 14–15px hacia footer, conjunto compacto sin apretar.
- **Alternativa:** Usar `gap` flex en form — rechazada: requiere reestructurar todo el form a flex column, más riesgo.

## Risks / Trade-offs

- **Tarjeta 400px puede verse estrecha en desktop grande** → Mitigación: 400px es estándar auth (380–420 pedido); en ≥1400px el fondo `frontis` sigue visible a los lados, no se ve vacío.
- **Link centrado debajo del botón puede perderse si usuario espera a la derecha** → Mitigación: color primario + tamaño secundario pero centrado es patrón esperado; se mantiene `hover` subrayado para affordance.
- **Reducir `mb-4` a `mb-3` afecta solo login, no otros `login-options`** → Mitigación: scope a `.login-options` dentro de `#loginForm` o añadir modificador `.login-options--compact`.

## Migration Plan

1. Editar `login.html` (estructura) y `auth.css` (ancho + márgenes + variante link).
2. Verificar en 360/768/1024/1400: tarjeta ≤420px centrada, orden checkbox→botón→link→footer, hover del link, y submit sigue a `auth.login`.
3. `make lint-boundaries` y `pytest tests/test_auth.py -q` verdes (no lógica tocada).
4. Rollback: revertir `max-width` y re-colocar link en `login-options` flex (un commit).

## Open Questions

- ¿Checkbox "Recordar usuario" debe quedar alineado a la izquierda o centrado cuando queda solo? Default: izquierda (alineado con inputs).
