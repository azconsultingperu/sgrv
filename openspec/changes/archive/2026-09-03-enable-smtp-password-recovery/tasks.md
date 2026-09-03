## 1. Configuración SMTP cPanel

- [x] 1.1 Actualizar `app/config.py` para soportar `MAIL_USE_SSL`/`MAIL_USE_TLS` como bool real, `MAIL_DEFAULT_SENDER` con display name "SGRV – IESTP Paiján", y defaults a `sgrv.azconsultingperu.com:465/SSL` + `soporte@sgrv.azconsultingperu.com`; verificar con `python -c "from app import create_app; app=create_app(); print(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], app.config['MAIL_USE_SSL'])"` que lee env correctamente.
- [x] 1.2 Actualizar `.env.example` con bloque cPanel (465/SSL) documentado y placeholder de password, y verificar que `.gitignore` ignora `.env`; verificar con `grep -q "^\.env$" .gitignore && echo ok`.
- [x] 1.3 Endurecer `app/modules/notifications/infrastructure/email_adapter.py` para bifurcar `SMTP_SSL` vs `SMTP+starttls`, usar `email.utils.formataddr` con `MAIL_DEFAULT_SENDER`, y loguear sin exponer password; verificar con test manual `enviar_correo` a una dirección de prueba (o mock smtplib) que el `From` es el institucional y que 465 no hace STARTTLS.

## 2. Modelo y migración para token single-use + rate limit

- [x] 2.1 Añadir al dominio identidad la persistencia de token (columnas `reset_token_hash`/`reset_token_expires_at`/`reset_token_used` en `usuarios` o nueva tabla `password_reset_tokens`) + tabla o columnas para `password_reset_attempts` (ip, username, created_at); verificar que `app/modules/identidad/domain/usuario.py` importa solo `app.shared.db` y que `make lint-boundaries` pasa.
- [x] 2.2 Generar migración Alembic `flask --app run.py db migrate -m "password recovery single-use and rate limit"` y revisarla; verificar `flask --app run.py db upgrade` en dev y que `flask db downgrade` revierte limpio.

## 3. Backend auth – flujo seguro

- [x] 3.1 Parchear `app/modules/identidad/presentation/auth_controller.py:recuperar` para respuesta siempre genérica (eliminar rama `No se encontró...`), integrar rate limit 3/15 min por IP y DNI (helper con query ventana), generar token con `max_age=900`, persistir hash+expiry, y delegar fallo SMTP a `enviar_correo_recuperacion` sin flash técnico; verificar con `pytest tests/test_recover_*.py` que enumeración no filtra (mismo body/código para existente vs inexistente) y que el 4º intento en 15 min es throttled.
- [x] 3.2 Parchear `auth_controller.reset_password` para validar firma+expiry+hash+`used` flag, marcar token como usado en el mismo commit que `set_password`, y auditar; verificar que reusar token tras éxito redirige con "inválido o ha expirado" y que token expirado (>15 min) es rechazado (mock de tiempo o `time.sleep` en test).
- [x] 3.3 Rediseñar `app/templates/email/recuperar_contrasena.html` como plantilla HTML institucional (no texto plano) con: logo SGRV, saludo personalizado `Hola {{ usuario.nombres }},`, botón CTA visible "Restablecer Contraseña" con `href={{ reset_url }}` (además del link en texto plano como fallback), nota "Este enlace vence en 15 minutos" y tono/colores/tipografía alineados a `login.html` (`#16264A`, `#2F80ED`, Inter/Segoe UI); actualizar TTL de "1 hora" a "15 minutos"; verificar con `render_template` que el HTML contiene logo, saludo, botón, URL y nota de 15 min, y que se envía como `MIMEText(html, 'html')`.

## 4. Frontend reset_password – paridad visual

- [x] 4.1 Reescribir `app/templates/auth/reset_password.html` para usar `auth.css?v=17`, `auth-validation.js` (`initAuthValidation` con badge `!`), mismo `login-card`/`auth-brand`, footer `¡Crea, Innova e Inspira!`, y validación de fortaleza; verificar visualmente en 1024px que iguala a `login.html` (snapshot o inspección de clases) sin haber tocado `recuperar.html` ni `auth.css` salvo cableado mínimo.

## 5. Verificación y cierre

- [x] 5.1 Añadir/actualizar tests de regresión (`tests/test_boundaries.py` + nuevos `tests/test_password_recovery.py`) que cubran: enumeración, TTL 15, single-use, rate limit, From institucional, y fallo SMTP silencioso; verificar `FLASK_ENV=testing venv/bin/python -m pytest tests/ -v` pasa y `make lint-boundaries` pasa.
- [x] 5.2 Smoke manual end-to-end con credenciales reales de `soporte@sgrv.azconsultingperu.com:465` (solicitar DNI+correo de prueba en dev), verificar que el correo llega con remitente correcto y que el enlace restablece contraseña; documentar pasos de deploy cPanel (`FLASK_APP=passenger_wsgi.py flask db upgrade`).
