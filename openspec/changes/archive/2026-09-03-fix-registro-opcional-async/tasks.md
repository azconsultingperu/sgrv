## 1. Visual requerido/opcional

- [x] 1.1 Añadir `*` rojo a labels de apellidos, nombres, dni, fecha_nacimiento, sexo, celular, institucion_id y `(opcional)` gris a email, direccion, carrera_id, area_interes, modalidad_contacto, fecha/hora visita, promotor, observaciones en `registro/index.html` y `editar.html`, más leyenda `* Campos obligatorios` arriba del form, y verificar que se ven en desktop y móvil.
- [x] 1.2 Validar `sexo` en `registro_controller.registrar` (si `sexo not in ('M','F','O')` añadir a `errores` y marcar `is-invalid` en el select) y verificar que POST sin sexo devuelve 200 con error y POST con sexo pasa.

## 2. Email async

- [x] 2.1 Modificar `app/modules/notifications/application/event_handlers.py` para encolar `notificar_nuevo_registro` en `threading.Thread daemon` y `app/modules/notifications/infrastructure/email_adapter.py` para usar `timeout=10` en `SMTP_SSL`/`SMTP`, y verificar que `POST /registro/` responde 302 en <1s aunque `MAIL_SERVER` sea lento (mock con delay).
- [x] 2.2 Verificar que fallo SMTP no revierte registro y solo loguea (mail log), y que el alumno queda en BD.

## 3. Spinner Guardar

- [x] 3.1 Añadir JS en `registro/index.html` y `editar.html` que en `form submit` deshabilite el botón Guardar/Actualizar, cambie a spinner y prevenga doble POST, rehabilitando si `checkValidity` falla, y verificar que doble click solo hace un POST y que validación fallida no deja botón bloqueado.
