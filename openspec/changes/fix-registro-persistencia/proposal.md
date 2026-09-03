## Why

Al enviar `POST /registro/` con datos incompletos, el sistema hace `flash` + `render_template(..., form=request.form)` pero los 3 selects (`institucion_id, carrera_id, promotor_id`) vuelven vacíos a "Seleccionar..." aunque el usuario sí los había elegido. El comparador `form.xxx == c.id` falla porque `form` es string (`'3'`) y `c.id` es int (`3`) en Jinja (`'3' == 3` → False). Los derivados `distrito/provincia/edad` (readonly + JS) tampoco se repintan. El usuario debe re-elegir todo y percibe pérdida de datos.

## What Changes

- **Selects persistentes:** Cambiar en `registro/index.html` y `editar.html` los 3 selects a `{% if form.xxx|string == c.id|string %}selected{% endif %}` (igual que `consulta` ya hace). Añade `is-invalid` si aplica.
- **Derivados repintados:** Al cargar con `form` ya poblado, disparar `calcularEdad()` y el `change` de `institucion_id` para rellenar `distrito/provincia/edad` sin esperar interacción.
- **Foto:** No se repinta por seguridad del browser (comportamiento esperado, se documenta).

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `registro-form`: Persistencia de selects y derivados tras error de validación.

## Impact

- `app/templates/registro/index.html` — 3 selects + JS de re-hidratación
- `app/templates/registro/editar.html` — mismo
- `app/modules/registro/presentation/registro_controller.py` — sin cambios (ya pasa `form=request.form`)
- Sin migración, sin cambios en modelo.
