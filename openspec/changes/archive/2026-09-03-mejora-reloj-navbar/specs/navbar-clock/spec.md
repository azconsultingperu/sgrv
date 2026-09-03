## Purpose

Hacer que el reloj del navbar sea inmediatamente comprensible y visualmente consistente con el design system, mostrando hora en 12h con AM/PM y fecha legible con iconografía, sin perder precisión ni accesibilidad.

## ADDED Requirements

### Requirement: Formato de hora en 12h con AM/PM y fecha legible

El badge `#relojNavbar` SHALL mostrar hora en formato 12h con segundos y sufijo `AM`/`PM` (ej. `02:05:22 PM`) y fecha en formato corto legible en español (ej. `03 sep 2026` o `mié, 03 sep 2026`). La fuente de tiempo SHALL ser la hora local del navegador (`new Date()`), actualizada cada 1000ms.

#### Scenario: Hora con AM/PM visible
- **WHEN** se carga cualquier página autenticada y el reloj se renderiza a las 14:05:22
- **THEN** el texto de hora muestra `02:05:22 PM` (no `14:05:22`)

#### Scenario: Medianoche y mediodía correctos
- **WHEN** son las 00:05 y las 12:05
- **THEN** se muestran `12:05:00 AM` y `12:05:00 PM` respectivamente

#### Scenario: Fecha legible en español
- **WHEN** la fecha es 2026-09-03
- **THEN** se muestra `03 sep 2026` o `mié, 03 sep` (mes abreviado en minúsculas, no `09/03/2026`)

#### Scenario: Actualización cada segundo
- **WHEN** el reloj lleva 5s visible
- **THEN** los segundos han avanzado 5 unidades sin recargar la página

### Requirement: Apariencia con iconos y jerarquía visual

El `.clock-badge` SHALL dejar de ser texto plano y pasar a layout `display:inline-flex; align-items:center; gap:0.4rem` con icono Lucide (`clock` de 14-16px) junto a la hora, hora en `font-weight:700` y fecha en `color:var(--text-muted)` y `font-size:0.78rem`, con `font-variant-numeric:tabular-nums` para que los dígitos no "brinquen". El badge SHALL mantener `border:1px solid var(--border-color)` y `background:var(--surface-2)` pero con `padding` y `border-radius` coherentes con otros badges del navbar.

#### Scenario: Icono visible
- **WHEN** se inspecciona `#relojNavbar` en desktop
- **THEN** existe un `<i data-lucide="clock">` (o svg) antes de la hora

#### Scenario: Jerarquía hora vs fecha
- **WHEN** se compara tipografía de hora y fecha
- **THEN** la hora es más grande/pesada que la fecha y la fecha usa `text-muted`

#### Scenario: Números estables
- **WHEN** los segundos pasan de `09` a `10`
- **THEN** el ancho del badge no vibra (tabular-nums)

### Requirement: Claridad y accesibilidad inmediata

El badge SHALL tener `title` y `aria-label` con formato completo y sin abreviaturas ambiguas (ej. `Miércoles, 03 de septiembre de 2026 — 02:05:22 PM (hora local)`). Al hacer hover SHALL mostrar `title` nativo del navegador.

#### Scenario: Hover muestra ayuda
- **WHEN** el usuario hace hover sobre el reloj
- **THEN** el tooltip del navegador muestra el texto completo con fecha larga y "hora local"

#### Scenario: Lector de pantalla
- **WHEN** un lector inspecciona `#relojNavbar`
- **THEN** `aria-label` contiene la fecha y hora completas

### Requirement: Responsive sin romper navbar

En viewport `<576px` el badge SHALL mostrar solo hora con AM/PM (oculta fecha con `d-none d-sm-inline` o media query) para no desbordar el navbar. La fecha completa SHALL permanecer accesible vía `title`/`aria-label`.

#### Scenario: Móvil solo hora
- **WHEN** se abre en 375px
- **THEN** se ve `02:05 PM` (o con segundos) pero no `03 sep 2026` dentro del badge

#### Scenario: Desktop hora + fecha
- **WHEN** se abre en 1024px
- **THEN** se ven hora y fecha separadas
