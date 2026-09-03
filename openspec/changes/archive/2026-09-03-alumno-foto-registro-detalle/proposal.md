## Why

El registro de visitas carece de identidad visual del estudiante y el detalle actual fragmenta la información en 4 cards desconectadas (`Datos Personales`, `Contacto`, `Datos del Colegio`, `Datos Académicos y Visita`), dificultando lectura rápida en campo. Añadir foto opcional al final de `registro` y rediseñar `consulta/detalle` a 2 cards estilo `Mi Perfil` (foto circular 110px + tabla consolidada) mejora identificación, reduce carga cognitiva y mantiene coherencia con el patrón ya usado en perfil.

## What Changes

- **Foto opcional en registro:** Sección 6 "Foto del Estudiante" al final de `registro/index.html` y `registro/editar.html` con input file, preview circular 110px, botones Cambiar/Eliminar, soporte `capture="environment"` para cámara en móvil y validación igual a perfil (JPG/PNG/WebP/GIF, 2–10MB, 1000x1000, exif transpose, conversión a WEBP 600 + thumb 90). Solo accesible para `rol_id <= 2` (Administrador/Supervisor) vía `admin_or_supervisor_required`. Form pasa a `multipart/form-data`.
- **Modelo + storage:** Nueva columna `alumnos.foto VARCHAR(255) nullable` con migración Alembic, helpers `tiene_foto()/foto_url()` con fallback a iniciales + color hash (reusa `usuario.avatar_color` lógica) y default `img/avatar-default.svg`. Storage en `app/static/uploads/alumnos/` (separado de `perfil`), nombres `{alumno_id}_{uuid}.webp` y `{uuid}_min.webp`, borrado seguro al reemplazar/eliminar.
- **Detalle 4→2 cards:** `consulta/detalle.html` pasa de grid 2x2 a `col-md-4` foto circular 110px centrada + nombre/DNI badge/colegio + `col-md-8` tabla consolidada con secciones. Mantiene edición/volver.
- **Thumb en listado:** `consulta/index.html` añade columna thumb 32px (`avatar-sm` circular) antes de DNI, con `login_required` para servir via `GET /registro/foto/<id>` y `GET /registro/foto/<id>?t=1` (thumb), privadas.
- **Borrado con foto:** `registro.eliminar` (soft delete → hard delete según decisión) elimina archivos físicos de foto junto al registro; `Visita` asociada se borra igual que hoy.

## Capabilities

### New Capabilities
- `alumno-foto`: Foto opcional del alumno en registro/edición, validación, storage, serving privado y borrado. Cubre modelo, controller, storage y UI de registro.
- `consulta-detalle`: Rediseño de detalle de alumno de 4 cards a 2 cards estilo perfil (110px circular como Mi Perfil), integrando foto y consolidando tablas.
- `consulta-listado`: Thumb 32px circular en tabla de consulta/index antes de DNI, con serving privado.

### Modified Capabilities
- Ninguna — todas son capacidades nuevas (no existe spec previa de detalle/listado).

## Impact

- `app/modules/registro/domain/alumno.py` — nueva columna `foto`
- `migrations/versions/*.py` — migración alumno foto
- `app/modules/registro/presentation/registro_controller.py` — manejo `request.files['foto']` en `registrar` y `editar`, nueva ruta `servir_foto` + helpers storage
- `app/modules/registro/infrastructure/alumno_foto_storage.py` (nuevo) — lógica espejo de `perfil_controller._procesar_avatar` pero para alumnos
- `app/config.py` — nuevas constantes `ALUMNO_FOTO_DIR`, `ALUMNO_FOTO_MAX_SIZE`, etc.
- `app/templates/registro/index.html`, `editar.html` — sección foto
- `app/templates/consulta/detalle.html` — re-layout 2 cards
- `app/templates/consulta/index.html` — columna thumb
- Sin breaking changes en API pública más allá de `enctype` del form.
