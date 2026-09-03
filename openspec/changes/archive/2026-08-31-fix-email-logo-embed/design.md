## Context

Ver `proposal.md`. Estado actual: `recuperar_contrasena.html:10` usa `https://raw.githubusercontent.com/.../logo.png` y `email_adapter.enviar_correo` solo adjunta `MIMEText(html)` sin imágenes. El cambio anterior (`enable-smtp-password-recovery`) dejó el envío funcional pero dependiente de CDN externo.

## Goals / Non-Goals

**Goals:**
- Logo visible offline / sin bloquear por cliente (CID).
- Un único punto de adjunto (adapter) para todos los emails.
- Fallback no-bloqueante si falta el archivo.

**Non-Goals:**
- Cambiar dominio/host de imágenes, ni tocar `SERVER_NAME` / `url_for(_external)` (problema 2 aparte).
- Rediseñar plantilla de correo ni cambiar copy.
- Soporte para múltiples logos por plantilla (v1: un único CID `logo_sgrv`).

## Decisions

**1. CID con MIMEImage vs URL absoluta con `_external=True`**
- Elegido: `cid:logo_sgrv` + `MIMEImage(open('app/static/img/logo.png','rb').read())` con `Content-ID: <logo_sgrv>`, `Content-Disposition: inline`.
- Alternativa URL absoluta (`https://sgrv.azconsultingperu.com/static/img/logo.png`) descartada: sigue requiriendo fetch externo y falla si el cliente bloquea imágenes remotas o si el dominio no está desplegado (justo problema 2). CID es autocontenido.
- Base64 `data:` URI descartado: muchos clientes (Outlook) lo bloquean y aumenta tamaño.

**2. Adjunto en adapter, no en plantilla**
- Plantillas solo cambian `src` a `cid:logo_sgrv`; el adapter se encarga de adjuntar. Así no se duplica lógica y todos los correos heredan el fix.
- Ruta del archivo: `os.path.join(current_app.root_path, 'static', 'img', 'logo.png')` (resuelve a `app/static/img/logo.png`). Se lee en cada envío; costo despreciable (<50KB) y evita cache stale.

**3. Fallback si falta archivo**
- Si `logo.png` no existe o no se puede leer, el adapter hace `logger.warning` y envía sin adjunto. El HTML seguirá con `cid:` y el cliente mostrará alt text, pero el envío no lanza excepción (cumple spec).

## Risks / Trade-offs

- **Tamaño del correo +~30KB por envío** → Mitigación: logo PNG ya optimizado (~10-20KB), impacto menor que la ganancia de entregabilidad.
- **Clientes que ignoran CID** (raro) → Mitigación: `alt="SGRV"` ya presente; el correo sigue legible.
- **Doble Content-ID si se llama dos veces** → Mitigación: generar un único `MIMEImage` por `enviar_correo` invocación.

## Migration Plan

1. Editar `app/templates/email/*.html` → `src="cid:logo_sgrv"`.
2. Parchear `email_adapter.py` para adjuntar `MIMEImage`.
3. Tests: verificar `MIMEMultipart` contiene `image/png` con `logo_sgrv`.
4. Deploy: sin migración DB, solo código + plantilla. Rollback: revertir ambos archivos.

## Open Questions

- Ninguna para este scope.
