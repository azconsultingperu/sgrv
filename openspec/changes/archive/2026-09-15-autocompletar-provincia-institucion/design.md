## Context

Ver `proposal.md` Why. Actualmente `registro/index.html:79-93` y `editar.html` renderizan `<option>{{ c.nombre }} - {{ c.distrito }}</option>` sin `data-provincia`/`data-region`, y el listener `select[name="institucion_id"] -> change` solo hace `split(' - ')[1]` para `distrito`, dejando `provincia` siempre vacío. El modelo `InstitucionEducativa` ya tiene `provincia` y `region` en BD (seed 6 colegios). `custom-select.js` envuelve el `<select>` nativo y dispara `change` en él, por lo que el listener sobre el nativo sigue siendo válido. No se requiere migración ni API.

## Goals / Non-Goals

**Goals:**
- Autocompletar `provincia` (y `region`) al elegir institución, consistente con `distrito`.
- Mantener compatibilidad con `custom-select` y con rehidratación tras error.
- Sin nuevas dependencias ni cambios de esquema.

**Non-Goals:**
- Crear endpoint REST para instituciones en esta iteración (follow-up si se necesita búsqueda async).
- Autocompletar `region` con lógica distinta a `provincia` (mismo flujo data-*).

## Decisions

**Decisión 1: Data attributes en `<option>` vs endpoint fetch**
- Elegido `data-distrito`/`data-provincia`/`data-region` en cada `option` (render Jinja `c.distrito|c.provincia|c.region`). *Por qué*: datos ya cargados en `colegios` para el select; evita round-trip, es instantáneo, no añade latencia ni falla de red, y funciona con `custom-select` que preserva `dataset` del nativo. *Alternativa fetch* (`GET /registro/institucion/<id>`) descartada por sobreingeniería y por requerir manejo de loading/error.

**Decisión 2: Leer de `dataset` del `option` seleccionado, no de `text.split`**
- Cambiar `selected.text.split(' - ')[1]` por `selected.dataset.distrito` / `provincia` / `region`. *Por qué*: `provincia` no está en el texto visible; `dataset` es fuente única de verdad y evita parse frágil. Mantiene `distrito` consistente si el formato de texto cambia.

**Decisión 3: Mismo listener para `index` y `editar`, y rehidratación via `dispatchEvent('change')` existente**
- Reutilizar bloque `if (sel && sel.value) sel.dispatchEvent(...)` ya usado para distrito. *Por qué*: cubre caso de re-render tras error y edición con valor pre-cargado sin duplicar lógica.

## Risks / Trade-offs

- **Colegios con `provincia` nula/vacía** → Mitigación: JS asigna `''` si dataset vacío; input queda vacío (comportamiento previo).
- **Texto de option con formato distinto** → Mitigación: ya no se depende de `split`; dataset es independiente del texto visible.
- **custom-select oculta el nativo con `display:none`** → dataset sigue accesible en `select.options[selectedIndex].dataset`; listener sobre nativo sigue disparándose vía `custom-select` que hace `select.dispatchEvent('change')`.

## Migration Plan

1. Editar `registro/index.html` y `editar.html` para añadir `data-*` a options.
2. Ajustar listener JS para leer dataset y escribir `provincia`/`region`.
3. Verificar con `pytest` y prueba manual de rehidratación.
4. Rollback: revertir templates a estado previo (solo distrito).
