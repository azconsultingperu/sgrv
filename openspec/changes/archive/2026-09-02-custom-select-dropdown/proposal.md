## Why

Los 15 `<select>` nativos del sistema (registro, usuarios, auditoría, consulta) usan el desplegable del OS, que no respeta la identidad visual (bordes, sombras, paleta, hover) del resto del diseño. El patrón de `dropdown` custom ya usado en el navbar (`ADMINISTRADOR`) sí la respeta y es reutilizable sin añadir dependencias.

## What Changes

- Reemplazar visualmente los 15 `select.form-select` por un componente hand-made que reutiliza el patrón del navbar: se oculta el `<select>` nativo (`display:none` pero permanece en el DOM), se renderiza un botón con look `form-select` y un `ul.dropdown-menu` con `li` por cada `option`. **BREAKING (visual):** el desplegable pasa de nativo a custom, pero sin cambiar `name`/`value`.
- **Puente de validación:** si el `<select>` nativo tiene `is-invalid` (añadido por `auth-validation.js` o por validación de `required`), el botón visible SHALL reflejar `is-invalid` con `border-color: var(--danger-color)` y mostrar el `invalid-feedback` existente; al corregir, se limpia igual que en inputs.
- **Evento `change`:** al elegir una opción en el custom, SHALL actualizar `select.value`, disparar `select.dispatchEvent(new Event('change', {bubbles:true}))` y `input` para que el listener de `registro/index.html:188` (`institucion_id → distrito`) siga funcionando.
- **Filtros GET:** los selects de `auditoria/index.html` y `consulta/index.html` mantienen `name`/`value` en el `<select>` oculto, por lo que el `GET` envía los mismos parámetros sin cambios en backend.
- **Selected inicial desde Jinja:** al inicializarse, el custom SHALL leer `select.options[select.selectedIndex]` (el `selected` renderizado por `{% if ... %}selected{% endif %}` en edición) y mostrar ese `text` en el botón; si no hay `selected` (placeholder), muestra el texto del `option` vacío o placeholder. Respeta `form.reset()` y cambios dinámicos de opciones.

## Capabilities

### New Capabilities
- `custom-select`: Componente hand-made de reemplazo visual para `select.form-select` con desplegable custom, puente de validación, propagación de `change` y respeto de `selected` inicial, reutilizable para cualquier formulario futuro sin dependencia externa.

### Modified Capabilities
- Ninguna — no existe spec previa de selects; `form-validation` no cambia de requisitos, solo se integra.

## Impact

- `app/static/js/custom-select.js` (nuevo, ~80 líneas) — inicializa `querySelectorAll('select.form-select')`, expone `initCustomSelect`.
- `app/static/css/style.css` — estilos del botón y `ul.dropdown-menu` del custom (reusa vars de `form-select`/`dropdown-menu` existentes), sin tocar `auth.css`.
- `app/templates/base.html` — incluir `custom-select.js` y bump `?v=`; `app/templates/registro/*`, `usuarios/*`, `auditoria/*`, `consulta/*` sin cambios de markup (solo el `<select>` existente).
- Sin impacto en backend, `auth-validation.js` (solo integración vía `is-invalid`) ni en `main.js` salvo inicialización.
