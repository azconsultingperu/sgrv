## Why

SGRV tiene una base visual sólida (tokens, Inter, dark mode) pero cada módulo inventa jerarquía, colores y patrones móviles ad-hoc. En móvil las tablas requieren scroll horizontal oculto, los filtros apilan 6 inputs, los touch targets son de 28-34px y las notificaciones usan una animación lateral no adaptada. Sin reglas compartidas, cada módulo nuevo replica la inconsistencia.

## What Changes

- **Endurecer sistema visual sin redesign:** Mantener tokens, tipografía Inter, paleta y radius actuales; definir reglas de uso funcional para jerarquía, color, espaciado y tamaños.
- **Toast-island móvil (dirección B):** Isla superior compacta, centrada, con animación física suave (Y+scale, spring), gesto swipe-to-dismiss, pausa por touch, haptic y safe-area. Reemplaza la animación lateral actual en `es-movil`.
- **Tablas responsive:** Nuevo patrón `table--cards` — en desktop tabla, en móvil cards apiladas con la misma data, sin duplicar markup.
- **Filter drawer / bottom sheet:** En móvil los filtros de consulta/auditoría colapsan a un botón `Filtros (n)` que abre drawer con `Aplicar/Cancelar`.
- **Form sections:** Formularios largos (registro/editar) en móvil se agrupan en acordeones de sección con un solo bloque abierto.
- **Confirm sheet:** El modal `data-confirm` en móvil pasa a bottom sheet con handle, swipe-down y haptic.
- **Touch & a11y:** Todo interactivo ≥44px en <768px, foco visible, `prefers-reduced-motion` respetado.
- **Responsive coherente:** Sidebar swipe-from-edge, navbar, dashboard/charts (lazy + skeleton, 240px en móvil), safe-area `env()` y `100dvh` correcto.
- **Estados globales:** Patrones únicos para vacío (`empty-state`), carga (skeleton pulse), error (`alert` + reintento) y éxito (toast-island).

## Capabilities

### New Capabilities
- `design-tokens`: Jerarquía visual unificada, tipografía, paleta de uso funcional, espaciado y tamaños consistentes.
- `ui-components`: Componentes reutilizables — botones/estados, tablas-cards, filter-drawer, form-sections, confirm-sheet, toast-island, estados globales y touch targets.
- `responsive-layout`: Navegación/sidebar, dashboard y gráficos, responsive breakpoints, safe-area y accesibilidad móvil/tablet/escritorio.

### Modified Capabilities
- _Ninguna_ — es un sistema nuevo aditivo sobre UI existente; los specs previos (`modular-boundaries`, `domain-events`) no cambian.

## Impact

- **Código afectado:** `app/static/css/style.css`, `app/static/css/auth.css`, `app/static/js/main.js`, `app/templates/base.html`, `app/templates/partials/navbar.html`, `app/templates/partials/sidebar.html`, `app/templates/dashboard/index.html`, `app/templates/consulta/index.html`, `app/templates/registro/index.html`, `app/templates/registro/editar.html`, `app/templates/usuarios/index.html`, `app/templates/auditoria/index.html`, `app/templates/reportes/index.html`, `app/templates/partials/paginacion.html` y futuros módulos. Sin cambios en `app/shared`, `app/modules/*/domain` ni lógica de negocio.
- **Dependencias:** Ninguna nueva (CSS/JS vanilla + Bootstrap 5.3 + Chart.js existentes).
- **Sistemas:** Build/test sin cambios; validación visual manual en 360px, 768px, 1024px y con `prefers-reduced-motion`.
