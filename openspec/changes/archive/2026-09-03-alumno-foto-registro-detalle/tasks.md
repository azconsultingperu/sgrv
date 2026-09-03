## 1. Modelo y migración

- [x] 1.1 Añadir `foto = db.Column(db.String(255), nullable=True)` + helpers `tiene_foto()`, `foto_url(thumb=False)`, `iniciales()` y `foto_color()` a `app/modules/registro/domain/alumno.py` y verificar que `flask db migrate -m "add alumno foto"` genera migración con columna nullable sin defaults.
- [x] 1.2 Añadir constantes `ALUMNO_FOTO_DIR`, `ALUMNO_FOTO_MAX_SIZE=2*1024*1024`, `ALUMNO_FOTO_MAX_DIM=1000`, `ALUMNO_FOTO_FULL_DIM=600`, `ALUMNO_FOTO_THUMB_DIM=90`, `ALUMNO_FOTO_EXTENSIONS` a `app/config.py` y verificar que `create_app` crea el directorio con `os.makedirs`.
- [x] 1.3 Crear migración Alembic y verificar `flask db upgrade` en testing deja `alumnos` existentes con `foto IS NULL` y `foto_url()` retorna fallback.

## 2. Storage y serving privado

- [x] 2.1 Crear `app/modules/registro/infrastructure/alumno_foto_storage.py` con `_foto_dir()`, `_path_seguro()`, `_drop_foto_files()`, `guardar_foto(alumno, file_storage)` (PIL verify, exif_transpose, thumbnail WEBP 600/90, uuid, borrado seguro) y verificar conversión a WEBP en test unitario con imagen sintética 800x800.
- [x] 2.2 Añadir rutas `GET /registro/foto/<int:alumno_id>` y `?t=1` en `registro_controller.py` con `@login_required`, `_path_seguro`, fallback a `avatar-default.svg` y headers `private, max-age=0`, y verificar con test que sin login redirige 302 y con login retorna 200 webp.
- [x] 2.3 Integrar `guardar_foto` en `POST /registro/` y `POST /registro/editar/<id>` (multipart) con validación de extensión/tamaño y manejo de errores JSON/flash, y verificar que `POST` sin foto crea alumno y con foto válida guarda archivos.

## 3. UI Registro (opcional + cámara + móvil)

- [x] 3.1 Añadir sección 6 "Foto del Estudiante" al final de `app/templates/registro/index.html` (antes de Guardar) con `enctype="multipart/form-data"`, `input type=file accept=".png,.jpg,.jpeg,.webp,.gif" capture="environment"`, preview circular 110px (`#alumnoFotoWrap`), botones Cambiar/Eliminar, texto ayuda "JPG, PNG, WebP o GIF · máx. 2 MB · opcional" y JS preview FileReader con validación previa, y verificar render en desktop y móvil 375px.
- [x] 3.2 Replicar sección foto en `app/templates/registro/editar.html` mostrando foto existente vía `alumno.foto_url()` o iniciales, con botón Eliminar visible solo si `tiene_foto()`, y verificar que `GET /registro/editar/<id>` muestra preview correcto.
- [x] 3.3 Añadir JS que haga `capture="environment"` funcional (cámara trasera en móvil), `loading` lazy y manejo de `Eliminar` (limpia input y preview a iniciales), y verificar en emulación móvil que file picker ofrece cámara.

## 4. Detalle 4→2 cards estilo perfil

- [x] 4.1 Reemplazar `app/templates/consulta/detalle.html` de 4 cards 2x2 a `col-md-4` foto 110px (`#alumnoFotoWrap` idéntico a perfil) + nombre/DNI badge/colegio + `col-md-8` tabla consolidada con headers `Datos Personales/Contacto/Colegio/Académicos y Visita` y verificar que `GET /consulta/detalle/<id>` renderiza 2 cards y no 4.
- [x] 4.2 Implementar fallback a iniciales con color hash cuando `not tiene_foto()` y fallback a `avatar-default.svg` cuando archivo falta, y verificar ambos casos con test de template.
- [x] 4.3 Verificar paridad de datos: todos los campos de las 4 cards viejas (incl. visita fecha/hora/promotor/observaciones) siguen presentes con mismo formato `dd/mm/YYYY` y `HH:MM`.

## 5. Listado con thumb 32px

- [x] 5.1 Añadir primera columna thumb 32px (`avatar-sm` circular) en `app/templates/consulta/index.html` antes de DNI, con `<img src="{{ a.foto_url(thumb=True) }}" loading="lazy" alt="Foto de ...">` si `tiene_foto()` else `<span>` iniciales, y verificar que header tiene 9 columnas y `tbody` muestra thumbs.
- [x] 5.2 Verificar serving thumb privado, fallback a full y `loading="lazy"` + `alt` en test de integración con `TestingConfig` y cliente login.

## 6. Borrado con foto y verificación

- [x] 6.1 Modificar `POST /registro/eliminar/<id>` para borrar archivos foto (`*.webp` y `*_min.webp`) tras soft delete (salvo snapshot auditoría), poner `foto=NULL`, y verificar que `POST` de alumno con foto elimina archivos del disco.
- [x] 6.2 Verificar que eliminar alumno sin foto y reemplazar foto en edición no dejan huérfanos (no error, no archivos viejos) con tests de filesystem.
- [x] 6.3 Verificación E2E: registrar alumno con foto vía `POST /registro/` (multipart), ver thumb en `/consulta/`, ver foto grande en `/consulta/detalle/<id>`, editar reemplazando foto, eliminar y verificar que `GET /registro/foto/<id>` retorna default.
