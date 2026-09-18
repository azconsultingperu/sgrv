## Why

En el formulario `registro/index.html` y `editar.html` al seleccionar una Institución Educativa solo se autocompleta `distrito` (extraído con `split(' - ')` del texto de la opción), pero `provincia` queda vacía porque el modelo `InstitucionEducativa` sí tiene `provincia` en BD (y en `distrito`, `region`, `tipo`) pero el template/JS no la usa. El usuario debe llenarla a mano y queda inconsistente con los datos maestros.

## What Changes

- En `registro/index.html` y `registro/editar.html`, cada `<option>` de `institucion_id` expondrá `data-distrito`, `data-provincia` y `data-region` provenientes de `c.distrito`/`c.provincia`/`c.region`.
- El JS del formulario al `change` del select rellenará **los tres campos** `distrito`, `provincia` y `region` (readonly) desde `dataset`; al limpiar selección, los dejará vacíos (region vuelve a vacío o a valor por defecto si se decide).
- En la rehidratación tras error de validación (`form=request.form`), el JS re-disparará el `change` para que `distrito/provincia/region` muestren los valores del instituto previamente elegido sin intervención.
- **BREAKING**: No hay — solo datos adicionales visibles; el envío del form sigue siendo solo `institucion_id` (distrito/provincia/region son readonly, no se envían).
- Verificar con los colegios seed existentes (6 instituciones) que `provincia` se muestra correctamente (ej. Ascope, Paiján, etc.) y que no se rompe `custom-select` ni `distrito`.

## Capabilities

### New Capabilities
- No new capability — es corrección de comportamiento existente dentro del formulario.

### Modified Capabilities
- `registro-form`: Requisito de autocompletado de `distrito/provincia` tras elegir institución (antes solo distrito, ahora también provincia y región).

## Impact

- **Templates**: `app/templates/registro/index.html`, `app/templates/registro/editar.html` — añadir `data-*` a options.
- **Static JS**: fragmento inline en ambos templates (listener `institucion_id -> distrito/provincia/region`) y rehidratación.
- **Backend**: sin cambios (solo lectura de `c.provincia` en Jinja); no requiere migración ni API nueva. Si se desea robustez, opcional endpoint `GET /registro/institucion/<id>` como fallback, fuera de alcance inicial.
- **Tests**: verificar que `GET /registro/` renderiza `data-provincia` y que JS llena campos.
