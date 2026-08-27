## Purpose

Asegura que navegación, dashboard y layout respondan de forma coherente en móvil, tablet y escritorio, respetando safe-area, accesibilidad y preferencia de movimiento.

## ADDED Requirements

### Requirement: Navegación y sidebar responsive
El sidebar SHALL ser `244px` fijo con `transform` en desktop (`collapsed`/`expanded`) y overlay con `backdrop 1035` en <992px. En móvil SHALL abrirse por botón ☰ y por swipe desde el borde izquierdo (≥30px), y cerrarse por backdrop, swipe y `Esc`. El body SHALL usar `overscroll-behavior: contain` para evitar rebote detrás del overlay.

#### Scenario: Swipe abre sidebar en móvil
- **WHEN** se hace swipe desde el borde izquierdo en 360px con sidebar cerrado
- **THEN** el sidebar entra con `transform 180ms ease` y el `backdrop` aparece con `opacity 0→1`

#### Scenario: Sidebar no bloquea scroll del contenido en iOS
- **WHEN** el sidebar está abierto en iOS Safari y se hace scroll dentro de `main-content`
- **THEN** el scroll del body no rebota detrás del backdrop y `lockMainScroll` no deja el contenido congelado al cerrar

### Requirement: Dashboard y gráficos adaptados a móvil
En <768px `chart-frame` SHALL ser 240px (no 300px), solo el primer chart (Registros por mes) SHALL ser visible sin scroll, los demás SHALL hacer lazy render al entrar en viewport y mostrar `skeleton` mientras cargan. Los `stat-card` SHALL ser `col-6` en móvil con `min-height 84px` y `stat-icon 40px`, y `kpi-band` 104px.

#### Scenario: Dashboard en móvil prioriza contenido
- **WHEN** se abre `dashboard/index.html` en 360px
- **THEN** el primer paint muestra 5 `stat-card` en 2 columnas + 1 chart de 240px sin scroll horizontal, y el segundo chart solo renderiza tras `IntersectionObserver`

#### Scenario: Gráficos respetan dark mode y no desbordan
- **WHEN** se cambia de `light` a `dark` en móvil
- **THEN** los ejes y grid de Chart.js cambian a `var(--text-secondary)`/`var(--border-color)` sin recargar la página y el canvas nunca excede `100vw - 32px`

### Requirement: Breakpoints y layout fluido
El sistema SHALL usar breakpoints `576/768/992/1600` (Bootstrap) con `main-content` `max-width 1600px` centrado, `container-fluid.p-4` → `0.9rem` en <768px, y `page-header` en una sola línea con `status-pill` no caído. El layout SHALL usar `min-height: 100dvh` + `padding-bottom: calc(1.5rem + env(safe-area-inset-bottom))` en móvil.

#### Scenario: Page header no se rompe en móvil
- **WHEN** se renderiza cualquier `page-header` con `h4` + `status-pill` en 360px
- **THEN** ambos permanecen en la misma línea con `flex-wrap: nowrap` y el `status-pill` no cae debajo del título

#### Scenario: Safe-area respetada
- **WHEN** se abre cualquier vista en iPhone con notch en 390px
- **THEN** el último botón no queda bajo el home indicator y el `bottom` de `#toastContainer` y `.filter-drawer` usan `env(safe-area-inset-bottom)`

### Requirement: Accesibilidad y prefers-reduced-motion
Todo componente SHALL tener `focus-visible` (outline 2px + shadow) y respetar `@media (prefers-reduced-motion: reduce)` desactivando `transition`/`animation` a `0.01ms` y `scroll-behavior` a `auto`. Los toasts y drawers SHALL no animar si el usuario prefiere movimiento reducido.

#### Scenario: Usuario con movimiento reducido
- **WHEN** el sistema tiene `prefers-reduced-motion: reduce` y llega un toast
- **THEN** la isla aparece sin `mcToastIn`/`mcIslandOut`, solo `opacity` instantáneo y `progreso` sin animación

#### Scenario: Navegación por teclado
- **WHEN** se tabula por `navbar`, `sidebar` y `filter-drawer`
- **THEN** el foco siempre es visible con `outline: 2px solid var(--primary-color)` y el drawer atrapa foco hasta cerrar con `Esc`

### Requirement: Consistencia entre módulos y regla para futuros módulos
Cualquier módulo nuevo SHALL reutilizar `toast-island`, `table--cards`, `filter-drawer`, `form-section`, `confirm-sheet`, `empty-state`/`skeleton` y tokens existentes sin crear variantes ad-hoc. Un `make lint-design` o revisión visual SHALL fallar si se detecta `h5.text-*` semántico, `color: #` hardcodeado o `min-height: 34px` en móvil.

#### Scenario: Nuevo módulo respeta sistema
- **WHEN** se crea `app/modules/seguimiento/presentation` con una tabla y filtros
- **THEN** la tabla usa `data-responsive="cards"` y los filtros usan `filter-drawer` sin duplicar CSS, y una auditoría visual en 360/768/1024 muestra la misma experiencia que `consulta`

#### Scenario: Revisión detecta ad-hoc
- **WHEN** un PR añade `.custom-card { background: #f0f0f0; border-radius: 12px; }`
- **THEN** la revisión lo rechaza por usar hex y radius fuera de `var(--radius-*)` y `var(--surface-*)`
