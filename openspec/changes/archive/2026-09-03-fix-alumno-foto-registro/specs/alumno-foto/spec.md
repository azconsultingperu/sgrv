## MODIFIED Requirements

### Requirement: Campo foto opcional en registro y edición

El sistema SHALL añadir al final de `registro/index.html` y `registro/editar.html` (sección 6 "Foto del Estudiante", después de "Datos de la Visita") un control de subida opcional con preview circular 110px (mismo tamaño y estilo que `#avatarPreviewWrap` en `perfil/index.html`), input `type="file" accept=".png,.jpg,.jpeg,.webp,.gif" capture="environment"` y texto de ayuda "JPG, PNG, WebP o GIF · máx. 2 MB · 1000x1000 px · opcional". El form SHALL usar `enctype="multipart/form-data"` y el campo SHALL llamarse `foto`. En móvil el control SHALL centrar foto, botones y texto de ayuda (`justify-content-center` / `text-center` en `<768px`, `justify-content-md-start` en desktop). El preview sin foto SHALL mostrar `<img src="avatar-default.svg">` dentro del círculo con opacidad tenue (no "--"). El botón inicial en `registro/index.html` SHALL decir "Añadir foto" y tras seleccionar archivo SHALL cambiar a "Cambiar foto" y mostrar "Eliminar"; en `editar.html` con foto existente SHALL decir "Cambiar foto" desde el inicio.

#### Scenario: Registro sin foto
- **WHEN** un supervisor envía `POST /registro/` sin adjuntar archivo en `foto`
- **THEN** el alumno se crea con `foto = NULL` y el registro es válido (no se exige foto)

#### Scenario: Registro con foto válida
- **WHEN** se adjunta `foto` válida (JPG 800x800, 1MB) y se envía `POST /registro/`
- **THEN** el alumno se crea, la foto se convierte a WEBP 600 + thumb 90 y se guarda en `app/static/uploads/alumnos/{id}_{uuid}.webp`

#### Scenario: Registro con foto válida muestra un solo toast de éxito
- **WHEN** `POST /registro/` con foto válida crea alumno correctamente
- **THEN** la respuesta es `302` a `/consulta/` con un único flash `success` "Registro creado exitosamente" y el listado muestra el nuevo alumno; no se muestra flash `danger`

#### Scenario: Registro con foto inválida muestra solo error y no crea duplicado
- **WHEN** se adjunta `foto` con formato no permitido o >2MB y se envía `POST /registro/`
- **THEN** la respuesta NO crea alumno duplicado si ya existe, y muestra un único flash `danger` con el motivo ("Formato no permitido" o "supera los 2 MB") sin flash `success`; si el alumno aún no existía y la foto falla, el alumno creado sin foto permanece pero el flash es solo `danger` explicando que el registro se guardó sin foto (sin doble flash)

#### Scenario: Edición muestra foto existente
- **WHEN** se abre `GET /registro/editar/<id>` de un alumno que ya tiene foto
- **THEN** el preview muestra la foto existente vía `alumno.foto_url()` y el botón Eliminar está visible; si no tiene foto, muestra `avatar-default.svg` centrado y Eliminar está oculto

#### Scenario: Botón inicial es Añadir cuando no hay foto
- **WHEN** se abre `registro/index.html` sin foto previa
- **THEN** el botón dice "Añadir foto" (no "Cambiar foto")

#### Scenario: Tras seleccionar foto el botón cambia a Cambiar
- **WHEN** el usuario selecciona una foto válida en `registro/index.html`
- **THEN** el preview muestra la imagen, el botón pasa a decir "Cambiar foto" y aparece "Eliminar"

#### Scenario: Móvil centra foto y botones
- **WHEN** se abre `registro/index.html` en viewport 375px
- **THEN** la foto 110px, los botones y el texto de ayuda están centrados horizontalmente (`justify-content-center`), no alineados a la izquierda

#### Scenario: Placeholder por defecto es avatar svg
- **WHEN** se abre `registro/index.html` sin haber seleccionado foto
- **THEN** dentro de `#alumnoFotoWrap` se ve `<img src="/static/img/avatar-default.svg">` con opacidad tenue, no texto "--"

#### Scenario: Solo roles autorizados ven el campo
- **WHEN** un usuario con `rol_id <= 2` (Administrador/Supervisor) abre `registro/index.html`
- **THEN** ve la sección foto; un usuario con `rol_id > 2` no accede al módulo (redirect por `admin_or_supervisor_required`)

#### Scenario: Edición reemplaza foto
- **WHEN** en edición se adjunta nueva foto y se envía `POST /registro/editar/<id>`
- **THEN** la foto anterior es borrada del disco (salvo snapshot en auditoría) y la nueva queda como `alumno.foto`
