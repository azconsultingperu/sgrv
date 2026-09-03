## Context

Ver `proposal.md` Why. `registro_controller:100` ya pasa `form=request.form` (ImmutableMultiDict de strings). El bug está en el template: `form.institucion_id == c.id` compara `'3' == 3` → False.

## Goals / Non-Goals

**Goals:** Que los 3 selects y sus derivados sobrevivan al re-render tras `flash` sin tocar el controller.

**Non-Goals:** No repintar `file` input, no cambiar validación, no tocar modelo.

## Decisions

**Decisión 1: `|string` en los 3 selects**
- *Por qué:* Es lo que ya usa `consulta/index.html` y es la forma idiomática en Jinja para comparar string vs int. No requiere cambiar el controller a castear a int.
- *Alternativa descartada:* Castear en controller `form.get('institucion_id', type=int)` y pasar como int → rompería otros campos que esperan string.

**Decisión 2: Re-disparar JS al cargar si `form` ya trae valores**
- *Por qué:* `distrito/provincia` y `edad` son readonly y se llenan por `change`/`fetch`. Si el form ya viene con `value`, basta con `if (form.institucion_id) { triggerChange() }` y `if (fnInput.value) calcularEdad()` en `DOMContentLoaded`.
- *Alternativa descartada:* Pintar `distrito` directo en Jinja desde `colegios` → duplica lógica y no contempla `edad`.

## Risks / Trade-offs

- **Foto siempre se pierde** → Mitigación: texto de ayuda ya dice que es opcional y se debe re-seleccionar; no hay forma segura de repintar `file`.
- **Custom-select puede no reflejar `selected`** → Mitigación: `custom-select.js` ya observa `selected` al iniciar; con `|string` el `selected` quedará bien y el botón mostrará el texto correcto.

## Migration Plan

- Solo templates. Sin migración. Rollback: revertir `|string`.

## Open Questions

- Ninguna.
