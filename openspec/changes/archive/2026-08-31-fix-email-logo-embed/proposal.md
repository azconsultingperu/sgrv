## Why

El correo de recuperación muestra "Logo SGRV" como texto alternativo porque `<img src="https://raw.githubusercontent.com/.../logo.png">` depende de un CDN externo bloqueado por muchos clientes (Gmail, Outlook). Para la identidad institucional del IESTP Paiján el logo debe verse siempre, sin depender de URLs externas.

## What Changes

- Reemplazar en `app/templates/email/recuperar_contrasena.html` (y en cualquier otra plantilla en `app/templates/email/` que use logo externo) el `src` externo por `cid:logo_sgrv`.
- Extender `app/modules/notifications/infrastructure/email_adapter.py` para adjuntar `app/static/img/logo.png` como `MIMEImage` con `Content-ID: <logo_sgrv>` en cada envío (todos los correos del sistema, no solo recuperación).
- Mantener compatibilidad: si el archivo no existe, no romper el envío (log warning, envío sin CID).
- Sin cambios de API ni de flujo de recuperación.

## Capabilities

### New Capabilities
<!-- none - es mejora de entregabilidad, no nueva capacidad -->

### Modified Capabilities
- `notifications`: el envío de email SHALL incrustar el logo institucional como CID en lugar de depender de URLs externas, y las plantillas SHALL referenciarlo via `cid:`.

## Impact

- `app/modules/notifications/infrastructure/email_adapter.py` (lógica de adjunto CID)
- `app/templates/email/recuperar_contrasena.html` (y `nuevo_registro.html`, `nuevo_usuario.html` si usan logo)
- `app/static/img/logo.png` (fuente, ya existe, se lee en runtime; no se versiona nuevo binario)
- Tests de regresión para verificar que el `MIMEImage` está presente y el HTML contiene `cid:`
