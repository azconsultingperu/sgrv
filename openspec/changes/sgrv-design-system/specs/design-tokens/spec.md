## Purpose

Define y endurece los tokens y reglas visuales de SGRV para que cualquier módulo mantenga jerarquía, color y espaciado coherentes sin soluciones ad-hoc.

## ADDED Requirements

### Requirement: Jerarquía visual unificada
El sistema SHALL usar tres niveles únicos: Page Title (h4 1.22rem Bold + icono primary), Section Title (h5 1rem Bold con border-bottom e icono) y Card Title (h6 0.94rem Semibold). La Section Title SHALL ser siempre `color: var(--text-primary)`; el color semántico (success/warning/info) SHALL aparecer solo en el icono, nunca en el texto.

#### Scenario: Registro usa jerarquía correcta
- **WHEN** se renderiza `registro/index.html` con secciones Datos Personales, Contacto, Colegio
- **THEN** cada `h5` es `text-primary` con `border-bottom` y solo el `i` lleva `text-success`/`text-warning`, y un validador visual no encuentra `h5.text-success` en el DOM

#### Scenario: Nuevo módulo respeta niveles
- **WHEN** un futuro módulo añade una sección con `h5`
- **THEN** el linter visual reporta error si usa `h5.text-info` o `h5.text-warning` directo

### Requirement: Tipografía Inter sin variantes ad-hoc
El sistema SHALL usar exclusivamente `font-family: var(--font-sans)` (Inter) y tamaños `base 0.94rem`, `sm 0.86rem`, `xs 0.78rem`. Cualquier texto SHALL usar `var(--text-primary)` / `secondary` / `muted`; los hex directos (`#172033`) SHALL estar prohibidos fuera de `auth.css` legacy.

#### Scenario: Texto no usa hex directo
- **WHEN** se inspecciona cualquier template fuera de `auth/` en desktop y móvil
- **THEN** no existe `color: #` hardcodeado en los nodos de texto y `getComputedStyle` devuelve un valor de `var(--text-*)`

#### Scenario: Tamaño permitido
- **WHEN** un componente define `font-size: 0.82rem` fuera de la escala
- **THEN** el sistema de revisión lo marca como violación de tokens

### Requirement: Paleta de uso funcional
Primary SHALL usarse solo para acción/foco/activo; Success/Info/Warning/Danger SHALL usarse solo para estado (badge, progreso, toast, alert), nunca para decorar secciones o iconos de sección sin estado. El sidebar SHALL permanecer `var(--sidebar-bg) #111827` en light y ` #0b111c` en dark.

#### Scenario: Dashboard no abusa de colores
- **WHEN** se renderiza `dashboard/index.html`
- **THEN** los `stat-card` no usan `stat-icon-warning` sin que haya estado warning real, y los `h5` de sección no tienen `text-*` semántico

#### Scenario: Estado usa color correcto
- **WHEN** se muestra un toast `error` o un `badge bg-danger`
- **THEN** el color es `var(--danger-color)` y en dark mode cambia a `var(--danger-color)` oscuro sin hex fijo

### Requirement: Espaciado y tamaños consistentes
El sistema SHALL usar ritmo `--space-6` (1.5rem) entre secciones, `g-3` dentro de secciones, `p-4` desktop / `p-3` móvil para `card-body`, y alturas de control 44px base (42px legacy permitido solo en desktop) y 36px para `sm` en móvil. Un control interactivo SHALL respetar esos mínimos.

#### Scenario: Card respeta padding responsive
- **WHEN** se abre cualquier `card-body.p-4` en 360px y 1024px
- **THEN** en 360px el padding computado es 1rem (16px) y en 102티브 el padding es 1.5rem, sin `padding` hardcodeado en el template

#### Scenario: Control no es demasiado pequeño en móvil
- **WHEN** se inspecciona un `form-control-sm` en 360px
- **THEN** su altura es ≥36px y nunca 34px
