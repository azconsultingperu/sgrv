## Context

Ver `proposal.md` Why. Tras `alumno-foto`, el POST tarda 3 min por SMTP síncrono y el form no distingue requeridos de opcionales (todos los labels iguales, `novalidate` desactiva `required` nativo, `sexo` no está en `errores`).

## Goals / Non-Goals

**Goals:** Marcar visualmente requerido/opcional, validar `sexo`, async email con timeout, spinner.

**Non-Goals:** No cambiar modelo, no añadir campos, no migrar a Celery, no wizard.

## Decisions

**Decisión 1: Marcado A+C con `*` y `(opcional)`**
- *Por qué:* `*` rojo es patrón universal para requerido; `(opcional)` gris es explícito y coincide con `Foto (opcional)` ya usado. Leyenda arriba evita duda. No requiere JS.
- *Alternativa descartada:* Solo `*` → opcional queda ambiguo; solo `(opcional)` → requerido no resalta.

**Decisión 2: Validación `sexo` en backend + `is-invalid`**
- *Por qué:* Hoy `sexo` se lee pero no se valida; si viene '' se guarda '' y rompe reportes. Añadir a `errores` y marcar `select` con `is-invalid` + `invalid-feedback` es consistente con `dni`/`celular`. También propagar a `custom-select` si existe.
- *Alternativa descartada:* Validar solo en frontend → bypass con `curl`.

**Decisión 3: Email async vía `threading.Thread daemon` con `timeout=10`**
- *Por qué:* Suficiente para SGRV (pocos emails/día), sin infra extra. `daemon=True` no bloquea shutdown. `SMTP_SSL(..., timeout=10)` evita 3 min. Handler hace `thread.start()` y retorna; el request responde 302 en ms.
- *Alternativa descartada:* Celery/RQ → overkill, requiere Redis. `asyncio` → Flask es sync.

**Decisión 4: Spinner con `disabled` y `checkValidity()`**
- *Por qué:* Previene doble POST y da feedback. Si `form.checkValidity()===false`, se cancela submit y se rehabilita botón para que el usuario corrija.
- *Alternativa descartada:* Solo `disabled` sin check → si el form es inválido, el botón queda bloqueado para siempre.

## Risks / Trade-offs

- **Thread sin reintento puede perder email si SMTP cae justo al enviar** → Mitigación: loguea error, el registro igual queda; el admin puede reenviar manualmente o se añade reintento futuro.
- **Marca `(opcional)` alarga labels en móvil** → Mitigación: `small text-muted` no rompe layout, ya probado en `Foto (opcional)`.
- **Spinner puede ocultar error de validación si el JS no rehabilita** → Mitigación: rehabilitar en `catch` y en `invalid` event.

## Migration Plan

- Sin migración. Deploy: templates + controller + email_adapter. Rollback: revertir commits, el email vuelve a ser síncrono pero sin pérdida de datos.

## Open Questions

- Ninguna.
