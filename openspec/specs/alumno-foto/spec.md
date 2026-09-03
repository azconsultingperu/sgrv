# alumno-foto Specification

## Purpose
Permite al personal autorizado adjuntar una foto opcional del estudiante al final del formulario de registro/edición para dotar de identidad visual al expediente y facilitar identificación en campo, reutilizando el patrón probado de avatar de perfil pero aislado para alumnos.

## Requirements

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

### Requirement: Modelo y storage de foto de alumno

El sistema SHALL añadir a `Alumno` la columna `foto VARCHAR(255) nullable` con migración Alembic, y SHALL proveer helpers `tiene_foto() -> bool` y `foto_url(thumb=False) -> str` que retornen URL privada `url_for('registro.servir_foto', alumno_id=id)` o fallback a `url_for('static', filename='img/avatar-default.svg')` o iniciales con color hash. El storage SHALL ser `app/static/uploads/alumnos/` (config `ALUMNO_FOTO_DIR`), con constantes `ALUMNO_FOTO_MAX_SIZE = 2*1024*1024`, `ALUMNO_FOTO_MAX_DIM = 1000`, `ALUMNO_FOTO_FULL_DIM = 600`, `ALUMNO_FOTO_THUMB_DIM = 90`, `ALUMNO_FOTO_EXTENSIONS = {'png','jpg','jpeg','webp','gif'}` en `app/config.py`.

#### Scenario: Columna nullable en BD
- **WHEN** se aplica la migración y se lista `alumnos` existentes
- **THEN** todos tienen `foto IS NULL` sin romper lecturas previas

#### Scenario: Helper sin foto devuelve fallback
- **WHEN** `alumno.tiene_foto()` es False y se llama `foto_url()`
- **THEN** retorna `/static/img/avatar-default.svg` (o URL de iniciales) y no una ruta de upload

#### Scenario: Helper con foto devuelve URL privada
- **WHEN** `alumno.foto = "12_abc.webp"` y se llama `foto_url(thumb=True)`
- **THEN** retorna `/registro/foto/12?t=1` que sirve el thumb webp

### Requirement: Validación y procesamiento de imagen

El sistema SHALL validar en servidor cada upload de `foto` igual que `perfil_controller._procesar_avatar`: verifica `extension in ALUMNO_FOTO_EXTENSIONS`, `len(datos) <= MAX_SIZE`, `PIL.Image.verify()` válida, `ancho*alto <= 50_000_000`, `ImageOps.exif_transpose`, conversión a `RGBA/RGB`, `thumbnail((600,600), LANCZOS)` y guardado WEBP quality 85 (full) y 80 (thumb). Errores SHALL retornar `400/413` con JSON `{'ok': False, 'error': '<mensaje>'}` y no crear alumno si es registro. Si la validación falla en registro con multipart, el form SHALL re-renderizar con flash `danger` sin perder los demás campos.

#### Scenario: Formato no permitido
- **WHEN** se sube `foto` con extensión `.pdf`
- **THEN** la respuesta es `400` con error "Formato no permitido. Use JPG, PNG, WebP o GIF." y no se crea alumno

#### Scenario: Imagen demasiado grande
- **WHEN** se sube `foto` de 3 MB (supera 2 MB)
- **THEN** la respuesta es `413` con error "La imagen supera los 2 MB" y no se guarda

#### Scenario: Imagen válida se convierte a WEBP
- **WHEN** se sube `foto` PNG 1000x1000 válida
- **THEN** en disco quedan `id_uuid.webp` y `id_uuid_min.webp` ambos `image/webp`

### Requirement: Serving privado y privacidad

El sistema SHALL servir fotos solo a usuarios autenticados vía `GET /registro/foto/<alumno_id>` y `GET /registro/foto/<alumno_id>?t=1` con `@login_required`, verificando path seguro dentro de `ALUMNO_FOTO_DIR` y retornando `404` → fallback a `avatar-default.svg` si no existe. La respuesta SHALL tener `Cache-Control: private, max-age=0, must-revalidate` y `mimetype image/webp`. SHALL NOT exponer fotos sin login ni listarlas en `static` público.

#### Scenario: Sin login no se ve foto
- **WHEN** un visitante sin sesión hace `GET /registro/foto/1`
- **THEN** es redirigido a login (302) y no ve la imagen

#### Scenario: Con login ve foto
- **WHEN** un usuario autenticado hace `GET /registro/foto/1` de alumno con foto
- **THEN** recibe `200 image/webp` con la foto

#### Scenario: Alumno sin foto sirve default
- **WHEN** se pide foto de alumno sin foto o archivo faltante
- **THEN** el servidor retorna `avatar-default.svg` con `200 image/svg+xml`

### Requirement: Borrado de foto al eliminar alumno

Cuando `POST /registro/eliminar/<id>` ejecuta soft delete (o hard según regla vigente) y el alumno tiene `foto`, el sistema SHALL borrar ambos archivos (`{base}.webp` y `{base}_min.webp`) del disco salvo que una fila de `auditorias` los referencie como snapshot histórico (mismo criterio que `_drop_avatar_files` en perfil). Si borrado es soft (`eliminado=True`), también SHALL borrar archivos físicos porque el caso de uso es "no desea estudiar / problemas de asistencia" y no se conserva expediente visual. El alumno queda `eliminado=True` y su foto en BD se pone `NULL` tras borrar archivos.

#### Scenario: Eliminar alumno con foto borra archivos
- **WHEN** admin hace `POST /registro/eliminar/5` de alumno con `foto="5_abc.webp"`
- **THEN** tras commit, `alumno.eliminado=True`, `alumno.foto IS NULL` y no existen `5_abc.webp` ni `5_abc_min.webp` en `alumnos/`

#### Scenario: Eliminar alumno sin foto no falla
- **WHEN** se elimina alumno sin foto
- **THEN** el borrado de foto es no-op y no lanza error

#### Scenario: Reemplazo no deja huérfanos
- **WHEN** se reemplaza foto en edición
- **THEN** los archivos viejos son borrados inmediatamente después de guardar los nuevos
