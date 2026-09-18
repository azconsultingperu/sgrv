## ADDED Requirements

### Requirement: Operadores activos como opciones de Promotor Responsable

El select `promotor_id` en `registro/index.html` y `registro/editar.html` SHALL listar la unión en vivo de promotores activos (`promotores.activo=True`) y usuarios activos no eliminados con rol Operador (`usuarios.rol_id=3`, `estado=True`, `eliminado=False`), ordenados alfabéticamente por apellidos+nombres. Cada opción Operador SHALL mostrar `nombres + apellidos` del usuario en el mismo formato que las opciones de promotor clásico y SHALL distinguirse con marcador de origen (atributo `data-origen="operador"` y sufijo visual o agrupación `optgroup`). El placeholder `Seleccionar promotor...` SHALL mantenerse como primera opción y el campo SHALL seguir siendo opcional (envío vacío guarda visita sin promotor).

#### Scenario: Operador aparece en registro
- **WHEN** un usuario autorizado abre `GET /registro/` existiendo al menos un Operador activo (ej. Operador seed 11112222)
- **THEN** el HTML contiene dentro de `#promotor_id` una `<option>` con su nombre (`OPERADOR APELLIDO`) marcada con `data-origen="operador"`, además de las opciones de `promotores` clásicos.

#### Scenario: Nuevo Operador aparece sin pasos manuales
- **WHEN** un admin crea un usuario con rol Operador vía `POST /usuarios/crear` y luego se abre `GET /registro/`
- **THEN** el nuevo nombre ya figura en `#promotor_id` (la fuente se consulta en vivo en cada render, sin sincronización manual ni job).

#### Scenario: Editar también lista Operadores
- **WHEN** se abre `GET /registro/editar/<id>`
- **THEN** `#promotor_id` contiene las mismas opciones unión que en registro y preselecciona la referencia guardada en la visita (sea promotor clásico u Operador).

#### Scenario: Operador inactivo o eliminado no aparece
- **WHEN** un Operador tiene `estado=False` o `eliminado=True`, o cambia de rol
- **THEN** su nombre deja de figurar en `#promotor_id` en el siguiente `GET`, pero las visitas históricas que lo referencian siguen mostrando su nombre (snapshot o resolución tolerante).

### Requirement: Guardado y visualización de visita con promotor Operador

El backend `POST /registro/` y `POST /registro/editar/<id>` SHALL aceptar una referencia a Operador además de un `promotor_id` clásico, SHALL persistirla en la visita sin romper el FK existente, y todas las vistas que muestran promotor (consulta/detalle "No asignado", reportes CSV/Excel, email `nuevo_registro.html`) SHALL mostrar el nombre del Operador cuando la visita lo referencia y SHALL seguir mostrando el promotor clásico o "No asignado" en los demás casos.

#### Scenario: Registro con Operador se guarda
- **WHEN** se envía `POST /registro/` con datos válidos y la opción Operador elegida
- **THEN** la respuesta redirige con `Registro creado exitosamente` y la visita queda vinculada al Operador (no a un promotor clásico ni a `NULL`).

#### Scenario: Detalle muestra nombre del Operador
- **WHEN** se abre el detalle/consulta de un alumno cuya visita referencia a un Operador
- **THEN** el campo Promotor muestra `nombres + apellidos` del Operador en vez de "No asignado".

#### Scenario: Visitas históricas intactas
- **WHEN** existen visitas con `promotor_id` clásico o `NULL` anteriores al cambio
- **THEN** siguen mostrándose igual que antes (nombre clásico o "No asignado") y los reportes no fallan por `None`.

## MODIFIED Requirements

### Requirement: Persistencia de selects y derivados tras error de validación

Cuando `POST /registro/` falla por validación y el controller hace `render_template(..., form=request.form)`, el HTML SHALL repintar los 3 selects (`institucion_id, carrera_id, promotor_id`) con la opción previamente elegida marcada `selected` usando comparación `|string` (`form.xxx|string == c.id|string`), y SHALL re-disparar el JS que rellena `distrito/provincia` y `edad` para que los campos readonly también muestren el valor previo sin requerir nuevo `change`. Para `promotor_id`, la comparación SHALL resolver también valores con prefijo de origen (ej. opción Operador) de modo que si el usuario había elegido un Operador, ese Operador quede como `selected` tras el re-render y no se pierda a "Seleccionar...". El `input type=file` de foto SHALL permanecer vacío por seguridad del browser.

#### Scenario: Selects persisten
- **WHEN** el usuario elige `institucion_id=3, carrera_id=2, promotor_id=5` y envía con `dni` inválido
- **THEN** la respuesta `200` re-renderiza el form con los 3 selects mostrando `3,2,5` como `selected` y no "Seleccionar..."

#### Scenario: Operador elegido persiste tras error
- **WHEN** el usuario elige un Operador en `promotor_id` y envía con `dni` inválido
- **THEN** la respuesta `200` re-renderiza el form con ese Operador como `selected` (no vuelve a "Seleccionar...").

#### Scenario: Derivados se re-hidratan
- **WHEN** la respuesta re-renderiza con `institucion_id=3` y `fecha_nacimiento=2008-01-01`
- **THEN** `distrito/provincia` muestran el distrito/provincia de la institución `3` y `edad` muestra la edad calculada sin que el usuario toque el select/fecha

#### Scenario: Foto no persiste
- **WHEN** se re-renderiza tras error con foto previamente seleccionada
- **THEN** el `input file` queda vacío (comportamiento estándar) y el usuario debe re-seleccionar la foto si desea

#### Scenario: Editar también persiste
- **WHEN** `POST /registro/editar/<id>` falla por validación
- **THEN** los mismos 3 selects y derivados se repintan igual que en `index`

#### Scenario: Provincia autocompletada al elegir colegio
- **WHEN** el usuario cambia `institucion_id` a un colegio con `provincia="Ascope"`
- **THEN** los inputs `distrito`, `provincia` y `region` se actualizan inmediatamente a los valores del colegio sin recargar

#### Scenario: Limpieza al deseleccionar
- **WHEN** el usuario vuelve a `Seleccionar institución...`
- **THEN** `distrito`, `provincia` y `region` quedan vacíos (o región vuelve a valor por defecto si aplica)
