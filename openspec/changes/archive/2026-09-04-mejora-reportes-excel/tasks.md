## 1. Base y estilos

- [x] 1.1 Crear `app/modules/reportes/application/excel_styles.py` con paleta (`BRAND_PRIMARY #2563eb`, `ZEBRA #f8fafc`, `BORDER #dde4ee`), helpers `style_header(cell)`, `style_kpi_box(ws, ref, valor)`, `autosize_columns(ws, anchos)`, `add_logo(ws, "Resumen")` y `setup_print(ws)` y verificar import sin error con `python -c "from app.modules.reportes.application.excel_styles import style_header"`.
- [x] 1.2 Refactorizar `app/modules/reportes/application/reporte_service.py` a 4 generadores tipados `generar_alumnos_excel(params)`, `generar_visitas_excel(params)`, `generar_colegios_excel(params)`, `generar_carreras_excel(params)` que reusan `registro/public.py` para filtros y usan `excel_styles`, manteniendo `generar_reporte_excel(tipo, params)` como facade y verificar `FLASK_ENV=testing pytest tests/test_reportes.py -k excel -v` pasa.

## 2. Filtros y permisos

- [x] 2.1 Actualizar `app/modules/reportes/presentation/reportes_controller.py` para leer `request.args` (dni/nombres/apellidos/colegio/distrito/sexo/carrera/edad/fechas/promotor/tipo/área) y pasar `params` a cada generador, convalidación `ValueError('Rango de fechas inválido')` → flash + redirect, y verificar descarga con `?sexo=M` filtra filas.
- [x] 2.2 Cambiar `supervisor_required` a `rol_id in (1,2,4)` para permitir Consultas, mantener 3 bloqueado, y verificar con tests: `auth_client` rol4 recibe 200 en `/reportes/alumnos/excel` y cliente operador recibe 302 a `/dashboard`.
- [x] 2.3 Actualizar `app/templates/reportes/index.html` para añadir form GET con datepickers `fecha_desde/hasta`, selects `colegio` (list_instituciones), `distrito` distinct, `carrera` (list_carreras), `sexo`, `tipo`, con botón Filtrar que preserve query en links de descarga y verificar en browser que `/reportes/?sexo=M` mantiene selección.

## 3. Libro multi-hoja y branding

- [x] 3.1 Implementar para cada reporte estructura 2 hojas `Resumen` (índice 0) y `Detalle` (índice 1) con: Resumen logo 80×80 `logo.png` en A1, título A2, metadata A3 `Generado: ... — Usuario: ... — Filtros: ...`, 3-4 KPIs en cajas; Detalle header fila 4 azul `#2563eb` bold, `freeze_panes=A5`, `autoFilter`, anchos calibrados, zebra, fila totales bold double-top, `fitToWidth`, y verificar abriendo `alumnos.xlsx` y `colegios.xlsx` que tienen 2 hojas y freeze en A5.
- [x] 3.2 Integrar archivos que genere Claude para cada tipo: colocar contenido normalizado en `reporte_service.py` y `excel_styles.py`, adaptar `A3` filtros y anchos por reporte (Alumnos 15 cols A:O, Visitas 9 cols, Colegios 8 cols, Carreras 5 cols) y verificar visualmente cada `.xlsx` (header, totales, filtros).

## 4. Gráficos y CSV espejo

- [x] 4.1 Añadir 4 gráficos nativos openpyxl en hoja Resumen anclados `D5/A15` ~15×7.5cm con paleta brand: PieChart sexo (Alumnos), LineChart registros por mes (Visitas via `dashboard_get_registros_por_mes`), BarChart horizontal ranking (Colegios), DoughnutChart (Carreras), con fallback si <2 categorías no crear chart y verificar que `alumnos.xlsx` contiene pie y `colegios.xlsx` contiene bar.
- [x] 4.2 Actualizar CSV a espejo Excel: mismos headers fila 4, `delimiter=';'`, `utf-8-sig` BOM, fechas `yyyy-mm-dd`, respetar mismos `params` que Excel, y verificar `GET /reportes/alumnos/csv?sexo=F` empieza con BOM y contiene `;` y igual conteo que Excel.

## 5. Validación

- [x] 5.1 Añadir/actualizar tests en `tests/test_reportes.py`: filtros (sexo/distrito), branding (2 hojas, freeze, header color), permisos rol4 OK y rol3 302, gráficos existen, CSV con `;` y BOM, y verificar `FLASK_ENV=testing pytest tests/test_reportes.py -v` con 8+ tests pasa.
- [x] 5.2 Verificar `venv/bin/lint-imports` keeps 5/5 y `openspec validate` sin errores, más prueba manual: generar los 4 xlsx con y sin filtros, con dataset vacío y 1 fila, comprobar props Author=SGRV, footer y auditoría `Exportación EXCEL` creada.
