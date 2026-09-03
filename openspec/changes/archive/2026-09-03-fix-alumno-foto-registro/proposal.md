## Why

El registro con foto opcional quedó con 4 fricciones que rompen el flujo: el POST a veces no muestra toast de éxito aunque el alumno sí se crea (aparece en /consulta), el bloque de foto no centra botones en móvil, el botón dice "Cambiar foto" aun sin foto, y el placeholder "--" no usa el avatar por defecto. Hay que corregirlos sin cambiar el contrato de foto opcional.

## What Changes

- **Registro no completa / toast no brinca:** Unifica flashes a un solo mensaje final (evita `flash danger` + `flash success` en el mismo request que se pisa). Si `guardar_foto` falla, muestra solo `danger` con el motivo y **no** hace `success`; si ok o sin foto, solo `success`. Evita `db.session.rollback()` tras el `commit` del `UnitOfWork` que puede borrar el flash de sesión.
- **Móvil centrado:** Centra en `<768px` la foto, botones y texto de ayuda en `registro/index.html` y `editar.html` con `justify-content-center` / `text-center` y `justify-content-md-start` en desktop. Mantiene `110px` circular.
- **Botón dinámico:** En `registro/index.html` (sin foto) el botón inicial es "Añadir foto"; tras seleccionar archivo pasa a "Cambiar foto" y aparece "Eliminar". En `editar.html` respeta estado existente.
- **Placeholder por defecto:** Reemplaza "--" por `<img src="avatar-default.svg">` dentro de `#alumnoFotoWrap` con opacidad tenue, igual que `perfil` sin foto.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `alumno-foto`: Corrige contrato de flashes, validación y placeholder del registro con foto (sin cambiar almacenamiento/serving).
- `consulta-detalle`: No cambia — ya está en 2 cards, se mantiene.
- `consulta-listado`: No cambia.

## Impact

- `app/modules/registro/presentation/registro_controller.py` — lógica de flashes/commit de foto
- `app/templates/registro/index.html` — botón dinámico, centrado móvil, placeholder svg
- `app/templates/registro/editar.html` — mismo centrado y placeholder
- `app/static/css/style.css` — si hace falta ajuste de `#alumnoFotoWrap` para centrado (opcional)
- Sin migración, sin cambios en `alumno_foto_storage.py` ni rutas.
