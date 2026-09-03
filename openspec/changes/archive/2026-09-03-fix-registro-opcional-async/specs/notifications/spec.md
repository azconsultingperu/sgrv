## MODIFIED Requirements

### Requirement: Envío de email vía eventos

`notifications` SHALL enviar emails solo como handler suscrito a `AlumnoRegistrado` y `UsuarioCreado` vía `app/shared/events.py`, usando un adapter de infraestructura que envuelva `smtplib` y SHALL aislar errores sin revertir la transacción ya commiteada. El adapter SHALL soportar SSL/STARTTLS según config y SHALL usar `MAIL_DEFAULT_SENDER` con nombre visible, y SHALL nunca propagar el error técnico al usuario (solo log). El handler `on_alumno_registrado` SHALL encolar el envío en un `threading.Thread` daemon con `timeout=10` en `SMTP_SSL`/`SMTP` para no bloquear el request; el `POST /registro/` SHALL responder `302` en <500ms incluso si SMTP tarda o falla.

#### Scenario: Email tras registro
- **WHEN** `registro_service.crear_alumno_con_visita` publica `AlumnoRegistrado` y hace commit
- **THEN** `notifications/application/event_handlers.py:on_alumno_registrado` encola el envío en thread daemon y retorna inmediatamente; el request `POST /registro/` responde `302` sin esperar el SMTP

#### Scenario: Sin evento no hay email
- **WHEN** se crea un alumno pero la transacción hace rollback
- **THEN** ningún email se envía.

#### Scenario: Fallo SMTP no bloquea registro
- **WHEN** `SMTP_SSL` tarda >10s o falla (timeout, auth)
- **THEN** el thread loguea `logger.error` y termina, pero el alumno ya está guardado y el usuario ve `success`; el request original no espera más de 500ms

#### Scenario: Fallo SMTP aislado en recuperación
- **WHEN** `enviar_correo_recuperacion` falla durante recuperación de contraseña
- **THEN** el adapter retorna `False`, loguea el error con `current_app.logger.error` sin incluir password, y el controller responde con mensaje genérico sin exponer el fallo.
