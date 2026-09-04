## MODIFIED Requirements

### Requirement: Formato de hora en 12h con AM/PM y fecha legible

El badge `#relojNavbar` SHALL mostrar hora en formato 12h con segundos y sufijo `AM`/`PM` (ej. `02:05:22 PM`) y fecha en formato corto `Sept 04` (mes abreviado inglés de 4 letras para septiembre como `Sept`, resto 3 letras — `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sept`, `Oct`, `Nov`, `Dec` — seguido de día a 2 dígitos). El badge SHALL mostrar solo `Sept 04` sin año; el año SHALL permanecer solo en `title`/`aria-label`. La fuente de tiempo SHALL ser la hora local del navegador (`new Date()`), actualizada cada 1000ms.

#### Scenario: Hora con AM/PM visible
- **WHEN** se carga cualquier página autenticada y el reloj se renderiza a las 14:05:22
- **THEN** el texto de hora muestra `02:05:22 PM` (no `14:05:22`)

#### Scenario: Medianoche y mediodía correctos
- **WHEN** son las 00:05 y las 12:05
- **THEN** se muestran `12:05:00 AM` y `12:05:00 PM` respectivamente

#### Scenario: Fecha en formato Sept 04 (opción A)
- **WHEN** la fecha es 2026-09-04
- **THEN** el badge muestra `Sept 04` (no `04 set`, no `Sep 04`, no `04/09/2026`)

#### Scenario: Otros meses abreviados
- **WHEN** la fecha es 2026-01-09 o 2026-12-25
- **THEN** se muestra `Jan 09` o `Dec 25` respectivamente

#### Scenario: Actualización cada segundo
- **WHEN** el reloj lleva 5s visible
- **THEN** los segundos han avanzado 5 unidades sin recargar la página

### Requirement: Apariencia con iconos y jerarquía visual

El `.clock-badge` SHALL usar `display:inline-flex; align-items:center;` con icono Lucide `clock` de 14px con `display:block; flex-shrink:0; align-self:center;` y cada span interno (`#relojHora`, `#relojAmPm`, `#relojFecha`) SHALL tener `line-height:1; align-self:center;` para centrado vertical óptico perfecto respecto al icono. Hora en `font-weight:700`, fecha en `color:var(--text-muted)` y `font-size:0.74rem`, con `font-variant-numeric:tabular-nums`. El badge SHALL mantener `border:1px solid var(--border-color)` y `background:var(--surface-2)` con padding vertical simétrico.

#### Scenario: Icono visible y centrado
- **WHEN** se inspecciona `#relojNavbar` en desktop
- **THEN** existe un `<i data-lucide="clock">` (o svg) de 14px antes de la hora y su centro vertical coincide con el de la hora/fecha (misma línea media, no baseline desfasada)

#### Scenario: Jerarquía hora vs fecha
- **WHEN** se compara tipografía de hora y fecha
- **THEN** la hora es más grande/pesada que la fecha y la fecha usa `text-muted`

#### Scenario: Números estables
- **WHEN** los segundos pasan de `09` a `10`
- **THEN** el ancho del badge no vibra (tabular-nums)

#### Scenario: Centrado no vibra al cambiar AM/PM
- **WHEN** la hora pasa de `11:59:59 AM` a `12:00:00 PM`
- **THEN** el icono permanece verticalmente centrado sin salto
