## Purpose

Provee reportes institucionales exportables (Excel con branding y CSV espejo) para alumnos, visitas, colegios y carreras, con libros multi-hoja, filtros, permisos por rol y gráficos, trazados en auditoría.

## ADDED Requirements

### Requirement: Branding institucional en Excel

Cada `.xlsx` SHALL incluir en hoja `Resumen` fila 1 logo `logo.png` 80×80 en A1 sobre franja título `IESTP Paiján — Reporte <Tipo>` (Inter/Calibri 14pt bold `#172033`), fila 3 metadata `Generado: DD Mon YYYY HH:MM — Usuario: <nombres> (<DNI>)` en italic 9pt `#64748b`, y fila 4 header con fondo `#2563eb` texto blanco bold, bordes `thin #dde4ee`. Detalle SHALL usar zebra `#f8fafc`, props Author=`SGRV` Title=`Reporte <Tipo> YYYY-MM-DD` y footer impresión `Página &P de &N`.

#### Scenario: Excel Alumnos con branding
- **WHEN** supervisor descarga `/reportes/alumnos/excel`
- **THEN** el .xlsx abre con logo en Resumen!A1, título "IESTP Paiján — Reporte Alumnos" en A2, metadata con usuario y fecha en A3, y header azul en Detalle!A4

#### Scenario: Props y footer
- **WHEN** se inspecciona el .xlsx en Excel → Archivo → Información → Propiedades
- **THEN** Author es `SGRV` y Title contiene `Reporte Alumnos`, y al imprimir cada hoja muestra "Página 1 de 2" en footer

### Requirement: Libro multi-hoja Resumen+Detalle

Cada reporte SHALL ser libro de 2 hojas: `Resumen` (índice 0) y `Detalle` (índice 1). `Resumen` SHALL contener 3-4 KPIs en cajas con borde double y fill `#e8f0ff` (ej. TOTAL, edad prom, % interesados), tabla top 5 y un gráfico nativo openpyxl. `Detalle` SHALL tener `freeze_panes=A5`, `autoFilter` sobre header fila 4, anchos calibrados por columna, y fila final totales en bold con borde top double. Si el dataset está vacío, `Detalle` SHALL tener solo header + fila "Sin registros" y `Resumen` SHALL mostrar "Sin datos suficientes" sin chart.

#### Scenario: Libro Alumnos con 2 hojas y freeze
- **WHEN** se abre `alumnos.xlsx` con 42 alumnos
- **THEN** hay hojas `Resumen` y `Detalle`, Detalle tiene freeze en A5, autofilter en A4:O4, y al hacer scroll la fila 4 permanece visible

#### Scenario: Dataset vacío sin error
- **WHEN** se exporta visitas con rango sin resultados
- **THEN** Detalle tiene header + "Sin registros" y Resumen muestra KPIs en 0 sin lanzar excepción y sin chart

### Requirement: Filtros por reporte reflejados en UI y Excel

La UI `/reportes/` SHALL exponer filtros GET por tipo: alumnos (dni, nombres, apellidos, colegio, distrito, sexo, carrera, edad_desde/hasta, fecha_desde/hasta), visitas (fecha_desde/hasta, promotor, colegio), colegios (distrito, provincia, tipo), carreras (área). El controller SHALL leer `request.args` y pasar `params` al service que SHALL filtrar via `registro/public.py` o queries directas. El Excel SHALL escribir en Resumen!A3 y Detalle!A3 `Filtros: <lista humana>` o `Filtros: Todos (N registros)` si vacío. Rango inválido SHALL producir `ValueError('Rango de fechas inválido')` con flash y redirect a `/reportes/`.

#### Scenario: Filtro aplicado visible en Excel
- **WHEN** se descarga `/reportes/alumnos/excel?sexo=M&colegio=San+Juan&fecha_desde=2026-08-01`
- **THEN** Detalle!A3 contiene "Filtros: Sexo=M | Colegio=San Juan | 01/08/2026 — 04/09/2026" y el listado solo trae alumnos M de ese colegio en ese rango

#### Scenario: Sin filtros muestra Todos
- **WHEN** se descarga `/reportes/colegios/excel` sin query
- **THEN** Detalle!A3 contiene "Filtros: Todos (6 registros)" y lista los 6 colegios del seed

#### Scenario: Rango inválido
- **WHEN** se solicita `/reportes/visitas/excel?fecha_desde=2026-13-40`
- **THEN** el sistema hace flash "Rango de fechas inválido" y redirige a `/reportes/` sin generar archivo

### Requirement: Permisos por rol para exportar

Solo roles 1 (Admin), 2 (Supervisor) y 4 (Consultas) SHALL poder acceder a `/reportes/` y a las 8 rutas de descarga (`/alumnos/csv|excel` etc). Rol 3 (Operador) SHALL recibir 302 a `/dashboard` con flash `No tiene permisos`. Cada descarga exitosa SHALL registrar auditoría `Exportación <FORMATO>` en módulo `Reportes` con detalle `Exportado <tipo>`.

#### Scenario: Consultas puede exportar
- **WHEN** usuario 99998888 (rol 4) autenticado pide `GET /reportes/alumnos/excel`
- **THEN** recibe 200 con `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` y se crea fila en `auditorias` con `usuario_id=99998888, accion=Exportación EXCEL, modulo=Reportes`

#### Scenario: Operador bloqueado
- **WHEN** operador 11112222 (rol 3) pide `GET /reportes/`
- **THEN** recibe 302 Location `/dashboard` y flash danger

### Requirement: Mini gráficos nativos por reporte

Cada `Resumen` SHALL contener un gráfico nativo openpyxl anclado (ej. `D5` o `A15`, tamaño ~15×7.5 cm) con paleta `primary #2563eb / success #16803c / info #0f7490`: Alumnos PieChart sexo (M/F), Visitas LineChart registros por mes, Colegios BarChart horizontal ranking por total, Carreras DoughnutChart por total. Si dataset <2 categorías, el gráfico SHALL no crearse y Resumen SHALL mostrar placeholder texto.

#### Scenario: Gráfico Alumnos sexo
- **WHEN** hay 22 M y 20 F y se abre `alumnos.xlsx` Resumen
- **THEN** existe un PieChart con 2 porciones etiquetadas `M (52.4%)` y `F (47.6%)` con colores `#2563eb` y `#0f7490`

#### Scenario: Fallback sin gráfico
- **WHEN** hay 0 carreras con alumnos (todo 0)
- **THEN** Resumen de carreras.xlsx no contiene chart y muestra "Sin datos suficientes para gráfico"

### Requirement: CSV espejo con formato Excel ES

El CSV SHALL tener los mismos headers que Excel fila 4, delimitados por `;`, codificados en `utf-8-sig` (BOM), con fechas `yyyy-mm-dd` y horas `HH:MM`, y SHALL respetar los mismos filtros que el Excel. Content-Type `text/csv` y `Content-Disposition: attachment; filename=<tipo>.csv`.

#### Scenario: CSV Alumnos con ; y BOM
- **WHEN** se descarga `/reportes/alumnos/csv?sexo=F`
- **THEN** el contenido empieza con BOM `\xEF\xBB\xBF`, primera línea `DNI;Nombres;Apellidos;Edad;Sexo;Celular;Email;Institución;Carrera` y solo filas F

#### Scenario: CSV respeta filtros idénticos a Excel
- **WHEN** se descarga CSV y Excel de visitas con mismo `fecha_desde/hasta`
- **THEN** ambos contienen el mismo número de filas (mismo dataset filtrado)
