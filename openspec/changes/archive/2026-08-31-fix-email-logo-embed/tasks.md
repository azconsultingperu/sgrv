## 1. Plantillas de correo

- [x] 1.1 Reemplazar en `app/templates/email/recuperar_contrasena.html` (y en `nuevo_registro.html` / `nuevo_usuario.html` si contienen `<img>`) el `src` externo por `cid:logo_sgrv` y verificar que `grep -r "raw.githubusercontent" app/templates/email/` no devuelve resultados y que `grep -r "cid:logo_sgrv" app/templates/email/` sí lo hace.
- [x] 1.2 Verificar que la plantilla sigue renderizando `Hola {{ usuario.nombres }}` y el botón con `{{ reset_url }}` tras el cambio mediante `render_template` en test.

## 2. Adapter de email

- [x] 2.1 Extender `app/modules/notifications/infrastructure/email_adapter.py:enviar_correo` para adjuntar `app/static/img/logo.png` como `MIMEImage` con `Content-ID: <logo_sgrv>` y `Content-Disposition: inline` (lectura desde `current_app.root_path/static/img/logo.png`), con fallback que loguea warning y no rompe el envío si el archivo falta; verificar con test unitario que `MIMEMultipart` contiene parte `image/png` con `logo_sgrv`.

## 3. Verificación

- [x] 3.1 Añadir test `tests/test_email_logo_cid.py` que renderiza la plantilla y envía vía `enviar_correo` mockeando `smtplib` y asserts: HTML contiene `cid:logo_sgrv`, no contiene URL externa, y el mensaje tiene adjunto CID; verificar con `venv/bin/python -m pytest tests/test_email_logo_cid.py -v` y `venv/bin/python -m pytest tests/test_password_recovery.py -v` que no hay regresión.
