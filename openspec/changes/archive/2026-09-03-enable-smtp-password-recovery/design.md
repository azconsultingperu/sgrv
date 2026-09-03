## Context

SGRV es monolito modular Flask. La recuperación hoy es stateless (`itsdangerous` 1h, reutilizable) con `smtplib.SMTP:587/STARTTLS` hardcodeado a Gmail y `From=MAIL_USERNAME`. El frontend `recuperar.html` ya es pulido (validación inline, spinner, fetch genérico) pero el backend filtra enumeración. El contrato SMTP real es cPanel `sgrv.azconsultingperu.com:465/SSL` con `soporte@sgrv.azconsultingperu.com`. Ver `proposal.md` y specs `password-recovery-hardening` / `recover-password` / `notifications` para el qué.

## Goals / Non-Goals

**Goals:**
- Enviar correo real por 465/SSL con remitente institucional sin hardcodear secretos.
- TTL 15 min + single-use verificable.
- Anti-enumeración estricta y rate limit 3/15 min por IP y DNI.
- Paridad visual de `reset_password.html` con login/recuperar.

**Non-Goals:**
- Modificar `recuperar.html`/`auth.css` más allá de cableado mínimo (prohibido).
- Introducir Redis/Celery/cola async ni `Flask-Mail` (se mantiene `smtplib` + bus sync).
- Cambiar el sistema de roles/sesiones ni el flujo de login.
- Outbox persistente para retry de email (v1: log + fallo silencioso).

## Decisions

**1. Adapter SMTP dual SSL/TLS**
- `email_adapter.enviar_correo` bifurca: si `MAIL_USE_SSL is True` o `MAIL_PORT==465` → `smtplib.SMTP_SSL`; si no, `SMTP` + `starttls()` si `MAIL_USE_TLS`. `From` pasa a `MAIL_DEFAULT_SENDER` con display name `SGRV – IESTP Paiján` vía `email.utils.formataddr`.
- Alternativa `Flask-Mail` descartada: añade dependencia y no aporta nada que `smtplib` no cubra; además ya existe shim sin Flask-Mail.
- Rationale: compatibilidad Gmail (587) y cPanel (465) sin fork de código.

**2. Token single-use sin nueva tabla (opción preferida) vs nueva tabla**
- Opción A (preferida): añadir columnas a `usuarios` (`reset_token_hash`, `reset_token_expires_at`, `reset_token_used`) o reutilizar `sesiones`. Simple, sin migración de tabla nueva, una query por reset.
- Opción B: tabla `password_reset_tokens` (usuario_id, token_hash, expires_at, used_at). Más limpia si se quiere historiar/auditar múltiples tokens.
- Decisión: implementar **Opción A** si se quiere minimizar migraciones; documentar ambas y dejar que `tasks.md` ejecute A, con nota de migrar a B si se requiere auditoría de múltiples tokens. Hash del token con `hashlib.sha256` para no guardar el raw.
- TTL: `serializer.loads(max_age=900)` (900s = 15 min). Copiar también en template de email.

**3. Rate limit sin infraestructura externa**
- Sin Redis: tabla `password_reset_attempts` o diccionario en DB + limpieza por `peru_now()`. Clave compuesta `(ip, username)` con ventana 15 min. 3 filas recientes → 429/genérico.
- Alternativa memoria `Flask-Limiter` descartada por añadir dependencia y no persistir entre workers gunicorn.
- Se implementa como helper en `auth_controller` con query `WHERE created_at > now-15min`.

**4. Respuesta genérica**
- `recuperar()` siempre: `flash genérico` + misma respuesta HTTP (200) y mismo cuerpo; el JS `fetch` ya espera genérico pero se elimina la rama `No se encontró...` del backend. Logs diferencian internamente.

**5. Reset visual**
- `reset_password.html` se reescribe para usar `auth.css?v=17`, `auth-validation.js`, mismo `login-card`, toggle ojo si se desea, y validación de fortaleza existente. Sin tocar `recuperar.html`.

## Risks / Trade-offs

- **SSL 465 mal configurado en dev sin cPanel** → Mitigación: `.env.example` documenta ambas variantes y `email_adapter` loguea el modo elegido; test manual con `python -m smtplib` o `openssl s_client`.
- **Single-use con columnas en usuarios pierde historial** → Mitigación: auditar cada uso en `auditoria` (`Cambio de contraseña` ya existe) y dejar puerta a migrar a tabla dedicada.
- **Rate limit en DB aumenta writes** → Mitigación: ventana corta (15 min) y purga periódica; no bloquea el happy path.
- **Token stateless + DB state = doble fuente de verdad** → Mitigación: validar ambas (firma + expiración + `used` flag); si una falla, rechazar.
- **No tocar recuperar.html limita feedback** → Mitigación: el JS ya maneja genérico; solo el backend debe alinearse.

## Migration Plan

1. Migrar `app/config.py` para `MAIL_DEFAULT_SENDER` con display name y parsing bool de `MAIL_USE_SSL/TLS`.
2. Parchear `email_adapter.py` (SSL/TLS + From).
3. Migración Alembic para columnas de token/attempts (si se elige tabla/columnas).
4. Parchear `auth_controller.py` (rate limit + genérico + single-use).
5. Reescribir `reset_password.html` + ajustar copy de `recuperar_contrasena.html`.
6. Actualizar `.env.example` y verificar `.gitignore` contiene `.env`.
7. `flask db upgrade` en dev y `FLASK_APP=passenger_wsgi.py flask db upgrade` en cPanel. Rollback: revertir commits y `flask db downgrade` si hubo migración.

## Open Questions

- ¿Se prefiere tabla dedicada `password_reset_tokens` sobre columnas en `usuarios` para trazabilidad? Ambas cumplen spec; se propone columnas por simplicidad y se deja la decisión al implementador sin cambiar tasks.
