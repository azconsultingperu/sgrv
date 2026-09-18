## Why

El select "Promotor Responsable" del formulario de registro (`registro/index.html` y `registro/editar.html`) hoy solo lista la tabla `promotores`, que es un catálogo manual de 3 filas seed. Los usuarios con rol Operador (rol 3), que son quienes hacen trabajo de promoción en campo, no aparecen ahí, así que las visitas quedan con `promotor_id=NULL` ("No asignado") o con un nombre que no corresponde al usuario real. Se necesita que todo Operador activo sea elegible como Promotor Responsable y que la lista se actualice sola al crear un nuevo usuario Operador.

## What Changes

- El dropdown "Promotor Responsable" en `GET /registro/` y `GET /registro/editar/<id>` lista la unión de: (a) `Promotor` activos existentes + (b) `Usuario` activos con `rol_id=3` (Operador), ordenados por nombre.
- Cada opción de tipo Operador muestra `nombres + apellidos` del usuario (igual formato que hoy) con un marcador de origen para distinguirlos en UI.
- El `POST /registro/` y `POST /registro/editar/<id>` aceptan tanto un `promotor_id` clásico como una referencia a un Operador; la visita guarda la referencia correcta sin romper visitas históricas con `promotor_id=NULL` o con promotor clásico.
- Al crear un nuevo usuario con rol Operador (`POST /usuarios/crear`), este aparece automáticamente en el dropdown en el siguiente `GET /registro/` sin pasos manuales ni sincronización por lotes (la fuente se consulta en vivo en cada render).
- Reportes, consulta/detalle y emails que muestran `visita.promotor.nombres` siguen funcionando: si la visita apunta a un Operador, muestran su nombre; si es `NULL`, siguen mostrando "No asignado".

## Capabilities

### New Capabilities

- Ninguna. No se introduce una capacidad nueva aislada; se extiende el comportamiento de una existente.

### Modified Capabilities

- `registro-form`: el requirement del select `promotor_id` cambia — la fuente deja de ser solo `promotores` y pasa a ser unión en vivo `promotores activos + usuarios Operador activos`, con persistencia tras error de validación y paridad en `editar.html`.

## Impact

- Afectado: `app/modules/registro/presentation/registro_controller.py:71-73,194-196` (queries de `promotores` en `registrar` y `editar`), `app/templates/registro/index.html:155-159` y `editar.html:121-124` (render del `<select id="promotor_id">`), `app/modules/registro/domain/visita.py` + `promotor.py` (cómo se resuelve el nombre a mostrar), `app/modules/consulta/presentation/consulta_controller.py` y `detalle.html` (muestra de promotor), `app/modules/reportes/application/reporte_service.py:32,67` (acceso directo `v.promotor.nombres` que hoy revienta con `NULL`/Operador).
- No se toca el modelo de roles ni permisos: Operador sigue sin poder registrar/editar (solo Admin/Supervisor); solo su nombre aparece como opción elegible.
- Riesgo principal: colisión de IDs entre tabla `promotores` y `usuarios` si se usa un solo `promotor_id` entero. El diseño debe resolverlo (prefijo de origen, FK nullable adicional o tabla unificada de lectura) sin migración destructiva.
