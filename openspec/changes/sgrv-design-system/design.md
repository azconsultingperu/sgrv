## Context

SGRV ya tiene un design system base sólido: tokens CSS (`--primary`, `--sidebar-bg`, `--radius`, `--space`, `--control-height`), tipografía Inter, dark/light con `data-bs-theme`, y componentes como `mc-toast`, `confirm-modal`, `sidebar` con `transform`. Ver `proposal.md - Why`. La deuda está en el uso inconsistente de esos tokens por pantalla (h5 con 4 colores, tablas solo con scroll horizontal, filtros apilados, touch targets 28-34px, toast con `translateX` en móvil, `100dvh` sin `safe-area`). Bootstrap 5.3 + Chart.js + Jinja2 son constraints: no React, no nueva dependencia.

## Goals / Non-Goals

**Goals:**
- Endurecer reglas de uso de tokens existentes sin cambiar paleta/tipografía base, salvo subir `sm` a 36px en móvil.
- Proveer 7 componentes reutilizables que cualquier módulo futuro importe sin CSS ad-hoc: `toast-island`, `table--cards`, `filter-drawer`, `form-section`, `confirm-sheet`, `empty/skeleton/error`.
- Unificar responsive en 3 breakpoints reales (360, 768, 1024) con safe-area y `prefers-reduced-motion`.

**Non-Goals:**
- Redesign visual completo (no cambian colores base, no nueva tipografía, no ilustraciones).
- Cambiar lógica de negocio, `app/shared`, `app/modules/*/domain` ni añadir dependencias JS.
- Reescribir `auth.css` más allá de alinearlo a tokens (se mantiene `login-bg` con frontis).

## Decisions

### 1. Evolución, no revolución (sobre fork de CSS)
- **Decisión:** Reutilizar `style.css:19-121` tokens y `main.js` como base; añadir variantes `is-movil` y `data-responsive` en vez de crear `mobile.css` separado.
- **Rationale:** Evita duplicar 1960 líneas y mantiene dark mode existente. Un solo `style.css` con media queries es más fácil de auditar que dos sistemas.
- **Alternativa:** `mobile-first.css` separado → rechazada: duplica mantenimiento y rompe `?v=42` cache busting actual.

### 2. Toast-island B con CSS + Web Animations API ligera (sobre librería)
- **Decisión:** En `es-movil`, `#toastContainer` pasa a `position:fixed; top:calc(env(safe-area-inset-top,0)+12px); left:50%; transform:translateX(-50%)`; anim entrada `translateY(-20px) scale(.96)→0/1` 0.32s `cubic-bezier(.16,1,.3,1)`, salida `translateY+opacity`. Gesto `touchstart` pausa + `swipe` horizontal con `touchmove` + `velocity` + `navigator.vibrate(10)`. Mantener cola MAX 3 y `z-index` por debajo de sidebar cuando `sidebar-open`.
- **Rationale:** Sin dependencia, usa `env()` y `100dvh` ya presentes (`base.html:5`). Spring físico sin copiar iOS literal (escala .96, no blur).
- **Alternativa:** `sonner` o `notistack` → rechazada: añade React/port y no respeta `mostrarToast` actual (`main.js:377`).

### 3. Tablas → Cards vía CSS Container Queries + `data-label` (sobre duplicar markup)
- **Decisión:** Añadir `data-responsive="cards"` a `table` y en `<768px` aplicar `thead{display:none}` + `tr{display:block; border; radius}` + `td{display:flex; justify-content:space-between}` con `td::before{content:attr(data-label)}` generado desde `th` vía JS al hydrate. Sin duplicar HTML en Jinja.
- **Rationale:** Un solo markup, progresivo, accesible (lector ve `th` en desktop, `data-label` en móvil). Evita mantener dos templates.
- **Alternativa:** Dos plantillas (`table` vs `cards`) con `d-none d-md-block` → rechazada: duplica lógica de paginación y `empty-state`.

### 4. Filter drawer como `confirm-overlay` reutilizado (sobre offcanvas Bootstrap)
- **Decisión:** Reusar `.confirm-overlay` (style.css:1625) como base para `.filter-drawer` bottom sheet (`max-height:80dvh`, `overflow-y:auto`, `backdrop` 1035). En <768px el `form` de filtros se teleporta al drawer vía `appendChild`; en desktop permanece inline.
- **Rationale:** Ya tienes `z-index` y `backdrop` probados; evita `offcanvas` de Bootstrap que trae `body scroll lock` conflictivo con tu `lockMainScroll`.
- **Alternativa:** Bootstrap offcanvas → rechazada: requiere `data-bs-*` y rompe tu `sidebar` custom.

### 5. Form sections como `<details>`-like acordeón (sobre wizard)
- **Decisión:** Envolver cada `h5.section-title` + `row` en `section.form-section` con `aria-expanded` y `max-height` animado. En desktop `max-height:none` (siempre abierto); en móvil solo el primero `open`.
- **Rationale:** Preserva `novalidate` y validación existente (`registro/index.html:197`), solo añade agrupación. Wizard con pasos añadiría state y rompería `flash`.
- **Alternativa:** Stepper multi-paso → rechazada: más código JS y cambia flujo de `POST` actual.

### 6. Touch targets 44px vía `min-height` y `min-width` (sobre padding hack)
- **Decisión:** Subir `--control-height-sm` de 34px a 36px y en `@media (max-width:767.98px)` forzar `pagination .page-link`, `btn-group-sm`, `navbar .dropdown-toggle` a `min-height:44px`/`min-width:44px`. No cambiar `btn` base 42px en desktop (evita reflow).
- **Rationale:** WCAG 2.5.5 exige 44px; 36px es compromiso para densidad, pero 44px en móvil es obligatorio.
- **Alternativa:** Cambiar todo a 44px global → rechazada: hace desktop demasiado grande.

## Risks / Trade-offs

- **Toast isla tapa navbar sticky** → Mitigación: cuando `body.es-movil`, `top: calc(env(safe-area-inset-top) + 64px)` si `navbar` es sticky, o bajar `z-index` de isla a 1020 (< navbar 1025) para que quede debajo. Validar en iOS con notch.
- **Cards duplican lógica de `data-label`** → Mitigación: generar `data-label` automáticamente desde `th` al DOMContentLoaded, no manual en Jinja, para que futuros módulos no olviden el atributo.
- **Drawer teleport rompe `GET` con `search_params`** → Mitigación: el `form` teleportado mantiene `method="GET"` y `action` original; `Aplicar` hace `form.requestSubmit()` para preservar `pagination`.
- **Sidebar swipe colisiona con swipe de toast** → Mitigación: toast swipe solo horizontal con `threshold 60px` y `swipe` del sidebar solo desde `touchstart` en `0-30px` del borde izquierdo.

## Migration Plan

1. **Fase 0 - Tokens y lint visual:** Añadir `stylelint` rule o `make lint-design` que falle si encuentra `h5.text-*` semántico, `color: #` hardcodeado fuera de `auth.css`, o `min-height:34px` en móvil. No cambia UI.
2. **Fase 1 - Isla B:** Migrar `main.js:351-519` y `style.css:1474-1623` a isla superior en `es-movil`, con `env(safe-area)` y `prefers-reduced-motion`. Validar en 360px + `prefers-reduced-motion`.
3. **Fase 2 - Tablas y filtros:** Añadir `table--cards` y `filter-drawer` a `consulta` y `auditoria` primero (menor riesgo), luego `usuarios`/`reportes`.
4. **Fase 3 - Forms y confirm:** Envolver `registro`/`editar` en `form-section` y migrar `confirm-modal` a `confirm-sheet` en móvil.
5. **Fase 4 - Dashboard/sidebar/polish:** Ajustar `chart-frame` a 240px móvil + lazy, sidebar swipe, touch targets 44px, y auditar 3 breakpoints con `pytest` visual manual.
6. **Rollback:** Cada fase es CSS/JS aislado detrás de `body.es-movil` o `data-responsive`; revertir es quitar clase/variante sin tocar templates de desktop.

## Open Questions

- ¿El `filter-drawer` debe recordar el último estado (abierto/cerrado) en `localStorage` o siempre cerrado al entrar? Default propuesto: siempre cerrado.
- ¿El `toast-island` debe soportar acción (botón Deshacer/Ver) en esta v1 o solo título+descripción? Default: solo título+descripción; acción queda para v1.1 sin cambiar spec.
