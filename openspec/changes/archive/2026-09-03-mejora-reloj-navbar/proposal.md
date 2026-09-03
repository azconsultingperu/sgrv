## Why

El reloj del navbar (`#relojNavbar` junto al botón de tema) hoy muestra `03/09/2026 14:05:22` como texto plano en un `badge` genérico. Es visualmente básico, no deja claro a primera vista qué es hora y qué es fecha, y el formato 24h sin AM/PM es menos legible para usuarios no técnicos. Mejorar su apariencia aumenta claridad y profesionalismo sin tocar lógica de negocio.

## What Changes

- **Formato legible AM/PM:** Cambia `HH:MM:SS 24h` a `hh:mm:ss AM/PM` (ej. `02:05:22 PM`) y fecha a `03 sep 2026` o `mié, 03 sep` con capitalización, separando hora y fecha visualmente. Mantiene zona horaria local del navegador.
- **Diseño con iconos y jerarquía:** El badge pasa de texto plano a layout con `i[data-lucide="clock"]` para hora y `calendar` para fecha (o uno solo con separador), hora en `font-weight:700` y fecha en `text-muted` más pequeña, gap y padding refinados. No usa monospace genérico; usa `var(--font-sans)` con `tabular-nums` para números estables.
- **Claridad inmediata:** Añade `title`/`aria-label` con formato completo para accesibilidad y `tooltip` nativo al hover ("Hora local de tu dispositivo").
- **Responsive:** En móvil (`<576px`) muestra solo hora con AM/PM y oculta fecha para no romper el navbar; la fecha completa queda en `title`.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `navbar-clock`: Indicador de hora/fecha en el navbar con formato y apariencia mejorados.

## Impact

- `app/templates/partials/navbar.html` — estructura del badge con iconos y spans separados para hora/fecha/AMPM.
- `app/static/css/style.css` — `.clock-badge` con nueva tipografía, layout flex, tamaños y estado hover.
- `app/static/js/main.js` — `actualizarReloj()` con formato 12h, AM/PM y fecha legible.
- Sin cambios en backend, sin migración, sin dependencia nueva.
