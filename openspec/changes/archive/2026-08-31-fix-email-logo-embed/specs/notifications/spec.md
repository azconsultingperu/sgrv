## ADDED Requirements

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
