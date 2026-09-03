## Why

El flujo de recuperación de contraseña existe a medias: el backend (`auth_controller.recuperar` + `reset_password`) genera tokens stateless de 1h y el frontend `recuperar.html` tiene validación pulida, pero el envío real nunca llega a funcionar en cPanel porque la config SMTP sigue apuntando a Gmail placeholder (`azconsultingperu@gmail.com:587/TLS`), el `From` ignora `MAIL_DEFAULT_SENDER`, la respuesta filtra enumeración de usuarios, el token es reutilizable y no hay rate limit. Con las credenciales de soporte confirmadas (`soporte@sgrv.azconsultingperu.com` en `sgrv.azconsultingperu.com:465/SSL`, remitente "SGRV – IESTP Paiján") se puede cerrar el flujo end-to-end con las políticas ya acordadas (TTL 15 min, single-use, 3 intentos/15 min, error genérico).

## What Changes

- Configurar SMTP cPanel: `sgrv.azconsultingperu.com:465 SSL` con usuario `soporte@sgrv.azconsultingperu.com`; usar `MAIL_DEFAULT_SENDER` + nombre visible "SGRV – IESTP Paiján"; soportar tanto SSL directo (465) como TLS (587) según `MAIL_USE_SSL`/`MAIL_USE_TLS`; actualizar `.env.example` y documentar que el password va solo en `.env` (gitignored).
- Endurecer `app/modules/notifications/infrastructure/email_adapter.py` para respetar `MAIL_DEFAULT_SENDER`, manejar SSL vs STARTTLS correctamente, loguear sin exponer error crudo al usuario y mantener `try/except` que no revierte la request.
- Corregir `auth_controller.recuperar` para respuesta **siempre genérica** (mismo mensaje/flash/toast exista o no el usuario), aplicar rate limit (3/15 min por IP y por DNI), y delegar el fallo SMTP al sistema de notificaciones sin mostrar trace al frontend.
- Cambiar token a **TTL 15 min** (`max_age=900`) y hacerlo **single-use**: persistir hash/estado de token (tabla o columna en `usuarios`/`sesiones` o nueva `password_reset_tokens`) y marcarlo usado tras `reset_password` exitoso; rechazar reuse con mensaje "enlace ya utilizado o expirado".
- Alinear `reset_password.html` con la identidad de `login.html`/`recuperar.html` (mismo `login-card`, `auth.css v17`, `auth-validation.js` con badge `!`, spinner, etc.) sin tocar `recuperar.html`/`auth.css` más allá del cableado mínimo.
- Registrar/actualizar tests de regresión para el flujo (enumeración, expiración, reuse, rate limit).

## Capabilities

### New Capabilities

- `password-recovery-hardening`: endurecimiento del flujo de recuperación (token single-use 15 min, anti-enumeración estricta, rate limit 3/15 min, alineación visual de `reset_password.html`). Complementa sin duplicar el spec existente de UX.

### Modified Capabilities

- `recover-password`: el spec vivo hoy solo cubre UX frontend (consistencia visual, microcopy, validación inline, feedback). Este change añade requisitos de **backend seguro** (respuesta genérica real, TTL y single-use, rate limit, manejo SMTP silencioso) que antes no estaban especificados.
- `notifications`: el spec actual cubre envío vía eventos con `smtplib` tolerante a fallos. Se modifica para **soportar SSL directo 465**, respetar `MAIL_DEFAULT_SENDER` con nombre visible, y definir el contrato de "nunca exponer error técnico al usuario".

## Impact

- Archivos: `app/config.py`, `app/modules/notifications/infrastructure/email_adapter.py`, `app/modules/identidad/presentation/auth_controller.py`, `app/modules/identidad/domain/` (nueva entidad/columna para token si aplica), `app/templates/auth/reset_password.html`, `app/templates/email/recuperar_contrasena.html` (ajuste de copy TTL), `.env.example`, `migrations/` (si hay nueva tabla/columna), `tests/`.
- Dependencias: no se añade `Flask-Mail`; se sigue con `smtplib` + `itsdangerous`. Si se introduce throttling persistente puede usar tabla o cache en memoria (sin Redis).
- Fronteras modulares: `identidad` sigue dependiendo de `notifications` solo vía `email_adapter` (fachada permitida) o evento; no se rompe `lint-imports`.
- Riesgo: cambio de puerto a 465/SSL debe probarse en cPanel real; rollback es solo revertir env.
