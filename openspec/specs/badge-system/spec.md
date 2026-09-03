# badge-system Specification

## Purpose
Define la paleta de badges/etiquetas de estado/rol reutilizable para cualquier etiqueta futura (éxito, error, advertencia, información) con contraste WCAG AA y variantes por tema que preserven identidad de marca.

## Requirements

### Requirement: Contraste WCAG AA de badges actuales auditado

El sistema SHALL auditar el contraste de cada badge actual (texto blanco #ffffff sobre fondo del badge) en ambos temas contra WCAG AA 4.5:1 y SHALL documentar fallos.

#### Scenario: Auditoría en modo claro
- **WHEN** se calcula contraste blanco vs fondo en `:root`
- **THEN** `success #16803c` 5.02 PASS, `danger #c2413a` 5.11 PASS, `warning #b7791f` 3.64 FAIL, `info #0f7490` 5.36 PASS, `primary #2563eb` 5.17 PASS, `secondary #64748b` 4.76 PASS — solo warning falla.

#### Scenario: Auditoría en modo oscuro
- **WHEN** se calcula contraste blanco vs fondo en `[data-bs-theme="dark"]`
- **THEN** `success #4ade80` 1.74 FAIL, `danger #f87171` 2.77 FAIL, `warning #fbbf24` 1.67 FAIL, `info #38bdf8` 2.14 FAIL, `primary #60a5fa` 2.54 FAIL, `secondary #a8b3c2` 2.12 FAIL — todos fallan; el verde de "Activo" (#4ade80) es el peor caso y se ve apagado sobre `var(--surface-1)` #161d27.

#### Scenario: Identificación del peor caso
- **WHEN** se prioriza el fix
- **THEN** el badge `Activo` (success en dark) se marca como peor caso por contraste 1.74 y percepción apagada.

### Requirement: Paleta de estado con variables por tema

El sistema SHALL definir variables CSS dedicadas `--badge-success-bg`, `--badge-success-text`, `--badge-danger-bg`, `--badge-danger-text`, `--badge-warning-bg`, `--badge-warning-text`, `--badge-info-bg`, `--badge-info-text`, `--badge-primary-bg`, `--badge-secondary-bg` (y texto) en `:root` y `[data-bs-theme="dark"]`, reutilizables para cualquier badge/etiqueta futura, manteniendo identidad de marca pero con valores por tema que cumplan contraste.

#### Scenario: Variables en modo claro
- **WHEN** el tema es claro
- **THEN** `:root` define `success-bg #15803c` (o #16803c), `danger-bg #c2413a`, `warning-bg #b45309` (corrige #b7791f), `info-bg #0f7490`, `primary-bg #2563eb`, `secondary-bg #475569` (o #64748b) con texto `#ffffff` y todos ≥4.5:1 vs blanco.

#### Scenario: Variables en modo oscuro
- **WHEN** el tema es oscuro
- **THEN** `[data-bs-theme="dark"]` define las mismas o variantes ligeramente más oscuras pero aún con ≥4.5:1 vs blanco (ej. `success-bg #15803c` o #166534 7.13, `danger-bg #dc2626` 4.83 o #b91c1c, `warning-bg #b45309` 5.02, `info-bg #0369a1` ~6.5, `primary-bg #2563eb` 5.17, `secondary-bg #334155` 8.0) — no los pastel actuales.

#### Scenario: Reutilización futura
- **WHEN** se crea un nuevo badge con `class="badge bg-success"` u otro estado
- **THEN** consume `var(--badge-success-bg)` y `var(--badge-success-text)` sin hardcodear hex.

### Requirement: Consistencia y colisión con toasts

El rojo de badges (`Administrador`/`danger`) SHALL compartir tono con el rojo de toasts sólidos (`fix-toast-solid-background`) por consistencia de estado, pero SHALL diferenciarse visualmente por contexto (badge inline en tabla vs toast flotante con icono y sombra) para no generar confusión cuando coincidan en pantalla.

#### Scenario: Coexistencia badge y toast
- **WHEN** un toast de error (`background: var(--danger-color)`) aparece sobre una tabla con badge `Administrador` (`background: var(--badge-danger-bg)`)
- **THEN** ambos comparten familia roja pero son distinguibles por posición/forma/sombra; si se percibe confusión, el diseño MAY ajustar matiz (ej. badge `#b91c1c` vs toast `#dc2626`) manteniendo contraste.

#### Scenario: Verificación de paleta propuesta
- **WHEN** se presenta la paleta con hex exactos para claro y oscuro
- **THEN** cada par fondo/texto tiene contraste ≥4.5:1 vs blanco y vs fondo de tabla (`#ffffff` en claro, `#161d27` en oscuro) y se muestra en tabla para revisión antes de aplicar.

### Requirement: Aplicación en tablas del sistema

Los badges en `Gestión de Usuarios` (`Activo`/`Inactivo`, `Administrador`/`Supervisor`/`Operador`) y otras tablas SHALL usar las nuevas variables `--badge-*` en vez de `var(--success-color)` directo, manteniendo `color:#ffffff` y `border-radius:var(--radius-full)`.

#### Scenario: Badge Activo en oscuro
- **WHEN** se ve `Activo` en modo oscuro
- **THEN** su fondo es `#15803c` o `#166534` (no `#4ade80`) y el blanco contrasta ≥4.5:1, percibiéndose saturado y no apagado.

#### Scenario: Badge Supervisor en claro
- **WHEN** se ve `Supervisor` (warning) en modo claro
- **THEN** su fondo es `#b45309` (no `#b7791f`) y pasa 5.02 vs blanco.
