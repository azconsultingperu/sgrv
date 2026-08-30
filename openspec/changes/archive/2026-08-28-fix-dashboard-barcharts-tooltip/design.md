## Context

Ver `proposal.md - Why`. Estado actual en `app/templates/dashboard/index.html:306` y `318`: `chartColegios` y `chartDistritos` se crean con `type: 'bar'` sin `barPercentage`/`categoryPercentage` ni `plugins.tooltip` explícito; usan solo `backgroundColor` y escalas básicas. El tooltip nativo queda pegado sobre la barra y las barras ocupan casi todo el ancho de categoría. Constraint: Chart.js 4.x ya cargado, sin nueva dependencia; datos vienen de `dashboard_get_alumnos_por_colegio/distrito` (no tocar).

## Goals / Non-Goals

**Goals:**
- Barras más delgadas con aire entre columnas en ambos gráficos.
- Tooltip burbuja flotante con caret visible, separado de la barra, consistente entre gráficos.
- Evitar corte del tooltip en borde superior.

**Non-Goals:**
- Cambiar queries, endpoints, o formato de datos.
- Rediseño del dashboard ni nuevos gráficos.
- Añadir plugin Chart.js externo o tooltip custom HTML.

## Decisions

### 1. Configurar `barPercentage`/`categoryPercentage` en dataset (no en options globales)
- **Decisión:** En cada `datasets: [{ barPercentage: 0.55, categoryPercentage: 0.65, ... }]` para `chartColegios` y `chartDistritos`. Valor 0.55/0.65 deja ~35% de aire por categoría, probado en referencia profesional; 0.5–0.6 / 0.6–0.7 es rango aceptable, fijamos punto medio para consistencia.
- **Rationale:** Controla ancho relativo sin tocar `options.scales.x.barThickness` que sería absoluto y rompe responsive.
- **Alternativa:** `barThickness: 24` — rechazada: no escala con nº de categorías ni ancho de card.

### 2. Tooltip nativo con `position: 'nearest'` + `yAlign: 'bottom'` + caret
- **Decisión:** `options: { plugins: { tooltip: { enabled: true, position: 'nearest', yAlign: 'bottom', xAlign: 'center', caretSize: 7, caretPadding: 9, padding: 9, cornerRadius: 7, displayColors: false, backgroundColor: 'rgba(17,24,39,0.92)', titleColor: '#fff', bodyColor: '#fff', borderColor: 'rgba(255,255,255,0.12)', borderWidth: 1, titleFont: { weight: '600' } } }, layout: { padding: { top: 16 } } }` + `scales.y.suggestedMax` con 12% margen (calculado como `max*1.12`).
- **Rationale:** `yAlign: 'bottom'` fuerza tooltip arriba de la barra con caret apuntando hacia abajo; `nearest` evita salto a `average` cuando hay pocas barras; `caretPadding` separa burbuja de la barra; `layout.padding.top` evita corte sin tocar `clip` del canvas.
- **Alternativa:** Tooltip custom HTML externo — rechazada: más código, debe reimplementar caret y sombra; nativo con caret es suficiente.

### 3. Mantener tema oscuro/claro via `chartColores()`
- **Decisión:** Reusar `chartColores()` para `backgroundColor`/`borderColor` del tooltip, pero fijar fondo tooltip a oscuro semitransparente con borde sutil para contraste en ambos temas; texto siempre blanco para legibilidad de burbuja.
- **Alternativa:** Tooltip con `backgroundColor: chartColores().primary` — rechazada: poco contraste y se confunde con barra.

### 4. Margen superior via `layout.padding` + `suggestedMax`
- **Decisión:** Añadir `layout: { padding: { top: 14 } }` en `options` y `scales.y: { suggestedMax: Math.ceil(max*1.12), beginAtZero: true }`. Si `max` es 0 (sin datos) no se aplica.
- **Rationale:** `suggestedMax` no fuerza escala si datos son bajos, solo da aire; `layout.padding` da espacio de render del tooltip fuera del área de dibujo sin aumentar altura del canvas.
- **Alternativa:** `padding-top` CSS en `.chart-frame` — complementario pero no sustituye `suggestedMax`; se puede añadir como respaldo `style.css: .chart-frame { padding-top: 4px }`.

## Risks / Trade-offs

- **Tooltip oscuro en tema claro puede desentonar** → Mitigación: usar fondo `rgba(17,24,39,0.92)` con borde claro es estándar dashboards (contraste) y pasa en ambos temas; si se prefiere claro en light, se puede bifurcar por `dark` flag.
- **`suggestedMax` con pocos datos deja mucho vacío arriba** → Mitigación: 12% es compromiso; con max=2, suggestedMax=3 deja solo 1 unidad extra, no excesivo.
- **Barras muy delgadas con pocas categorías (2–3) pueden verse ralas** → Mitigación: 0.55/0.65 sigue dejando barras legibles; si hay 2 colegios, el aire es deseado para look profesional, no se ve vacío.
- **Chart.js `position: 'nearest'` puede variar xAlign en bordes** → Mitigación: fijar `xAlign: 'center'` estabiliza; probar en 360px y 1024px.

## Migration Plan

1. Editar `app/templates/dashboard/index.html` — únicos 2 bloques `new Chart(...)` para colegios/distritos.
2. Verificar visual en 360/768/1024 con datos de seed (6 colegios, 3 distritos) y con barra al máximo (mock `max`).
3. `make lint-boundaries` y `pytest tests/test_boundaries.py` siguen verdes (sin cambio Python).
4. Rollback: revertir `barPercentage`/`tooltip` a valores previos (un commit).

## Open Questions

- ¿Tooltip debe mostrar solo valor o también porcentaje del total? Default: solo valor + label (ej. "San Juan — 12 alumnos"), sin porcentaje en v1.
