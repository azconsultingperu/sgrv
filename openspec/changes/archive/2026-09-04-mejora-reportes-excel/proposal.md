## Why

Los reportes actuales (`reporte_service.py:1`) generan Excel y CSV pelados — `ws.append` sin estilos, sin logo, sin freeze, sin totales y con columnas incompletas (alumnos solo 9 de 15 campos). La UI (`reportes/index.html:9`) no expone filtros y el rol Consultas (4) no puede exportar aunque el seed lo promete. Para directivos del IESTP el archivo luce como dump de BD, no como reporte institucional imprimible. Claude generará plantillas profesionales y este change las integra.

## What Changes

- **Branding institucional (opción B completa):** Logo `logo.png` 80×80 en A1, franja título `IESTP Paiján` en Inter 14pt bold `#172033`, metadata `Generado: 04 Sept 2026 14:05 — Usuario: Admin (DNI) — Filtros: ...` en italic 9pt `#64748b`, header tablas `#2563eb` sobre blanco, zebra `#f8fafc`, bordes `thin #dde4ee`, props Author/Title y footer impresión `Página &P de &N`.
- **Libro multi-hoja Resumen+Detalle:** Cada `.xlsx` pasa a 2 hojas (Resumen ejecutivo con KPIs + Detalle con datos). Resumen con KPIs en cajas + tablas top 5 + gráficos nativos openpyxl; Detalle con `freeze A5`, `autoFilter`, anchos calibrados, totales y `fitToWidth`.
- **Filtros reales por reporte:** Exponer en UI datepickers/selects y respetar `request.args` (12 filtros de `consulta_controller.py:9` y `registro/public.py:115`): alumnos (dni/nombres/apellidos/colegio/distrito/sexo/carrera/edad/fechas), visitas (fecha_desde/hasta/promotor/colegio), colegios (distrito/provincia/tipo), carreras (área). Escribir `Filtros: ...` en A3 y `Todos` si vacío; validar rango con flash `Rango inválido`.
- **Rol Consultas exporta:** Cambiar `supervisor_required` de `(1,2)` a `(1,2,4)` en `reportes_controller.py:30`; Operador (3) sigue bloqueado. Actualizar tests.
- **Mini gráficos nativos:** PieChart sexo (Alumnos), LineChart registros por mes (Visitas), BarChart horizontal ranking (Colegios), DoughnutChart por carrera (Carreras) — en hoja Resumen, colores `#2563eb/#16803c/#0f7490`, con fallback si <2 filas no crear chart.
- **CSV espejo:** Headers idénticos a Excel fila 4, `delimiter=';'` + `utf-8-sig` BOM, fechas `yyyy-mm-dd`.

## Capabilities

### New Capabilities
- `reportes`: Generación de reportes institucionales Excel/CSV con branding, multi-hoja, filtros, permisos y gráficos — comportamiento observable de exportación.

### Modified Capabilities
- Ninguna (no existía spec previa de reportes; se crea como nueva).

## Impact

- `app/modules/reportes/application/reporte_service.py` — refactor a 4 generadores tipados + `excel_styles.py` (helper estilos/colores/anchos).
- `app/modules/reportes/presentation/reportes_controller.py` — decorador roles (1,2,4) + lectura de filtros + `registrar` auditoría sin regresión.
- `app/templates/reportes/index.html` — añade filtros UI (datepickers, selects colegio/distrito/carrera/sexo) con GET.
- `app/static/img/logo.png` — embebido en Excel vía `openpyxl.drawing.image`.
- `tests/test_reportes.py` — + test rol 4 puede exportar, + tests filtros y headers.
- Sin migración BD, sin nueva dependencia (openpyxl ya en `requirements.txt:13`).
