## Context

Ver proposal. El `POST` throttled hoy hace `flash` + `render_template`, y el `fetch` parsea `res.text`. En el harness de test el flash se consume, pero en navegador real con `fetch` + `base.html` el flash puede quedar para el siguiente `GET` si no se maneja como JSON.

## Goals / Non-Goals

**Goals:** Un único toast por intento throttled, sin reaparición en F5.
**Non-Goals:** Cambiar la lógica de rate limit ni el `DISABLE_RATE_LIMIT`.

## Decisions

- Para `fetch` devolver JSON en vez de HTML con `flash`; para no-JS mantener `flash`.
- Alternativa `session.pop` descartada por mezclar dos mecanismos.

## Risks

- JS que espera HTML con `includes` → Mitigación: actualizar `recuperar.html` para manejar JSON y fallback a HTML.
