## 1. Configuración de barras delgadas y espaciadas

- [x] 1.1 Ajustar `chartColegios` en `app/templates/dashboard/index.html:306` con `datasets: [{ barPercentage: 0.55, categoryPercentage: 0.65 }]` y verificar que `getComputedStyle` de la barra vs ancho de categoría deja gap ≥8px en desktop (inspección visual o `chartColegios.getDatasetMeta(0).data[0].width` < 60% de `chart.chartArea` dividido por nº categorías)
- [x] 1.2 Replicar mismo `barPercentage`/`categoryPercentage` en `chartDistritos` (`index.html:318`) y verificar que ambos gráficos comparten valores idénticos vía grep `barPercentage` en el archivo

## 2. Tooltip flotante con caret visible

- [x] 2.1 Configurar `options.plugins.tooltip` en `chartColegios` con `enabled: true, position: 'nearest', yAlign: 'bottom', xAlign: 'center', caretSize: 7, caretPadding: 9, padding: 9, cornerRadius: 7, displayColors: false, backgroundColor/border` según `design.md` y verificar hover sobre barra muestra burbuja arriba con flecha separada ≥8px (no superpuesta) en 1024px
- [x] 2.2 Aplicar idéntico `plugins.tooltip` en `chartDistritos` y verificar que ambos tooltips tienen mismo `caretSize`/`caretPadding`/`padding`/`cornerRadius` (diff del bloque `<script>` idéntico entre ambos charts)

## 3. Margen superior anti-corte y consistencia

- [x] 3.1 Añadir `options.layout.padding.top: 14` y `scales.y: { suggestedMax: Math.ceil(max*1.12), beginAtZero: true }` (donde `max = Math.max(...data)`) en ambos gráficos y verificar que barra al máximo (mock `max` ) no recorta tooltip contra borde superior del `.chart-frame` en 360px
- [x] 3.2 Verificar tema oscuro/claro: alternar `data-bs-theme` y disparar `sgrv:themechange`, confirmar que `aplicarTemaCharts()` sigue actualizando `grid/ticks/border` y que el tooltip mantiene contraste (fondo oscuro semitransparente + borde claro) sin cambiar `datasets` ni queries, y que `make lint-boundaries` sigue verde

## 4. Verificación integral

- [x] 4.1 Ejecutar validación visual manual en 360/768/1024 con datos de seed (6 colegios, 3 distritos): barras delgadas con aire, tooltip burbuja flotante con caret en ambos gráficos, sin corte superior, y verificar que `FLASK_ENV=testing venv/bin/python -m pytest tests/test_boundaries.py -q` pasa sin regresión
