## Why

Los gráficos de barras verticales del dashboard (Alumnos por Colegio y Alumnos por Distrito) se ven poco profesionales: barras demasiado anchas sin aire entre categorías y tooltip de Chart.js pegado sobre la barra tapando el dato en vez de flotar con caret visible. Mejorar la densidad y el tooltip eleva la legibilidad sin tocar datos.

## What Changes

- Ajustar configuración visual de Chart.js en `app/templates/dashboard/index.html` para `chartColegios` y `chartDistritos`:
  - `datasets[].barPercentage: 0.5–0.6` y `categoryPercentage: 0.6–0.7` para barras más delgadas y espaciadas.
  - `options.plugins.tooltip` explícito con `enabled: true`, `position: 'nearest'`, `yAlign: 'bottom'`, `caretSize: 6–8`, `caretPadding: 8–10`, `padding: 8–10`, `cornerRadius: 6–8`, sombra y separación visual (burbuja flotante).
  - Asegurar `scales.y.suggestedMax` con margen + `layout.padding.top` o `padding-top` del contenedor `chart-frame` para que el tooltip no se corte en el borde superior cuando la barra está cerca del máximo.
- Aplicar el mismo ajuste a ambos gráficos para consistencia.
- No cambia lógica de datos, queries ni endpoints (`dashboard_get_alumnos_por_colegio/distrito`).

## Capabilities

### New Capabilities
- `dashboard-barcharts`: Configuración visual de barras y tooltip flotante para los gráficos de barras del dashboard (ancho/espaciado y burbuja con caret).

### Modified Capabilities
- _Ninguna_ — cambio puramente visual, no altera specs de dominio existentes (`domain-events`, `modular-boundaries`, `notifications`).

## Impact

- **Código afectado:** `app/templates/dashboard/index.html` bloque `<script>` (inicialización `new Chart(...)` para `chartColegios` y `chartDistritos`); opcional `app/static/css/style.css` si se requiere `padding-top` en `.chart-frame`.
- **Dependencias:** Chart.js existente (sin nueva lib).
- **Riesgo:** Bajo, solo config visual; sin impacto en BD, API o permisos.
