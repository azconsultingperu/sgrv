## Context

Ver `proposal.md` Why. Estado actual: `Alumno` sin campo foto (`alumno.py:7`), `consulta/detalle.html:14` con 4 cards 2x2 y tablas `table-sm`, `perfil/index.html:15` con 2 cards (foto 110px + tabla) ya probado, `perfil_controller.py:135` con pipeline PIL completo (verify, exif_transpose, thumbnail WEBP 600/90, uuid, borrado seguro con check auditoría). Registro ya usa `multipart` parcial y validación DNI. Constraints: monolito modular estricto (`setup.cfg` layers), solo `public.py` cross-módulo, fotos privadas `login_required`, móvil primero.

## Goals / Non-Goals

**Goals:** Reusar patrón avatar de perfil para alumnos sin duplicar deuda, manteniendo foto opcional, serving privado y layout 2 cards idéntico a perfil (110px). Thumb 32px en listado sin N+1, cámara en móvil, borrado físico al eliminar.

**Non-Goals:** No historial de fotos (solo foto actual), no edición de foto sin pasar por registro/editar, no exponer fotos públicas, no cambiar permisos de registro (sigue `admin_or_supervisor_required`), no tocar reportes/excel, no evento de dominio para foto (no hace falta auditar foto, solo alumno).

## Decisions

**Decisión 1: Columna `alumnos.foto` + helpers en domain, storage separado `uploads/alumnos`**
- *Por qué:* 1 alumno = 1 foto actual, espejo de `usuario.avatar`. Separar dir evita colisión y borrado cruzado. Helpers `tiene_foto()/foto_url()` en `Alumno` encapsulan fallback iniciales/color hash (reusa `AVATAR_COLORS` y `hashlib.md5`).
- *Alternativa descartada:* Tabla `alumno_fotos` 1:1 → complejidad sin historial. Reusar mismo dir `perfil` → riesgo de ` _drop_avatar_files` borrando foto de alumno si UUID colisiona.

**Decisión 2: Replicar pipeline `_procesar_avatar` en `registro/infrastructure/alumno_foto_storage.py`**
- *Por qué:* PIL verify + exif_transpose + thumbnail LANCZOS + WEBP ya está batallado y maneja orientación móvil. Extraer a módulo compartido rompería frontera `identidad` vs `registro`; duplicar lógica aislada es aceptable (DRY menor que acoplamiento cross-módulo). Nombres `{alumno_id}_{uuid}.webp` evitan enumeración.
- *Alternativa descartada:* Helper genérico en `app/shared/` → implicaría mover config y crear dependencia compartida innecesaria para 2 usos.

**Decisión 3: Constantes `ALUMNO_FOTO_*` en `app/config.py` espejo de `PERFIL_*` pero con `MAX_SIZE 2MB`**
- *Por qué:* 10MB de perfil es excesivo para foto tomada en campo con datos móviles; 2MB reduce tiempo de subida. Mantener `MAX_DIM 1000 FULL 600 THUMB 90` para consistencia visual.
- *Alternativa descartada:* Reusar `PERFIL_AVATAR_MAX_SIZE` 10MB → subidas lentas en 3G.

**Decisión 4: Ruta `GET /registro/foto/<id>` y `?t=1` con `@login_required` en `registro_controller`**
- *Por qué:* Fotos son dato personal, deben heredar auth del módulo que las crea. Reusa `_path_seguro` y `send_file` con `private, max-age=0` de perfil. No nueva blueprint.
- *Alternativa descartada:* Ruta en `consulta` → confundiría ownership (foto pertenece a registro domain).

**Decisión 5: Detalle 2 cards con wrap 110px exacto + tabla consolidada**
- *Por qué:* Paridad visual con perfil reduce curva de aprendizaje. 110px es el valor canónico de `#avatarPreviewWrap` (`style.css:1640`). Tabla única con `<h6>` por sección mantiene todos los campos sin perder info, usando mismos `table-sm` y badges.
- *Alternativa descartada:* 1 card con banner superior → rompe patrón perfil y complica responsive.

**Decisión 6: Borrado físico al eliminar (soft delete también borra archivos)**
- *Por qué:* Decisión explícita del usuario: foto se elimina con alumno por "problemas de asistencia / no desea estudiar". No conservar snapshot histórico salvo que `auditoria.avatar` referencie (reusa check existente).
- *Alternativa descartada:* Conservar archivos tras soft delete → ocupa disco y expone dato que el usuario pidió eliminar.

## Risks / Trade-offs

- **Upload sin enctype** → `request.files` vacío y foto silenciosamente ignorada → Mitigación: template con `enctype="multipart/form-data"` y test que verifica presencia de atributo.
- **Envío con foto grande en móvil lento** → timeout → Mitigación: `capture="environment"` + validación JS previa (FileReader, check size <2MB antes de submit) y feedback toast.
- **Borrado huérfano si commit falla tras guardar archivo** → archivo en disco sin fila DB → Mitigación: guardar archivo solo tras validar todo y antes de `db.session.commit()`, y en `except` borrar archivo si se creó.
- **Thumb N+1 en listado** → si se hace query por foto separada, paginación 20 se vuelve 21 queries → Mitigación: `foto` ya está en `Alumno` row, no requiere join; thumb es solo URL derivada.
- **Exposición por path traversal** → Mitigación: `_path_seguro` con `realpath` + `startswith` como en perfil.

## Migration Plan

1. Crear `ALUMNO_FOTO_DIR` y helpers en `Alumno` (columna nullable).
2. `flask db migrate -m "add alumno foto"` → `flask db upgrade` (local) → `flask db stamp` en prod si needed, archivos existentes quedan NULL.
3. Deploy code con templates y controller nuevo; fotos viejas siguen con fallback iniciales sin regresión.
4. Rollback: revert migración `flask db downgrade` y eliminar `uploads/alumnos/`; detalle vuelve a 4 cards si se revierte template, pero migración downgrade deja columna fuera sin pérdida de otros datos.

## Open Questions

- Ninguna — todas las ambigüedades (opcional, roles, thumb, cámara, privacidad, borrado, tamaño) fueron resueltas con el usuario en explore.
