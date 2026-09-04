## Context

Ver `proposal.md` Why. Hoy `reporte_service.py:1` tiene 2 funciones monolíticas con `if tipo == 'alumnos'` y queries con N+1 (`colegios` hace `count` por cada IE). Excel sin estilos (`ws.append` + `wb.save`). Controller solo permite roles 1,2 y visitas filtra por fecha pero UI no expone inputs. El seed promete rol 4 Consultas con acceso a reportes. Se usará `registro/public.py:115` `consultar_alumnos_paginado` como fuente de filtros para no duplicar lógica.

## Goals / Non-Goals

**Goals:** Excel institucional imprimible con branding B + libro 2 hojas (Resumen+Detalle) + filtros reales por reporte + rol 4 habilitado + 4 gráficos nativos + CSV espejo con `;` + BOM.

**Non-Goals:** No migrar a xlsxwriter (se queda openpyxl ya instalado), no añadir PDF, no persistir reportes generados en `reportes` tabla (sigue solo auditoría), no paginar Excel (todo el dataset filtrado).

## Decisions

**Decisión 1: Generación pura con openpyxl + helper `excel_styles.py` (no plantilla .xlsx binaria)**
- *Por qué:* openpyxl 3.1.2 ya en `requirements.txt:13`, permite `PatternFill`, `Font`, `Border`, `Image`, `charts` y `printSetup` sin binarios externos. Helper centraliza paleta (`BRAND_PRIMARY #2563eb`, `BRAND_SUCCESS #16803c`, `BRAND_MUTED #64748b`, `ZEBRA #f8fafc`, `BORDER #dde4ee`) y funciones `style_header()`, `style_kpi_box()`, `autosize_columns()`. Evita subir `.xlsx` base al repo que habría que versionar.
- *Alternativa descartada:* Plantilla pre-diseñada + `load_workbook` → frágil al cambiar columnas, binario en git.
- *Alternativa descartada:* xlsxwriter → más rápido para charts pero no lee estilos existentes y añade dependencia.

**Decisión 2: Refactor service a 4 funciones tipadas que reusan `registro/public.py`**
- *Por qué:* Cada reporte tiene columnas y joins distintos; 4 funciones `generar_alumnos_excel(params)`, `generar_visitas_excel(params)`, `generar_colegios_excel(params)`, `generar_carreras_excel(params)` aislan queries. Para alumnos/visitas con filtros se llama a `consultar_alumnos_paginado` o query directa con `joinedload` para evitar N+1. `generar_reporte_excel(tipo)` queda como facade que delega.
- *Alternativa descartada:* Mantener `if tipo` gigante → difícil testear y añadir gráficos.
- *CSV:* helper `csv_writer` con `delimiter=';'`, `utf-8-sig`, fecha `yyyy-mm-dd`, mismos headers que Excel fila 4.

**Decisión 3: Libro 2 hojas con Resumen ejecutivo + Detalle (freeze + autofilter)**
- *Por qué:* Directivos quieren KPIs sin scrollear todo el detalle. Resumen en `wb.create_sheet("Resumen",0)` con 3-4 cajas KPI (`TOTAL: 42`, `Edad prom 16.8`, `% interesados 68%`), tabla top5 y chart anclado `D5`. Detalle en segunda hoja con `freeze_panes="A5"` (bajo header), `auto_filter.ref = "A4:O4"`, anchos calibrados (ej. Institución 22, Email 22), zebra con `ConditionalFormatting`, fila totales bold + `SUM` o count, `sheet_properties.pageSetUpPr.fitToWidth=1`.
- *Alternativa descartada:* 1 hoja con todo arriba → mezcla KPIs y datos, rompe impresión.
- *Logo:* `openpyxl.drawing.image.Image('app/static/img/logo.png')` 80×80 en `Resumen!A1`, offset 4px. Si falla load (sin Pillow) → degradar a texto.

**Decisión 4: Filtros en UI + reflejo en Excel + validación**
- *Por qué:* UI añade `<form method="GET">` con datepickers (`fecha_desde/hasta`), selects (`colegio/distrito/carrera/sexo/tipo`) que hacen GET a `/alumnos/excel?...`. Controller lee `request.args` y pasa `params` al service. Excel escribe en `A3` `Filtros: Sexo=M | Colegio=San Juan | 01/08/2026 — 04/09/2026` o `Filtros: Todos (42 registros)`. Validación de rango con `try datetime.strptime` → `ValueError('Rango inválido')` como hoy, flash en redirect.
- *Alternativa descartada:* POST con filtros → rompe bookmark y descarga directa.
- *Reuso:* Para alumnos se usa `consultar_alumnos_paginado` con todos los filtros; para visitas/colegios/carreras se usa `query.filter` directo con `params`.

**Decisión 5: Roles `(1,2,4)` + gráficos con fallback**
- *Por qué:* `supervisor_required` pasa a `(1,2,4)` → Consultas exporta pero Operador(3) no; auditoría ya registra actor. Gráficos: `PieChart` (sexo), `BarChart` (colegios), `LineChart` (visitas por mes desde `dashboard_get_registros_por_mes`), `DoughnutChart` (carreras). Si dataset <2 filas o sin datos → no crear chart (evita `IndexError`), Resumen muestra "Sin datos suficientes".
- *Alternativa descartada:* Permitir a 3 también → viola matriz de permisos `README.md:267`.

## Risks / Trade-offs

- **Logo + gráficos aumentan tamaño (~150KB → 400KB)** → Mitigación: sigue <1MB, aceptable; usar `logo.png` optimizado ya existente.
- **N+1 en colegios/carreras si no se optimiza** → Mitigación: usar `group_by` + `func.count` con `outerjoin` en service nuevo, no `count` por fila.
- **CSV con `;` rompe compatibilidad con parsers que esperan `,`** → Mitigación: documentar en header y ofrecer ambos vía query `?delimiter=comma` futuro; hoy `;` es estándar ES para Excel.
- **Filtros UI sin JS puede ensuciar URL** → Mitigación: form GET simple, sin JS, con `<select>` poblados desde `list_instituciones()`/`list_carreras()` y distrito distinct.

## Migration Plan

Solo frontend+backend sin migración. Pasos: helper estilos → refactorizar service (queries con filtros) → controller roles + params → UI filtros → plantillas Excel por tipo con 2 hojas + charts → CSV espejo → tests. Rollback: revert 4 archivos. Verificación: abrir `/reportes/`, elegir filtros, descargar `alumnos.xlsx`, verificar 2 hojas, filtros en A3, freeze, chart visible, y que rol 4 descarga pero rol 3 recibe 302.

## Open Questions

- Ninguna — branding B, 2 hojas, 12 filtros, rol 4 sí, 4 gráficos acordados.
