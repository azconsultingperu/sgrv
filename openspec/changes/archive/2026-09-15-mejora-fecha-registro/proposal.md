## Why

El `input type="date"` nativo despliega un calendario del sistema (popup del SO/navegador) inconsistente entre dispositivos, con mala ergonomía en desktop (navegación lenta año por año) y móvil (tap targets pequeños). En SGRV se usa en `fecha_nacimiento` y `fecha_visita` (registro/editar) y en filtros de auditoría/consulta, y el usuario reporta que la ventana desplegable no es agradable ni eficiente para ingresar fechas de 2007-2010 (nacimiento) o fecha actual.

## What Changes

- Reemplazar `type="date"` nativo en `registro/index.html` y `registro/editar.html` por una alternativa con mejor UX, sin romper validación, envío `YYYY-MM-DD` al backend, ni persistencia tras error.
- Evaluar y elegir 1 alternativa principal entre:
  - **A) Máscara DD/MM/YYYY** con `input type="text"` + `inputmode=numeric` + validación JS (ej. `15/03/2008` → `2008-03-15`).
  - **B) 3 selects segmentados** Día/Mes/Año (accesible, sin popup).
  - **C) Calendario ligero custom** (ej. flatpickr/litepicker vanilla, ~5-10KB) con navegación rápida por año y teclado.
  - **D) Híbrido**: máscara + botón calendario opcional (mejor de A y C).
- **Decisión recomendada**: **D Híbrido** — input texto enmascarado `DD / MM / AAAA` con separadores automáticos + botón pequeño Lucide `calendar` que abre calendario ligero solo si el usuario lo desea. Cubre escritura rápida (power users) y selección visual sin imponer popup.
- Mantener `fecha_visita` y `fecha_nacimiento` enviando `YYYY-MM-DD` (hidden o conversión JS) para no tocar `registro_controller` / `registro_service`.
- Extender el patrón a `auditoria/index.html` (`fecha_desde`/`fecha_hasta`) si se adopta calendario ligero, con consistencia visual.
- Preservar: `required`, `is-invalid`, edad calculada, auto-llenado `fecha_actual`, y rehidratación tras error (`form.fecha_*`).

## Capabilities

### New Capabilities
- `registro-fecha-input`: Componente de entrada de fecha para el módulo registro (máscara + calendario opcional), desacoplado del nativo.

### Modified Capabilities
- `registro-form`: Requisitos de inputs de fecha en `registro/index.html` y `registro/editar.html` (antes `type="date"`, ahora componente híbrido; validación y formato cambian).
- `consulta-listado` (si aplica) y `auditoria` filtros de fecha: si se unifica, actualizar spec de filtros; de lo contrario dejar fuera de alcance inicial.

## Impact

- **Templates**: `app/templates/registro/index.html`, `app/templates/registro/editar.html` (y opcional `auditoria/index.html`, `consulta/index.html`).
- **Static**: nuevo `app/static/js/fecha-input.js` (máscara + flatpickr/litepicker si se elige), `app/static/css/fecha-input.css` (opcional), `lucide` icon.
- **JS existente**: `calcularEdad`, auto `fecha_visita`/`hora` y rehidratación deben escuchar el nuevo input.
- **Backend**: sin cambios si se envía `YYYY-MM-DD`; solo validación de formato si se acepta `DD/MM/YYYY`.
- **Dependencias**: si se elige calendario ligero, añadir librería vanilla sin jQuery (flatpickr 4.x o equivalente) vía CDN o vendor.
- **Compatibilidad**: sin breaking change en API; degradación a `type="text"` con placeholder `DD/MM/AAAA`.
