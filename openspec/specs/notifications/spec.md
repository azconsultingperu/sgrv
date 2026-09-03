## Purpose

Completar el módulo notifications al layout oficial del monolito modular y centralizar el envío de emails vía eventos de dominio sin imports directos cross-módulo.

## Requirements

### Requirement: Estructura completa de notifications

El módulo `app/modules/notifications/` SHALL respetar el layout `domain/`, `application/`, `infrastructure/`, `presentation/` + `public.py` (o `__init__.py` re-export) como los demás módulos, y SHALL exponer su comportamiento solo vía `public.py` o eventos.

#### Scenario: Layout válido
- **WHEN** se lista `app/modules/notifications/`
- **THEN** existen `domain/`, `application/`, `infrastructure/`, `presentation/` y `public.py` (aunque `domain`/`presentation` puedan ser mínimos) y `make lint-boundaries` pasa.

#### Scenario: Sin import directo a services
- **WHEN** `app/modules/registro` o `identidad` necesitan enviar email
- **THEN** no contienen `from app.services.email_service import` y en su lugar publican `AlumnoRegistrado`/`UsuarioCreado` que `notifications` escucha.

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

### Requirement: Logo institucional incrustado en emails

Todos los correos enviados por el sistema SHALL incrustar el logo de `app/static/img/logo.png` como recurso CID y SHALL referenciarlo en el HTML via `cid:logo_sgrv`, sin depender de URLs externas (`https://raw.githubusercontent.com`, `https://sgrv.azconsultingperu.com/static/...`, etc.).

#### Scenario: HTML usa CID
- **WHEN** se renderiza `email/recuperar_contrasena.html` (u otra plantilla en `app/templates/email/` que incluya logo)
- **THEN** el `<img>` contiene `src="cid:logo_sgrv"` y no contiene `https://raw.githubusercontent.com` ni `https://sgrv.azconsultingperu.com/static`.

#### Scenario: Mensaje MIME incluye imagen CID
- **WHEN** `email_adapter.enviar_correo` envía cualquier correo
- **THEN** el `MIMEMultipart` contiene una parte `MIMEImage` con `Content-ID: <logo_sgrv>` y `Content-Disposition: inline`, adjuntando el bytes de `app/static/img/logo.png`.

#### Scenario: Fallback si falta el archivo
- **WHEN** `app/static/img/logo.png` no existe en el filesystem al momento del envío
- **THEN** el envío no falla: el adapter loguea un warning y envía el correo sin el adjunto CID (el HTML sigue con `cid:` pero el cliente mostrará alt text, sin excepción).

### Requirement: Soporte SMTP SSL 465 y remitente institucional

El adapter de email SHALL soportar tanto SSL directo (puerto 465) como STARTTLS (puerto 587) según configuración, SHALL usar `MAIL_DEFAULT_SENDER` con nombre visible "SGRV – IESTP Paiján <soporte@sgrv.azconsultingperu.com>" como `From`, y SHALL leer credenciales solo desde variables de entorno/`.env` (nunca hardcodeadas).

#### Scenario: Envío por SSL 465
- **WHEN** `.env` tiene `MAIL_SERVER=sgrv.azconsultingperu.com`, `MAIL_PORT=465`, `MAIL_USE_SSL=True`, `MAIL_USERNAME=soporte@sgrv.azconsultingperu.com`, `MAIL_DEFAULT_SENDER=soporte@sgrv.azconsultingperu.com`
- **THEN** `email_adapter.enviar_correo` conecta con `smtplib.SMTP_SSL` (sin STARTTLS) y el correo llega con `From: SGRV – IESTP Paiján <soporte@sgrv.azconsultingperu.com>`.

#### Scenario: Envío por STARTTLS 587 sigue funcionando
- **WHEN** la config es `MAIL_PORT=587` con `MAIL_USE_TLS=True`
- **THEN** el adapter usa `SMTP` + `starttls()` y el mismo `From` institucional, manteniendo compatibilidad con Gmail u otros proveedores.

#### Scenario: Credenciales no hardcodeadas
- **WHEN** se inspecciona el código y `app/config.py`
- **THEN** no hay password SMTP en texto plano; `MAIL_PASSWORD` se lee de `os.environ` y `.env` está en `.gitignore`; `.env.example` solo muestra placeholder.

### Requirement: Plantilla de recuperación HTML institucional

La plantilla `email/recuperar_contrasena.html` SHALL ser HTML (no texto plano), SHALL incluir el logo SGRV, SHALL saludar de forma personalizada con el nombre del usuario, SHALL mostrar un botón CTA visible "Restablecer Contraseña" enlazado a `reset_url` además del link en texto plano como fallback, SHALL aclarar que el enlace vence en 15 minutos, y SHALL respetar la identidad visual institucional de `login.html` (paleta `#16264A`/`#2F80ED`, tipografía Inter/Segoe UI, tono formal).

#### Scenario: Contenido visual completo del correo
- **WHEN** se renderiza el correo de recuperación tras el cambio
- **THEN** el HTML contiene el logo SGRV, el texto `Hola {{ usuario.nombres }}` (o `nombres + apellidos`), un `<a>` estilizado como botón con `href={{ reset_url }}` y texto "Restablecer Contraseña", la URL en texto plano debajo, y la nota "Este enlace vence en 15 minutos" (no "1 hora").

#### Scenario: Envío como HTML
- **WHEN** `enviar_correo_recuperacion` envía el correo
- **THEN** el mensaje se adjunta como `MIMEText(html, 'html')` y no como texto plano.
