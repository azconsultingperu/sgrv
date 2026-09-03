## Why

El registro demora 3 minutos por email síncrono que bloquea el POST, el usuario no distingue qué campos son opcionales (falta * y (opcional)), y el botón Guardar no da feedback (sin spinner, permite doble click). Con 50% del form el sistema guarda igual porque sexo y fecha no están validados como requeridos y el usuario cree que falló.

## What Changes

- **Visual opcional A+C:** En `registro/index.html` y `editar.html` cada label requerido lleva `*` rojo y cada opcional lleva `(opcional)` gris; arriba del form leyenda `* Campos obligatorios`. Requeridos: apellidos, nombres, dni, fecha_nacimiento, sexo, celular, institucion_id. Opcionales: email, direccion, carrera_id, area_interes, modalidad_contacto, desea/solicita, fecha/hora visita (auto), promotor, observaciones, foto. Mantiene `foto` con badge (opcional) existente.
- **Validación sexo y fecha:** Añade `sexo` a `errores` en `registro_controller.registrar` (si `sexo not in ('M','F','O')` → error) y marca `is-invalid` en el select. Fecha ya se valida vía try pero ahora con borde rojo.
- **Email async:** `notifications/event_handlers.on_alumno_registrado` deja de llamar `smtplib` bloqueante; encola en `threading.Thread daemon` con `timeout=10` y loguea error sin bloquear request. `POST /registro/` responde en <300ms.
- **Spinner Guardar:** En `formRegistro` submit, deshabilita botón, cambia a `<span class="spinner-border spinner-border-sm"></span> Guardando...`, evita doble submit; si validación frontend falla, rehabilita.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `registro-form`: Marcado visual requerido/opcional, validación de sexo/fecha con is-invalid, y spinner en Guardar.
- `notifications`: Envío de email async con timeout y sin bloquear registro.

## Impact

- `app/templates/registro/index.html`, `editar.html` — labels y leyenda, JS spinner
- `app/modules/registro/presentation/registro_controller.py` — validación sexo
- `app/modules/notifications/application/event_handlers.py` + `infrastructure/email_adapter.py` — thread async, timeout
- Sin migración, sin cambios en modelo.
